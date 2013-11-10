from luca.kit import cents, zzstr

title = u'Form 1040 Schedule B: Interest and Ordinary Dividends'
versions = '2012',
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

def fill_out(form, pdf):
    f = form
    pdf.load('us.f1040sb--{}.pdf'.format(f.form_version))
    pdf.pages = 1,

    pdf['_01['] = f.name
    pdf['_02['] = f.ssn

    pdf.pattern = 'f1-{:02}['

    n = 3
    for payer, amount in f.line1:
        pdf[n] = payer
        pdf[n+1], pdf[n+2] = zzstr(amount)
        n += 3

    pdf[45], pdf[46] = zzstr(f.line2)
    pdf[47], pdf[48] = zzstr(f.line3)
    pdf[49], pdf[50] = zzstr(f.line4)

    n = 51
    for payer, amount in f.line5:
        pdf[n] = payer
        pdf[n+1], pdf[n+2] = zzstr(amount)
        n += 3

    pdf[96], pdf[97] = zzstr(f.line6)
    pdf[98] = f.line7b

    pdf.pattern = '{}'

    a, b = f.line7a
    pdf['-cb1[0]'] = 'yes' if a else 'Off'
    pdf['-cb1[1]'] = 'no' if not a else 'Off'
    pdf['-cb2[0]'] = 'yes' if b else 'Off'
    pdf['-cb2[1]'] = 'no' if not b else 'Off'
    pdf['-cb3[0]'] = 'yes' if f.line8 else 'Off'
    pdf['-cb3[1]'] = 'no' if not f.line8 else 'Off'
