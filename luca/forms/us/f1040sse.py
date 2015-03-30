from luca.kit import Decimal, cents, zero, zzstr

title = u'Form 1040 Schedule SE: Self-Employment Tax'
versions = u'2012', u'2013', u'2014'

def defaults(form):
    f = form
    f.name = ''
    f.ssn = ''
    f.line1a = zero
    f.line1b = zero
    f.line2 = zero

def check(form, forms, eq):
    nothing = [None]

    f1040sc = forms.get('us.f1040sc', nothing)[0]
    if f1040sc:
        if f1040sc.line31 > zero:
            eq('line2', f1040sc.line31)

def compute(form):
    f = form
    f.line3 = f.line1a + f.line1b + f.line2
    f.line4 = cents(Decimal('.9235') * f.line3)

    if f.line4 < Decimal('400.00'):
        f.line5 = zero
        f.line6 = zero
        return

    if f.form_version == u'2014':
        ss_limit = Decimal('117000.00')
        combined_rate = Decimal('.153')
        maximum_ss = Decimal('14508.00')
        medicare_rate = Decimal('.029')
    else:
        ss_limit = Decimal('110100.00')
        combined_rate = Decimal('.133')
        maximum_ss = Decimal('11450.40')
        medicare_rate = Decimal('.029')

    if f.line4 <= ss_limit:
        f.line5 = combined_rate * f.line4
    else:
        f.line5 = maximum_ss + medicare_rate * f.line4
    f.line5 = cents(f.line5)

    if f.form_version >= u'2014':
        f.line6 = cents(f.line5 / 2)
        return

    # TODO: re-check the following

    if f.line5 <= Decimal('14643.30'):
        f.line6 = Decimal('.5751') * f.line5
    else:
        f.line6 = Decimal('1100.00') + Decimal('.50') * f.line5
    f.line6 = cents(f.line6)

def fill_out(form, pdf):
    f = form
    pdf.load('us.f1040sse--{}.pdf'.format(f.form_version))
    pdf.pages = 1,

    pdf.pattern = 'p1-t{}[0]'

    pdf[1] = f.name
    pdf[2] = f.ssn

    pdf[5], pdf[6] = zzstr(f.line1a)
    pdf[7], pdf[8] = zzstr(f.line1b)
    pdf[9], pdf[10] = zzstr(f.line2)
    pdf[11], pdf[12] = zzstr(f.line3)
    pdf[13], pdf[14] = zzstr(f.line4)
    pdf[15], pdf[16] = zzstr(f.line5)
    pdf[17], pdf[18] = zzstr(f.line6)
