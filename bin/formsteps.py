"""One-off program to generate tax forms until I learn the workflow."""

import re
import json
from decimal import Decimal
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen.canvas import Canvas
from StringIO import StringIO

from luca.forms.us import form_940
from luca.forms.us import form_941

integer_re = re.compile(r'\d+$')
decimal_re = re.compile(r'\d+\.\d+$')

class Form(object):
    pass

if __name__ == '__main__':

    if False:
        jsonpath = 'taxforms/2012-us-Form-940.json'
        pdfpath = '/home/brandon/Downloads/f940.pdf'
        form_module = form_940

    else:
        jsonpath = 'taxforms/2013-01-US-Form-941.json'
        pdfpath = '/home/brandon/Downloads/f941.pdf'
        form_module = form_941

    with open(jsonpath) as f:
        data = json.loads(f.read())

    form = Form()
    for section, keyvalues in data.items():
        for key, value in keyvalues.items():
            if isinstance(value, float):
                value = Decimal('{:.2f}'.format(value))
            setattr(form, key, value)

    form_module.compute(form)

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

    with open('output.pdf', 'w') as f:
        output.write(f)
