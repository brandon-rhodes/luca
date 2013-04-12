from luca.forms.formlib import Form
from luca.kit import Decimal, cents

title = u"Supplemental Income and Loss"
filename = 'f1040se--2012.pdf'
zero = cents(0)

def defaults(form):
    f = form
    for c in 'ABC':
        setattr(f, c, Form())
        subform = getattr(f, c)
        for i in range(3, 20):
            setattr(subform, 'line%d' % i, zero)

def compute(form):
    f = form
    f.A.line20 = f.A.line3

def fill(form, fields):
    f = form
    #     'topmostSubform[0].Page1[0].Line1[0].Pg1Table1a[0].a[0].p1-t5[0]':
    #         f.A.address,
    fields['p1-t1['] = [f.name, f.name]
    fields['t2['] = [f.ssn, f.ssn]
    #fields['
    # for i in range(3, 20):
    #
    fields['Line5['] = list('abcdef')  #split(f.A.line3) + 'abcd'.split()

def zz(value):
    if not isinstance(value, Decimal):
        return value
    return str(value).split('.')
