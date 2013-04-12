"""One-off program to generate tax forms until I learn the workflow."""

import re
import importlib
import subprocess
from StringIO import StringIO

import fdfgen
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen.canvas import Canvas

from luca.forms import formlib

integer_re = re.compile(r'\d+$')
decimal_re = re.compile(r'\d+\.\d+$')


def complete(jsonpath, pdfpath, outputpath='completed-form.pdf'):

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

    if not pdfpath:
        return

    print 'Generating', outputpath
    if hasattr(form_module, 'draw'):
        run_draw(form, form_module, pdfpath, outputpath)
    else:
        run_fill(form, form_module, pdfpath, outputpath)


def run_fill(form, form_module, pdfpath, outputpath):
    field_dict = form_module.fill(form)
    fields = field_dict.items()

    fdf = fdfgen.forge_fdf('', fields, [], [], [])
    fdf_file = open('data.fdf', 'w')
    fdf_file.write(fdf)
    fdf_file.close()

    subprocess.check_call(['pdftk', pdfpath, 'fill_form', 'data.fdf',
                           'output', outputpath])


def run_draw(form, form_module, pdfpath, outputpath):
    original_form = PdfFileReader(file(pdfpath, 'rb'))

    canvas = Canvas('fields.pdf')
    form_module.draw(form, canvas)
    overlays = PdfFileReader(StringIO(canvas.getpdfdata()))

    output = PdfFileWriter()

    for i in range(overlays.numPages):
        page = original_form.getPage(i)
        overlay = overlays.getPage(i)
        page.mergePage(overlay)
        output.addPage(page)

    print('Writing {}'.format(outputpath))
    with open(outputpath, 'w') as f:
        output.write(f)
