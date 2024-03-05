from luca.forms.formlib import Form
from luca.kit import zero, zstr


title = ("Form 1120S Schedule K-1: Shareholder's Share of Income, Deductions,"
         " Credits, etc.")

versions = u'2010', u'2012', u'2013', u'2014'
first_nine_lines = '1 2 3 4 5a 5b 6 7 8a 8b 9'.split()


def defaults(form):
    f = form
    f.final = False
    f.amended = False
    f.beginning_date = ''
    f.ending_date = ''
    f.ending_year = ''
    f.A = f.B = f.C = f.D = f.E = ''
    f.F = 100

    for number in first_nine_lines:
        f['line', number] = zero

    def empty_line():
        e = Form()
        e.code = ''
        e.amount = zero
        return e

    for n in range(10, 17+1):
        if n == 11:
            f.line11 = zero
            continue
        f['line', n] = [empty_line(), empty_line()]

def compute(form):
    pass

def fill_out(form, pdf):
    f = form
    if f.form_version in (u'2020'):
        return fill_out_2020(form, pdf)
    if f.form_version in (u'2018', u'2019'):
        return fill_out_2019(form, pdf)
    if f.form_version == u'2017':
        return fill_out_2017(form, pdf)
    if f.form_version < u'2017':
        return old_fill_out(form, pdf)

    pdf.load('us.f1120ssk--{}.pdf'.format(f.form_version))
    pdf.pages = 1,

    # TODO: these two codes might no longer be correct

    pdf['c1_01_0_[0]'] = 'Yes' if f.final else 'Off'
    pdf['c1_02_0_[0]'] = 'Yes' if f.amended else 'Off'

    # TODO: specific dates instead of calendar year

    # pdf.pattern = 'p1-t{}[0]'

    # pdf[1] = f.beginning_date
    # pdf[2] = f.ending_date
    # pdf[3] = f.ending_year

    pdf.pattern = 'f1_{:02d}[0]'

    n = 6
    for letter in 'ABCDEFG':
        pdf[n] = f[letter]
        n += 1
        if letter == 'D':
            n += 1

    n += 4 # TODO: H and I

    for number in first_nine_lines:
        pdf[n] = zstr(f['line', number])
        n += 1

    pdf[27] = zstr(f.line11)

    pdf.pattern = '{}'

    def write_lines(line_number, n):
        lines = f['line', line_number]
        for line in lines:
            pdf['f1_{}[0]'.format(n)] = line.code
            n += 1
            pdf['f1_{}[0]'.format(n)] = zstr(line.amount)
            n += 1

    write_lines(10, 24)
    #write_lines(11, 28)
    write_lines(12, 35)
    write_lines(13, 51)
    write_lines(14, 61)
    write_lines(15, 75)
    write_lines(16, 85)
    write_lines(17, 95)

def fill_out_2020(form, pdf):
    f = form
    pdf.load('us.f1120ssk--{}.pdf'.format(f.form_version))
    pdf.pages = 1,

    # TODO: these two codes might no longer be correct

    pdf['c1_01_0_[0]'] = 'Yes' if f.final else 'Off'
    pdf['c1_02_0_[0]'] = 'Yes' if f.amended else 'Off'

    # TODO: specific dates instead of calendar year

    # pdf.pattern = 'p1-t{}[0]'

    # pdf[1] = f.beginning_date
    # pdf[2] = f.ending_date
    # pdf[3] = f.ending_year

    pdf.pattern = 'f1_{:02d}[0]'

    n = 6
    for letter in 'ABCDEF':
        pdf[n] = f[letter]
        n += 1

    n += 4 # TODO: G and H

    for number in first_nine_lines:
        pdf[n] = zstr(f['line', number])
        n += 1

    pdf[27] = zstr(f.line11)

    pdf.pattern = '{}'

    def write_lines(line_number, n):
        lines = f['line', line_number]
        for line in lines:
            pdf['f1_{}[0]'.format(n)] = line.code
            n += 1
            pdf['f1_{}[0]'.format(n)] = zstr(line.amount)
            n += 1

    write_lines(10, 24)
    #write_lines(11, 28)
    write_lines(12, 35)
    write_lines(13, 51)
    write_lines(14, 61)
    write_lines(15, 75)
    write_lines(16, 85)
    write_lines(17, 95)

