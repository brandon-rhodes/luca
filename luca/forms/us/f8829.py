from luca.kit import Decimal, cents, zero, zstr, zzstr, ROUND_HALF_UP

title = u'Form 8829: Expenses for Business Use of Your Home'
versions = u'2012',
hundred = Decimal('100')

def defaults(form):
    f = form
    f.name = u''
    f.ssn = u''
    f.line1 = 100
    f.line2 = 1000
    # TODO: daycare computations in lines 4-6
    f.line8 = zero
    for n in range(9, 12) + range(16, 22):
        for letter in 'ab':
            f['line', n, letter] = zero
    f.line24 = zero
    f.line28 = zero
    f.line30 = zero
    f.line36 = zero
    f.line37 = zero
    f.line40 = 0

def compute(form):
    f = form
    f.line3 = (cents(f.line1) / cents(f.line2)
               ).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    f.line7 = f.line3

    f.line12a = sum(f['line', n, 'a'] for n in range(9, 12))
    f.line12b = sum(f['line', n, 'b'] for n in range(9, 12))
    f.line13 = cents(f.line12b * f.line7 / hundred)
    f.line14 = f.line12a + f.line13

    f.line15 = max(zero, f.line8 - f.line14)

    f.line22a = sum(f['line', n, 'a'] for n in range(16, 22))
    f.line22b = sum(f['line', n, 'b'] for n in range(16, 22))
    f.line23 = cents(f.line22b * f.line7)
    f.line25 = f.line22a + f.line23 + f.line24

    f.line38 = f.line36 - f.line37
    f.line39 = cents(f.line38 * f.line7)
    f.line41 = cents(f.line39 * f.line40)

    f.line26 = min(f.line15, f.line25)
    f.line27 = f.line15 - f.line26
    f.line29 = f.line41
    f.line31 = f.line28 + f.line29 + f.line30
    f.line32 = min(f.line27, f.line31)
    f.line33 = f.line14 + f.line26 + f.line32
    # TODO: f.line34 should really involve casualty loss plus another form!
    f.line34 = zero
    f.line35 = f.line33 - f.line34

    f.line42 = max(zero, f.line25 - f.line26)
    f.line43 = max(zero, f.line31 - f.line32)

def check(form, forms, eq):
    matches = forms['us.f1040sc']
    if matches:
        c = matches[0]
        eq('line8', c.line29)

def fill_out(form, pdf):
    f = form
    pdf.load('us.f8829--{}.pdf'.format(f.form_version))

    pdf.pattern = 'p1-t{}[0]'

    pdf[1] = f.name
    pdf[2] = f.ssn

    pdf[5] = zstr(f.line1)
    pdf[6] = zstr(f.line2)
    pdf[7] = zstr(f.line3 * hundred).rstrip(u'0 ')
    # pdf[8] = zstr(f.line4)
    # pdf[9] = zstr(f.line6)
    pdf[10] = zstr(f.line7 * hundred).rstrip(u'0 ')

    n = 11
    for seq in (
          [[8]] + [ab(i) for i in range(9, 13)] + [[13, 14, 15]]
          + [ab(i) for i in range(16, 23)] + [range(23, 40)]
          ):
        for i in seq:
            pdf[n], pdf[n+1] = zzstr(f['line', i])
            n += 2

    pdf[97] = zstr(f.line40 * hundred).rstrip(u'0 ')
    pdf[98], pdf[99] = zzstr(f.line41)
    pdf[100], pdf[101] = zzstr(f.line42)
    pdf[102], pdf[103] = zzstr(f.line43)

def ab(n):
    ns = str(n)
    return [ns + 'a', ns + 'b']
