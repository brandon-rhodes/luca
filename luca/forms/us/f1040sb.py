from luca.kit import Decimal, cents

title = u'Schedule B (Form 1040): Interest and Ordinary Dividends'
filename = 'f1040sb--2012.pdf'
zero = cents(0)

def defaults(form):
    f = form
    f.name = ''
    f.ssn = ''

    f.line1 = []
    f.line3 = zero

    f.line5 = []
    f.line7a = [False, False]
    f.line7b = ''
    f.line8 = False

def compute(form):
    f = form
    f.line2 = sum((amount for payer, amount in f.line1), zero)
    f.line4 = f.line2 - f.line3
    f.line6 = sum((amount for payer, amount in f.line5), zero)

def fill(form, fields):
    f = form

    def put(n, value):
        sa, sb = zz(value)
        fields['%02d[' % (n+0)] = sa
        fields['%02d[' % (n+1)] = sb

    fields['_01['] = f.name
    fields['_02['] = f.ssn

    n = 3
    for payer, amount in f.line1:
        fields['-%02d[' % n] = payer
        put(n+1, amount)
        n += 3

    put(45, f.line2)
    put(47, f.line3)
    put(49, f.line4)

    n = 51
    for payer, amount in f.line5:
        fields['%02d[' % n] = payer
        put(n+1, amount)
        n += 3

    put(96, f.line6)
    a, b = f.line7a
    fields['-cb1[0]'] = 'yes' if a else 'Off'
    fields['-cb1[1]'] = 'no' if not a else 'Off'
    fields['-cb2[0]'] = 'yes' if b else 'Off'
    fields['-cb2[1]'] = 'no' if not b else 'Off'
    fields['98['] = f.line7b
    fields['-cb3[0]'] = 'yes' if f.line8 else 'Off'
    fields['-cb3[1]'] = 'no' if not f.line8 else 'Off'

# General-purpose functions that will probably be factored out of here:

def yesno(value, fields):
    if value:
        fields[0] = 'Yes'
    else:
        fields[1] = 'No'

def z(value):
    if not value:
        return u''
    return unicode(value)

def zz(value):
    if not isinstance(value, Decimal):
        return value
    if not value:
        return (u'', u'')
    return unicode(value).split('.')
