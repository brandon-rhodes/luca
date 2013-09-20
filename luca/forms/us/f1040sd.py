from luca.kit import Decimal, dsum, zero, zstr

title = u'Schedule D (Form 1040): Capital Gains and Losses'


def defaults(form):
    f = form
    f.form_version = '2012'
    f.name = ''
    f.ssn = ''

    # Part I: Short-Term Capital Gains and Losses
    # Part II: Long-Term Capital Gains and Losses

    for line in 1, 2, 3:
        for letter in 'deg':
            setattr(f, 'line{}{}'.format(line, letter), zero)

    f.line4 = f.line5 = f.line6 = zero

    for line in 8, 9, 10:
        for letter in 'deg':
            setattr(f, 'line{}{}'.format(line, letter), zero)

    f.line11 = f.line12 = f.line13 = f.line14 = zero

    # Part III: Summary

    f.line18 = f.line19 = zero
    f.line22 = None


def check(form, forms, eq):
    f8949s = forms['us.f8949']
    if not f8949s:
        return

    for i, box in enumerate('ABC', 1):
        these = [f for f in f8949s if f.Part_I.box == box]
        for letter in 'degh':
            line = 'total_{}'.format(letter)
            n = dsum(getattr(f.Part_I, line) for f in these)
            eq('line{}{}'.format(i, letter), n)

    for i, box in enumerate('ABC', 8):
        these = [f for f in f8949s if f.Part_I.box == box]
        for letter in 'degh':
            line = 'total_{}'.format(letter)
            n = dsum(getattr(f.Part_II, line) for f in these)
            eq('line{}{}'.format(i, letter), n)


def compute(form):
    f = form

    # Part I: Short-Term Capital Gains and Losses
    # Part II: Long-Term Capital Gains and Losses

    for line in 1, 2, 3, 8, 9, 10:
        d = getattr(f, 'line{}d'.format(line))
        e = getattr(f, 'line{}e'.format(line))
        g = getattr(f, 'line{}g'.format(line))
        setattr(f, 'line{}h'.format(line), d - e + g)

    f.line7 = f.line1h + f.line2h + f.line3h + f.line4 + f.line5 + f.line6
    f.line15 = (f.line8h + f.line9h + f.line10h
              + f.line11 + f.line12 + f.line13 + f.line14)

    # Part III: Summary

    f.line16 = f.line7 + f.line15

    if f.line16 > zero:
        f.line17 = f.line15 >= zero and f.line16 >= zero
        if f.line17:
            # TODO: need a pretty error message if line18 or line19 has not
            # been filled out.
            f.line20 = (not f.line18) and (not f.line19)
        else:
            f.line20 = None
    elif f.line16 < zero:
        f.line17 = None
        f.line20 = None
        f.line21 = min(- f.line16, Decimal('3000.00'))


def fill_out(form, pdf):
    f = form
    pdf.load('us.f1040sd--{}.pdf'.format(f.form_version))

    pdf['f1_001['] = f.name
    pdf['f1_002['] = f.ssn

    # Part I: Short-Term Capital Gains and Losses

    pdf.pattern = 'f1_{:03d}'

    n = 3
    for line in 1, 2, 3:
        for letter in 'degh':
            value = getattr(f, 'line{}{}'.format(line, letter))
            pdf[n] = zstr(value)
            n += 1

    for line in 4, 5, 6, 7:
        value = getattr(f, 'line{}'.format(line))
        pdf[n] = zstr(value)
        n += 1

    # Part II: Long-Term Capital Gains and Losses

    for line in 8, 9, 10:
        for letter in 'degh':
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
