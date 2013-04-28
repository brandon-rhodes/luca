"""One-off program to generate tax forms until I learn the workflow."""

import os
import re
import importlib
import subprocess
from StringIO import StringIO
from subprocess import Popen, PIPE

import fdfgen
import requests
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen.canvas import Canvas

from luca.forms import formlib

integer_re = re.compile(r'\d+$')
decimal_re = re.compile(r'\d+\.\d+$')


def print_defaults(form_name):
    form_module_name = 'luca.forms.' + form_name
    try:
        form_module = importlib.import_module(form_module_name)
    except ImportError:
        raise ValueError('cannot find a Luca form named {!r}'.format(
                form_module_name))

    form = formlib.Form()
    form.form = form_name

    if hasattr(form_module, 'defaults'):
        form_module.defaults(form)

    print formlib.dump_json(form).encode('utf-8')


def complete(jsonpath):
    with open(jsonpath) as f:
        json_data = f.read()

    form, form_module = process(json_data)
    json_string = formlib.dump_json(form).encode('utf-8')
    print('Updating {}'.format(jsonpath))
    with open(jsonpath, 'w') as f:
        f.write(json_string)

    if not os.path.isdir('out'):
        os.mkdir('out')

    if hasattr(form_module, 'fill_out'):
        # Support new-style fill_out() pattern, to which all forms will
        # soon be rewritten.
        pdf = PDF()
        form_module.fill_out(form, pdf)
        basename, ext = os.path.splitext(os.path.basename(jsonpath))
        outputpath = os.path.join('out', basename + '.pdf')
        pdf.save(outputpath)
        return

    pdfpath = form.form + '--2012.pdf'
    fullpath = download_pdf(pdfpath)

    outputpath = os.path.join('out', os.path.basename(pdfpath))
    print 'Generating', outputpath
    inputpath = fullpath
    if hasattr(form_module, 'fill'):
        run_fill(form, form_module, inputpath, outputpath)
        inputpath = outputpath
    if hasattr(form_module, 'draw'):
        run_draw(form, form_module, inputpath, outputpath)


def process(json_data):
    form = formlib.load_json(json_data.decode('utf-8'))

    if not hasattr(form, 'form'):
        raise ValueError('your JSON "input" object needs to specify a "form"')

    form_module_name = 'luca.forms.' + form.form
    try:
        form_module = importlib.import_module(form_module_name)
    except ImportError:
        raise ValueError('cannot find a Luca form named {!r}'.format(
                form_module_name))

    if hasattr(form_module, 'defaults'):
        form._enter_default_mode()
        form_module.defaults(form)

    form._enter_output_mode()
    form_module.compute(form)

    return form, form_module


def run_fill(form, form_module, pdfpath, outputpath):
    out = subprocess.check_output(['pdftk', pdfpath, 'dump_data_fields'])
    lines = [ line.split(None, 1) for line in out.splitlines() ]
    names = [ fields[1] for fields in lines if fields[0] == 'FieldName:' ]

    fields = Fields(names)
    form_module.fill(form, fields)
    fields = fields.items

    fdf = fdfgen.forge_fdf('', fields, [], [], [])
    fdf_file = open('data.fdf', 'w')
    fdf_file.write(fdf)
    fdf_file.close()

    subprocess.check_call(['pdftk', pdfpath, 'fill_form', 'data.fdf',
                           'output', outputpath])


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

    # The beginning.

    def load(self, filename):
        self.original_pdf_path = download_pdf(filename)
        output = subprocess.check_output(
            ['pdftk', self.original_pdf_path, 'dump_data_fields'])
        lines = [ line.split(None, 1) for line in output.splitlines() ]
        self.names = [ words[1] for words in lines
                       if words[0] == 'FieldName:' ]

    # Various tools for setting field values.

    def __setitem__(self, substring, values):
        if not isinstance(substring, str):
            substring = self.pattern.format(substring)
        names = [name for name in self.names if substring in name]
        if not isinstance(values, (tuple, list)):
            values = [values]
        if len(names) != len(values):
            raise ValueError('{} names match {!r} but you supplied {} values'
                             '\n\nNames:\n\n{}\n\nValues:\n\n{}'
                             .format(len(names), substring, len(values),
                                     '\n'.join(names),
                                     '\n'.join(str(v) for v in values)))
        for tup in zip(names, values):
            self.fdf_fields.append(tup)

    @property
    def all(self):
        raise NotImplemented('you can only set .all, not access it')

    @all.setter
    def all(self, value):
        self.items.extend((name, value) for name in self.names)

    # The finale.

    def save(self, path):
        print 'Saving', path

        fdf = fdfgen.forge_fdf('', self.fdf_fields, [], [], [])
        pages = [str(p) for p in self.pages]

        p1 = Popen(
            ['pdftk', self.original_pdf_path, 'fill_form', '-', 'output', '-'],
            stdin=PIPE, stdout=PIPE,
            )
        p2 = Popen(
            ['pdftk', '-', 'cat'] +  pages + ['output', path],
            stdin=p1.stdout,
            )
        p1.stdout.close()
        p1.stdin.write(fdf)
        p1.stdin.close()
        p2.wait()


def run_draw(form, form_module, inputpath, outputpath):
    with open(inputpath, 'rb') as f:
        inputdata = f.read()
    original_form = PdfFileReader(StringIO(inputdata))

    canvas = Canvas('fields.pdf')
    page_numbers = form_module.draw(form, canvas)
    overlays = PdfFileReader(StringIO(canvas.getpdfdata()))

    output = PdfFileWriter()

    for i in range(overlays.numPages):
        page = original_form.getPage(i)
        overlay = overlays.getPage(i)
        page.mergePage(overlay)
        if (page_numbers is None) or ((i + 1) in page_numbers):
            output.addPage(page)

    print('Writing {}'.format(outputpath))
    with open(outputpath, 'w') as f:
        output.write(f)
