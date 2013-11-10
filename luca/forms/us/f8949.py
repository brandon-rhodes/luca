from luca.forms.formlib import Form
from luca.kit import cents, zstr

title = u'Form 8949: Sales and Other Dispositions of Capital Assets'
versions = '2011', '2012'
zero = cents(0)

def defaults(form):
    f = form
    f.name = ''
    f.ssn = ''

    build_example_row = {
        '2011': _build_example_row_2011,
        '2012': _build_example_row_2012
        }[form.form_version]

    f.Part_I = Form()
    f.Part_I.box = 'A'
    f.Part_I.table = [
        build_example_row(),
        build_example_row(),
        ]

    f.Part_II = Form()
    f.Part_II.box = 'A'
    f.Part_II.table = [
        build_example_row(),
        build_example_row(),
        ]

def _build_example_row_2011():
    f = Form()
    f.a = f.b = f.c = f.d = ''
    f.e = f.f = f.g = zero
    return f

def _build_example_row_2012():
    f = Form()
    f.a = f.b = f.c = ''
    f.d = f.e = zero
    f.f = ''
    f.g = zero
    return f


def compute(form):
    f = form

    for part in f.Part_I, f.Part_II:
        rows = part.table

        if f.form_version == '2011':
            part.total_e = sum((row.e for row in rows), zero)
            part.total_f = sum((row.f for row in rows), zero)
            part.total_g = sum((row.g for row in rows), zero)

        elif f.form_version == '2012':
            for row in rows:
                row.h = row.d - row.e + row.g

            part.total_d = sum((row.d for row in rows), zero)
            part.total_e = sum((row.e for row in rows), zero)
            part.total_g = sum((row.g for row in rows), zero)
            part.total_h = sum((row.h for row in rows), zero)


def fill_out(form, pdf):
    pdf.load('us.f8949--{}.pdf'.format(form.form_version))
    if form.form_version == '2011':
        fill_out_2011(form, pdf)
    elif form.form_version == '2012':
        fill_out_2012(form, pdf)

def fill_out_2011(form, pdf):
    f = form

    pdf['f1_001_0_[0]'] = f.name, f.name
    pdf['f1_002_0_[0]'] = f.ssn, f.ssn

    for pageno, part in [(1, f.Part_I), (2, f.Part_II)]:

        pdf.pattern = 'topmostSubform[0].Page{}[0].c{}_0{}_0_[0]'

        for n, letter in enumerate('ABC', 1):
            value = letter if part.box == letter else 'Off'
            pdf[pageno, pageno, n] = value

        pdf.pattern = 'f{}_{:03}_0_[0]'

        i = 14
        j = 226
        for row in part.table:

            if i <= 176:
                pdf[pageno, i+0] = row.a
                pdf[pageno, j] = row.b
                pdf[pageno, i+1] = row.c
                pdf[pageno, i+2] = row.d
                pdf[pageno, i+3] = zstr(row.e)
                pdf[pageno, i+5] = zstr(row.f)
                pdf[pageno, i+7] = zstr(row.g)
            else:
                pdf[pageno, i+0] = row.a
                pdf[pageno, i+1] = row.b
                pdf[pageno, i+2] = row.c
                pdf[pageno, i+3] = row.d
                pdf[pageno, i+4] = zstr(row.e)
                pdf[pageno, i+6] = zstr(row.f)
                pdf[pageno, i+8] = zstr(row.g)

            if i < 176:
                i += 9
            elif i == 176:
                i = 245
            else:
                i += 10

            j += 1

    pdf.pattern = '{}'

    pdf['f1_500_'] = zstr(f.Part_I.total_e)
    pdf['f1_476_'] = zstr(f.Part_I.total_f)
    pdf['f1_502_'] = zstr(f.Part_I.total_g)

    pdf['f2_500_'] = zstr(f.Part_II.total_e)
    pdf['f2_476_'] = zstr(f.Part_II.total_f)
    pdf['f2_502_'] = zstr(f.Part_II.total_g)

def fill_out_2012(form, pdf):
    f = form

    pdf['f1_001_0_[0]'] = f.name, f.name
    pdf['f1_002_0_[0]'] = f.ssn, f.ssn

    for pageno, part in [(1, f.Part_I), (2, f.Part_II)]:

        pdf.pattern = 'topmostSubform[0].Page{}[0].c1_0{}_0_[{}]'

        for n, letter in enumerate('ABC'):
            value = letter if part.box == letter else 'Off'
            pdf[pageno, pageno, n] = value

        pdf.pattern = 'f{}_{}[0]'

        n = 1
        for row in part.table:
            pdf[pageno, n + 0] = row.a
            pdf[pageno, n + 1] = row.b
            pdf[pageno, n + 2] = row.c
            pdf[pageno, n + 3] = zstr(row.d)
            pdf[pageno, n + 4] = zstr(row.e)
            pdf[pageno, n + 5] = row.f
            pdf[pageno, n + 6] = zstr(row.g)
            pdf[pageno, n + 7] = zstr(row.h)
            n += 10

    pdf.pattern = '{}'

    pdf['f1_159['] = zstr(f.Part_I.total_d)
    pdf['f1_160['] = zstr(f.Part_I.total_e)
    pdf['f1_161['] = zstr(f.Part_I.total_g)
    pdf['f1_162['] = zstr(f.Part_I.total_h)

    pdf['f2_167['] = zstr(f.Part_II.total_d)
    pdf['f2_168['] = zstr(f.Part_II.total_e)
    pdf['f2_169['] = zstr(f.Part_II.total_g)
    pdf['f2_170['] = zstr(f.Part_II.total_h)