def fill_out_2019(form, pdf):
    f = form
    pdf.load('us.f1120ssk--{}.pdf'.format(f.form_version))
    pdf.pages = 1,

    # TODO: these two codes might no longer be correct

    pdf['c1_01_0_[0]'] = 'Yes' if f.final else 'Off'
    pdf['c1_02_0_[0]'] = 'Yes' if f.amended else 'Off'

    # TODO: specific dates instead of calendar year

    # pdf.pattern = 'p1-t{}[0]'

    # pdf[1] = f.beginning_date
    # pdf[2] = f.ending_date
    # pdf[3] = f.ending_year

    pdf.pattern = 'f1_{:02d}[0]'

    n = 6
    for letter in 'ABCDEF':
        pdf[n] = f[letter]
        n += 1

    for number in first_nine_lines:
        pdf[n] = zstr(f['line', number])
        n += 1

    pdf[27] = zstr(f.line11)

    pdf.pattern = '{}'

    def write_lines(line_number, n):
        lines = f['line', line_number]
        for line in lines:
            pdf['f1_{}[0]'.format(n)] = line.code
            n += 1
            pdf['f1_{}[0]'.format(n)] = zstr(line.amount)
            n += 1

    write_lines(10, 24)
    #write_lines(11, 28)
    write_lines(12, 35)
    write_lines(13, 51)
    write_lines(14, 61)
    write_lines(15, 75)
    write_lines(16, 85)
    write_lines(17, 95)

def fill_out_2017(form, pdf):
    f = form
    pdf.load('us.f1120ssk--{}.pdf'.format(f.form_version))
    pdf.pages = 1,

    # TODO: these two codes might no longer be correct

    pdf['c1_01_0_[0]'] = 'Yes' if f.final else 'Off'
    pdf['c1_02_0_[0]'] = 'Yes' if f.amended else 'Off'

    # TODO: specific dates instead of calendar year

    # pdf.pattern = 'p1-t{}[0]'

    # pdf[1] = f.beginning_date
    # pdf[2] = f.ending_date
    # pdf[3] = f.ending_year

    pdf.pattern = 'f1_{:02d}[0]'

    n = 6
    for letter in 'ABCDEF':
        pdf[n] = f[letter]
        n += 1

    for number in first_nine_lines:
        pdf[n] = zstr(f['line', number])
        n += 1

    pdf[27] = zstr(f.line11)

    pdf.pattern = '{}'

    def write_lines(line_number, n):
        lines = f['line', line_number]
        for line in lines:
            pdf['p1-t{}a'.format(n)] = line.code
            pdf['p1-t{}[0]'.format(n)] = zstr(line.amount)
            n += 1

    write_lines(10, 22)
    write_lines(12, 28)
    write_lines(13, 36)
    write_lines(14, 41)
    write_lines(15, 48)
    write_lines(16, 53)
    write_lines(17, 58)

def old_fill_out(form, pdf):
    f = form
    pdf.load('us.f1120ssk--{}.pdf'.format(f.form_version))
    pdf.pages = 1,

    pdf['c1_01_0_[0]'] = 'Yes' if f.final else 'Off'
    pdf['c1_02_0_[0]'] = 'Yes' if f.amended else 'Off'

    pdf.pattern = 'p1-t{}[0]'

    pdf[1] = f.beginning_date
    pdf[2] = f.ending_date
    pdf[3] = f.ending_year

    n = 4
    for letter in 'ABCDEF':
        pdf[n] = f[letter]
        n += 1

    for number in first_nine_lines:
        pdf[n] = zstr(f['line', number])
        n += 1

    pdf[27] = zstr(f.line11)

    pdf.pattern = '{}'

    def write_lines(line_number, n):
        lines = f['line', line_number]
        for line in lines:
            pdf['p1-t{}a'.format(n)] = line.code
            pdf['p1-t{}[0]'.format(n)] = zstr(line.amount)
            n += 1

    write_lines(10, 22)
    write_lines(12, 28)
    write_lines(13, 36)
    write_lines(14, 41)
    write_lines(15, 48)
    write_lines(16, 53)
    write_lines(17, 58)
