from luca.forms.formlib import Form
from luca.kit import cents

title = u"Supplemental Income and Loss"
filename = 'f1040se--2012.pdf'

def defaults(form):
    f = form
    f.A = Form()
    f.A.line3 = cents(0)

def compute(form):
    f = form
    f.A.line20 = f.A.line3

def fill(form):
    f = form
    return {
        'topmostSubform[0].Page1[0].p1-t1[0]': f.name,
        'topmostSubform[0].Page1[0].p1-t2[0]': f.ssn,
        'topmostSubform[0].Page1[0].Line1[0].Pg1Table1a[0].a[0].p1-t5[0]':
            f.A.address,
        }
