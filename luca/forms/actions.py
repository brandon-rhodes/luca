"""One-off program to generate tax forms until I learn the workflow."""

import os
import re
import importlib
import subprocess
from StringIO import StringIO

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

    form = formlib.load_json(u'{"inputs": {}}')

    if hasattr(form_module, 'defaults'):
        form_module.defaults(form)

    print formlib.dump_json(form).encode('utf-8')


def complete(jsonpath):

    with open(jsonpath) as f:
        form = formlib.load_json(f.read().decode('utf-8'))

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

    json_string = formlib.dump_json(form).encode('utf-8')
    print('Updating {}'.format(jsonpath))
    with open(jsonpath, 'w') as f:
        f.write(json_string)

    if not os.path.isdir('out'):
        os.mkdir('out')

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


class Fields(object):
    """Object that lets you fill in the fields in a PDF."""

    def __init__(self, names, items=None):
        self.names = names
        self.items = [] if (items is None) else items

    @property
    def all(self):
        return list(self.items)

    @all.setter
    def all(self, value):
        self[''] = [value] * len(self.names)

    def __getitem__(self, pattern):
        if isinstance(pattern, slice):
            names = self.names[pattern]
        elif isinstance(pattern, int):
            names = self.names[pattern : pattern + 1]
        else:
            names = [ name for name in self.names if pattern in name ]
        return Fields(names, self.items)

    def __setitem__(self, pattern, value_or_values):
        fields = self[pattern]
        fields.set(value_or_values)

    def set(self, value_or_values):
        names = self.names
        if isinstance(value_or_values, (tuple, list)):
            values = value_or_values
        else:
            values = [value_or_values]
        if len(names) != len(values):
            raise ValueError('there are %d matching names but %d values'
                             '\n\nNames:\n\n%s\n\nValues:\n\n%s'
                             % (len(names), len(values),
                                '\n'.join(names),
                                '\n'.join(str(v) for v in values)))
        for tup in zip(names, values):
            self.items.append(tup)


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
