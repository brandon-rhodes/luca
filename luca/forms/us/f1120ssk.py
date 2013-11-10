from luca.forms.formlib import Form
from luca.kit import zero, zstr


title = ("Form 1120S Schedule K-1: Shareholder's Share of Income, Deductions,"
         " Credits, etc.")

versions = u'2012',
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
    pdf.load('us.f1120ssk--{}.pdf'.format(f.form_version))

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
