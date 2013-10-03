"""One-off program to generate tax forms until I learn the workflow."""

import importlib
import os
import re
import subprocess
import sys
from StringIO import StringIO
from collections import defaultdict
from subprocess import Popen, PIPE

import fdfgen
import requests
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen.canvas import Canvas

from luca.forms import formlib
from luca.kit import dstr

integer_re = re.compile(r'\d+$')
decimal_re = re.compile(r'\d+\.\d+$')


def print_defaults(form_name, form_version):
    form_module_name = 'luca.forms.' + form_name
    try:
        form_module = importlib.import_module(form_module_name)
    except ImportError:
        raise ValueError('cannot find a Luca form named {!r}'.format(
                form_module_name))

    if form_version is None or form_version not in form_module.versions:
        print 'Form versions supported:'
        for version in form_module.versions:
            print '   ', version
        return

    form = formlib.Form()
    form.form_name = form_name
    form.form_version = form_version

    if hasattr(form_module, 'defaults'):
        form_module.defaults(form)

    print formlib.dump_json(form).encode('utf-8')


def check(dirpath):
    forms = defaultdict(list)
    tuples = []

    for filename, path, json_data in forms_inside_directory(dirpath):
        form, form_module = process(json_data)
        forms[form.form_name].append(form)
        tuples.append((filename, form, form_module))

    #print [f.form for f in forms]
    n = [0]

    def eq(name, value):
        n[0] += 1
        form  # necessary to establish scoping for the following eval
        actual = eval('form.' + name)
        if actual != value:
            print filename, name, '=', actual, 'but should be', dstr(value)
        # TODO: add --verbose and print in that case too

    for filename, form, form_module in tuples:
        form_check = getattr(form_module, 'check', None)
        if form_check is not None:
            form_check(form, forms, eq)

    print 'Ran', n[0], 'check{}'.format('' if n[0] == 1 else 's')


def complete(path):
    if os.path.isfile(path):
        return complete_form(path)

    for filename, jsonpath, json_data in forms_inside_directory(path):
        complete_form(jsonpath)


def complete_form(jsonpath):
    with open(jsonpath) as f:
        json_data = f.read()

    form, form_module = process(json_data)
    json_string = formlib.dump_json(form).encode('utf-8')
    print('Updating {}'.format(jsonpath))
    with open(jsonpath, 'w') as f:
        f.write(json_string)

    if not os.path.isdir('out'):
        os.mkdir('out')

    pdf = PDF()
    form_module.fill_out(form, pdf)
    basename, ext = os.path.splitext(os.path.basename(jsonpath))
    outputpath = os.path.join('out', basename + '.pdf')
    pdf.save(outputpath)


def forms_inside_directory(dirpath):
    for filename in os.listdir(dirpath):
        if not filename.endswith('.json'):
            continue
        path = os.path.join(dirpath, filename)
        with open(path) as f:
            json_data = f.read()
        yield filename, path, json_data


def load(json_data):
    form = formlib.load_json(json_data.decode('utf-8'))

    if not hasattr(form, 'form_name'):
        raise ValueError('your JSON "input" object'
                         ' needs to specify a "form_name"')

    form_module_name = 'luca.forms.' + form.form_name
    try:
        form_module = importlib.import_module(form_module_name)
    except ImportError:
        raise ValueError('cannot find a Luca form named {!r}'.format(
                form_module_name))

    if hasattr(form_module, 'defaults'):
        form._enter_default_mode()
        form_module.defaults(form)

    return form, form_module


def process(json_data):
    form, form_module = load(json_data)

    form._enter_output_mode()
    if hasattr(form_module, 'compute'):
        form_module.compute(form)

    return form, form_module


def download_pdf(pdfpath):
    fullpath = os.path.join('cache', pdfpath)
    if not os.path.isdir('cache'):
        os.mkdir('cache')
    if not os.path.isfile(fullpath):
        url = 'http://luca-forms.s3.amazonaws.com/' + pdfpath
        response = requests.get(url)
        if not response.ok:
            print 'Error: could not download form from', url
            return
        data = requests.get(url).content
        with open(fullpath, 'w') as f:
            f.write(data)
    return fullpath


class PDF(object):

    def __init__(self):
        self.pages = ['1-end']
        self.pattern = '{}'
        self.fdf_fields = []
        self.canvases = {}

    # The beginning.

    def load(self, filename):
        self.original_pdf_path = download_pdf(filename)
        output = subprocess.check_output(
            ['pdftk', self.original_pdf_path, 'dump_data_fields'])
        lines = [ line.split(None, 1) for line in output.splitlines() ]
        self.names = [ words[1] for words in lines
                       if words[0] == 'FieldName:' ]

    # How form logic writes data into fields.

    def __setitem__(self, args, values):
        if not isinstance(args, tuple):
            args = (args,)

        pattern = self.pattern
        if pattern is None:
            names = [''.join(str(arg) for arg in args)]
        else:
            try:
                substring = self.pattern.format(*args)
            except IndexError:
                raise ValueError('your index tuple {!r} is the wrong length '
                                 'for the template {!r}'
                                 .format(args, self.pattern))
            names = [name for name in self.names if substring in name]

        if not isinstance(values, (tuple, list)):
            values = [values]

        for i, name in enumerate(names):
            value = values[i % len(values)]
            tup = (name, value)
            self.fdf_fields.append(tup)

    # How form logic fetches canvases for drawing atop form pages.

    def get_canvas(self, page_number):
        canvas = self.canvases.get(page_number)
        if canvas is None:
            canvas = Canvas('canvas{}.pdf'.format(page_number))
            self.canvases[page_number] = canvas
        return canvas

    # The finale.

    def save(self, path):
        print 'Saving', path

        fdf = fdfgen.forge_fdf('', self.fdf_fields, [], [], [])
        pages = [str(p) for p in self.pages]

        # TODO: the "cat" step breaks the JavaScript used to print
        # Georgia Form 600S, so we should just skip the step if the PDF
        # fails to specify a list of pages.

        p1 = Popen(
            ['pdftk', self.original_pdf_path, 'fill_form', '-',
             'output', '-', 'flatten'],
            stdin=PIPE, stdout=PIPE,
            )
        p2 = Popen(
            ['pdftk', '-', 'cat'] + pages + ['output', path],
            stdin=p1.stdout,
            )
        p1.stdout.close()
        p1.stdin.write(fdf)
        p1.stdin.close()
        p2.wait()

        if not self.canvases:
            return

        with open(path, 'rb') as f:
            inputdata = f.read()
        pdf = PdfFileReader(StringIO(inputdata))

        output = PdfFileWriter()

        for i in range(pdf.numPages):
            page = pdf.getPage(i)
            canvas = self.canvases.get(i + 1)
            if canvas is not None:
                canvas.showPage()
                overlay = PdfFileReader(StringIO(canvas.getpdfdata()))
                page.mergePage(overlay.getPage(0))
            output.addPage(page)

        # We call write() outside of the open() context to avoid
        # truncating the file if write() dies with an exception.

        output_stream = StringIO()
        try:
            output.write(output_stream)
        except Exception as e:
            sys.stderr.write('PyPDF exception: {}\n'.format(e))
            sys.exit(1)
        with open(path, 'w') as f:
            f.write(output_stream.getvalue())
