from luca.forms.formlib import Form
from luca.kit import zero, zstr


first_few_lines = '1 2 3 4 5a 5b 6 7 8a 8b 9'.split()


def defaults(form):
    f = form
    f.year = 2012
    f.A = f.B = f.C = f.D = f.E = ''
    f.F = 100

    for number in first_few_lines:
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
    pdf.load('us.f1120ssk--{}.pdf'.format(f.year))
    pdf.format = 'p1-t{}[0]'

    # TODO: fields for non-calendar accounting year

    n = 4
    for letter in 'ABCDEF':
        pdf[n] = f[letter]
        n += 1

    for number in first_few_lines:
        pdf[n] = zstr(f['line', number])
        n += 1

    pdf[27] = zstr(f.line11)

    pdf.format = '{}'

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
