from luca.kit import Decimal, cents, zero, zzstr

title = u'Form 1040 Schedule SE: Self-Employment Tax, Long'
versions = u'2013',

def defaults(form):
    f = form
    f.name = ''
    f.ssn = ''
    f.line1a = zero
    f.line1b = zero
    f.line2 = zero
    f.line4b = zero
    f.line5a = zero
    f.line8a = zero
    f.line8b = zero
    f.line8c = zero

def check(form, forms, eq):
    nothing = [None]

    f1040sc = forms.get('us.f1040sc', nothing)[0]
    if f1040sc:
        if f1040sc.line31 > zero:
            eq('line2', f1040sc.line31)

def compute(form):
    f = form
    f.line3 = f.line1a + f.line1b + f.line2
    if f.line3 >= zero:
        f.line4a = cents(Decimal('.9235') * f.line3)
    else:
        f.line4a = f.line3
    f.line4c = f.line4a + f.line4b

    if f.line4c < Decimal('400.00'):
        f.line5b = zero
        f.line6 = zero
        f.line8d = zero
        f.line9 = zero
        f.line10 = zero
        f.line11 = zero
        f.line12 = zero
        f.line13 = zero
        return

    f.line5b = cents(Decimal('.9235') * f.line5a)
    if f.line5b < Decimal('100.00'):
        f.line5b = zero

    f.line6 = f.line4c + f.line5b

    line7 = cents('113700.00')

    if f.line8a >= line7:
        f.line8d = zero
        f.line9 = zero
        f.line10 = zero
    else:
        raise NotImplementedError()

    f.line11 = cents(f.line6 * Decimal('.029'))
    f.line12 = f.line10 + f.line11
    f.line13 = cents(f.line12 * Decimal('0.5'))

def fill_out(form, pdf):
    f = form
    pdf.load('us.f1040sse--{}.pdf'.format(f.form_version))
    pdf.pages = 2,

    pdf.pattern = 'p2-t{}[0]'

    pdf[1] = f.name
    pdf[2] = f.ssn

    n = 5
    for v in (f.line1a, f.line1b, f.line2, f.line3,
              f.line4a, f.line4b, f.line4c, f.line5a, f.line5b,
              f.line6, f.line8a, f.line8b, f.line8c, f.line8d,
              f.line9, f.line10, f.line11, f.line12):
        pdf[n], pdf[n+1] = zzstr(v)
        n += 2

    pdf[52], pdf[53] = zzstr(f.line13)
