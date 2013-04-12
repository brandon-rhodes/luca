from luca.forms.formlib import Form
from luca.kit import Decimal, cents

title = u"Supplemental Income and Loss"
filename = 'f1040se--2012.pdf'
zero = cents(0)

def defaults(form):
    f = form
    for c in 'ABC':
        setattr(f, c, Form())
        sub = getattr(f, c)
        sub.address = ''
        for i in range(3, 20):
            setattr(sub, 'line%d' % i, zero)

def compute(form):
    f = form

    for subform_name in 'ABC':
        sub = getattr(f, subform_name)
        expenses = zero
        for j in range(5, 19):
            expenses += getattr(sub, 'line{}'.format(j))

        sub.line20 = expenses
        sub.line21 = sub.line3 + sub.line4 - expenses
        sub.line22 = zero  # TODO: loss after limitation from Form 8582

def fill(form, fields):
    f = form
    #     'topmostSubform[0].Page1[0].Line1[0].Pg1Table1a[0].a[0].p1-t5[0]':
    #         f.A.address,

    fields['p1-t1['] = [f.name, f.name]
    fields['t2['] = [f.ssn, f.ssn]

    for i, subform_name in enumerate('ABC'):
        sub = getattr(form, subform_name)
        cols = slice(2*i, 2*(i+1))

        fields['Pg1Table1a['][i] = sub.address

        for j in range(3, 23):
            pattern = 'Line{}['.format(j)
            value = getattr(sub, 'line{}'.format(j))
            fields[pattern][cols] = zz(value)

def zz(value):
    if not isinstance(value, Decimal):
        return value
    if not value:
        return ('', '')
    return str(value).split('.')
