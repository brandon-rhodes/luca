from luca.forms.formlib import Form
from luca.kit import Decimal, dsum, zero, zstr

title = u'Form 1040 Schedule D: Capital Gains and Losses'
versions = u'2011', u'2012'

def defaults(form):
    f = form
    f.name = ''
    f.ssn = ''

    f.carryover_worksheet = Form()

    cw = f.carryover_worksheet
    cw.previous_f1040_line41 = zero
    cw.previous_f1040sd_line7 = zero
    cw.previous_f1040sd_line15 = zero
    cw.previous_f1040sd_line21 = zero

    # Part I: Short-Term Capital Gains and Losses
    # Part II: Long-Term Capital Gains and Losses

    letters = 'efg' if f.form_version < '2012' else 'deg'

    for line in 1, 2, 3:
        for letter in letters:
            setattr(f, 'line{}{}'.format(line, letter), zero)

    f.line4 = f.line5 = zero

    for line in 8, 9, 10:
        for letter in letters:
            setattr(f, 'line{}{}'.format(line, letter), zero)

    f.line11 = f.line12 = f.line13 = zero

    # Part III: Summary

    f.line18 = f.line19 = zero
    f.line22 = None


def check(form, forms, eq):
    f8949s = forms['us.f8949']
    if not f8949s:
        return

    letters = 'efg' if form.form_version < '2012' else 'degh'

    for i, box in enumerate('ABC', 1):
        these = [f for f in f8949s if f.Part_I.box == box]
        for letter in letters:
            line = 'total_{}'.format(letter)
            n = dsum(getattr(f.Part_I, line) for f in these)
            eq('line{}{}'.format(i, letter), n)

    for i, box in enumerate('ABC', 8):
        these = [f for f in f8949s if f.Part_I.box == box]
        for letter in letters:
            line = 'total_{}'.format(letter)
            n = dsum(getattr(f.Part_II, line) for f in these)
            eq('line{}{}'.format(i, letter), n)


def compute(form):
    f = form

    cw = f.carryover_worksheet
    cw.line1 = cw.previous_f1040_line41
    cw.line2 = max(zero, - cw.previous_f1040sd_line21)
    cw.line3 = max(zero, cw.line1 + cw.line2)
    cw.line4 = min(cw.line2, cw.line3)
    cw.line5 = max(zero, - cw.previous_f1040sd_line7)
    cw.line6 = max(zero, cw.previous_f1040sd_line15)
    cw.line7 = cw.line4 + cw.line6
    cw.line8 = max(zero, cw.line5 - cw.line7)
    cw.line9 = max(zero, - cw.previous_f1040sd_line15)
    cw.line10 = max(zero, cw.previous_f1040sd_line7)
    cw.line11 = max(zero, cw.line4 - cw.line5)
    cw.line12 = cw.line10 + cw.line11
    cw.line13 = max(zero, cw.line9 - cw.line12)

    # Part I: Short-Term Capital Gains and Losses
    # Part II: Long-Term Capital Gains and Losses

    letters = 'efg' if f.form_version < u'2012' else 'deg'

    for line in 1, 2, 3, 8, 9, 10:
        setattr(f, 'line{}h'.format(line),
            getattr(f, 'line{}{}'.format(line, letters[0]))
            - getattr(f, 'line{}{}'.format(line, letters[1]))
            + getattr(f, 'line{}{}'.format(line, letters[2]))
            )

    if not hasattr(f, 'line6'):
        f.line6 = cw.line8
    f.line7 = f.line1h + f.line2h + f.line3h + f.line4 + f.line5 - f.line6
    if not hasattr(f, 'line14'):
        f.line14 = cw.line13
    f.line15 = (f.line8h + f.line9h + f.line10h
              + f.line11 + f.line12 + f.line13 - f.line14)

    # Part III: Summary

    f.line16 = f.line7 + f.line15

    if f.line16 >= zero:
        f.line17 = f.line15 >= zero and f.line16 >= zero
        if f.line17:
            # TODO: need a pretty error message if line18 or line19 has not
            # been filled out.
            f.line20 = (not f.line18) and (not f.line19)
        else:
            f.line20 = None
        f.line21 = zero
    elif f.line16 < zero:
        f.line17 = None
        f.line20 = None
        f.line21 = min(- f.line16, Decimal('3000.00'))


def fill_out(form, pdf):
    f = form
    pdf.load('us.f1040sd--{}.pdf'.format(f.form_version))

    pdf['f1_001['] = f.name
    pdf['f1_002['] = f.ssn

    letters = 'efgh' if f.form_version < u'2012' else 'degh'

    # Part I: Short-Term Capital Gains and Losses

    pdf.pattern = 'f1_{:03d}'

    n = 3
    for line in 1, 2, 3:
        for letter in letters:
            value = getattr(f, 'line{}{}'.format(line, letter))
            pdf[n] = zstr(value)
            n += 1

    for line in 4, 5, 6, 7:
        value = getattr(f, 'line{}'.format(line))
        pdf[n] = zstr(value)
        n += 1

    # Part II: Long-Term Capital Gains and Losses

    for line in 8, 9, 10:
        for letter in letters:
            value = getattr(f, 'line{}{}'.format(line, letter))
            pdf[n] = zstr(value)
            n += 1

    for line in 11, 12, 13, 14, 15:
        value = getattr(f, 'line{}'.format(line))
        pdf[n] = zstr(value)
        n += 1

    # Part III: Summary

    pdf.pattern = 'f2_{:03d}'

    pdf[1] = zstr(f.line16)
    pdf[2] = zstr(f.line18)
    pdf[3] = zstr(f.line19)
    pdf[5] = zstr(f.line21)

    pdf.pattern = '.c2_0{}_'

    pdf[1] = yesno(f.line17)
    pdf[2] = yesno(f.line20)
    pdf[3] = yesno(f.line22)


# General-purpose functions that will probably be factored out of here:

def yesno(value):
    if value is None:
        return ('Off', 'Off')
    return ('Yes' if value else 'Off',
            'Off' if value else 'No')
