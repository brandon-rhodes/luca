from luca.kit import Decimal, cents, dsum, zero

title = u'Schedule D (Form 1040): Capital Gains and Losses'


def defaults(form):
    f = form
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

    f.line18 = f.line19 = Decimal('NaN')
    f.line22 = None


def check(form, forms, eq):
    f8949s = [f for f in forms if f.form == 'us.f8949']

    for i, box in enumerate('ABC', 1):
        these = [f for f in f8949s if f.Part_I.box == box]
        for letter in 'degh':
            line = 'line2{}'.format(letter)
            n = dsum(getattr(f.Part_I, line) for f in these)
            eq('line{}{}'.format(i, letter), n)

    for i, box in enumerate('ABC', 8):
        these = [f for f in f8949s if f.Part_I.box == box]
        for letter in 'degh':
            line = 'line2{}'.format(letter)
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
    f.line17 = f.line15 >= 0 and f.line16 >= 0

    if f.line17:
        # TODO: need a pretty error message if line18 or line19 has not
        # been filled out.
        f.line20 = (f.line18 == zero) and (f.line19 == zero)

    # TODO: is line 21 never computed?
    f.line21 = zero


def fill(form, fields):
    f = form
    page = 1

    def put(n, value):
        fields['f%d_%03d[' % (page, n)] = z(value)

    fields['f1_001['] = f.name
    fields['f1_002['] = f.ssn

    # Part I: Short-Term Capital Gains and Losses

    n = 3
    for line in 1, 2, 3:
        for letter in 'degh':
            value = getattr(f, 'line{}{}'.format(line, letter))
            put(n, value)
            n += 1

    for line in 4, 5, 6, 7:
        value = getattr(f, 'line{}'.format(line))
        put(n, value)
        n += 1

    # Part II: Long-Term Capital Gains and Losses

    for line in 8, 9, 10:
        for letter in 'degh':
            value = getattr(f, 'line{}{}'.format(line, letter))
            put(n, value)
            n += 1

    for line in 11, 12, 13, 14, 15:
        value = getattr(f, 'line{}'.format(line))
        put(n, value)
        n += 1

    # Part III: Summary

    page = 2

    put(1, f.line16)
    fields['.c2_01_0_[0]'] = 'Yes' if f.line17 is True else 'Off'
    fields['.c2_01_0_[1]'] = 'No' if f.line17 is False else 'Off'
    put(2, f.line18)
    put(3, f.line19)
    fields['.c2_02_0_[0]'] = 'Yes' if f.line20 is True else 'Off'
    fields['.c2_02_0_[1]'] = 'No' if f.line20 is False else 'Off'
    put(5, f.line21)
    fields['.c2_03_0_[0]'] = 'Yes' if f.line22 is True else 'Off'
    fields['.c2_03_0_[1]'] = 'No' if f.line22 is False else 'Off'


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
