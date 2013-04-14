from luca.kit import Decimal, cents

title = u'Schedule A (Form 1040): Itemized Deductions'
zero = cents(0)

def defaults(form):
    f = form
    f.name = ''
    f.ssn = ''

    for n in (1, 2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18,
              20, 21, 22, 23, 25, 28):
        setattr(f, 'line{}'.format(n), zero)

    f.line5_type = 'income'
    f.line8_text1 = ''
    f.line8_text2 = ''
    f.line11_text1 = ''
    f.line11_text2 = ''
    f.line21_text1 = ''
    f.line23_text1 = ''
    f.line23_text2 = ''
    f.line28_text1 = ''
    f.line28_text2 = ''
    f.line28_text3 = ''
    f.line30 = False

def compute(form):
    f = form
    f.line3 = cents(f.line2 * 75 / 1000)
    f.line4 = max(f.line1 - f.line3, zero)
    f.line9 = f.line5 + f.line6 + f.line7 + f.line8
    f.line15 = f.line10 + f.line11 +  f.line12 +  f.line13 + f.line14
    f.line19 = f.line16 + f.line17 +  f.line18
    f.line24 = f.line21 + f.line22 + f.line23
    f.line26 = cents(f.line25 * 2 / 100)
    f.line27 = max(f.line24 - f.line26, zero)
    f.line29 = (f.line4 + f.line9 + f.line15 + f.line19 + f.line20
              + f.line27 + f.line28)

def fill(form, fields):
    f = form

    def put(n, value):
        sa, sb = zz(value)
        fields['-t{}['.format(n+0)] = sa
        fields['-t{}['.format(n+1)] = sb

    fields['-t1['] = f.name
    fields['-t2['] = f.ssn

    put(5, f.line1)
    put(7, f.line2)
    put(9, f.line3)
    put(11, f.line4)

    fields['-cb1[0]'] = '1' if f.line5_type == 'income' else 'Off'
    fields['-cb1[1]'] = '2' if f.line5_type == 'sales' else 'Off'
    put(13, f.line5)
    put(15, f.line6)
    put(17, f.line7)
    fields['-t19['] = f.line8_text1
    fields['-t20['] = f.line8_text2
    put(21, f.line8)
    put(23, f.line9)

    put(25, f.line10)
    fields['-t27['] = f.line11_text1
    fields['-t28['] = f.line11_text2
    put(29, f.line11)
    put(31, f.line12)
    put(400, f.line13)
    put(35, f.line14)
    put(37, f.line15)

    put(39, f.line16)
    put(41, f.line17)
    put(43, f.line18)
    put(45, f.line19)

    put(47, f.line20)

    fields['-t51['] = f.line21_text1
    put(49, f.line21)
    put(52, f.line22)
    fields['-t54['] = f.line23_text1
    fields['-t55['] = f.line23_text2
    put(56, f.line23)
    put(58, f.line24)
    put(60, f.line25)
    put(62, f.line26)
    put(64, f.line27)

    fields['-t66['] = f.line28_text1
    fields['-t67['] = f.line28_text2
    fields['-t68['] = f.line28_text3
    put(69, f.line28)

    put(71, f.line29)
    fields['-cb5['] = 'X' if f.line30 else 'Off'

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
