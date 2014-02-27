from decimal import Decimal
from luca.kit import cents, zero, zzstr

sevenk = Decimal('7000.00')
eighthpercent = Decimal('.008')
sixthpercent = Decimal('.006')

title = u"Form 940: Employer's Annual Federal Unemployment (FUTA) Tax Return"
versions = u'2012', u'2013'


def defaults(form):
    f = form
    f.ein = ''
    f.name = ''
    f.trade_name = ''
    f.address = ''
    f.city = ''
    f.state = ''
    f.zip = ''
    f.line1a = '  '
    f.line3 = zero
    f.line4 = zero
    f.line4a = False
    f.line4b = False
    f.line4c = False
    f.line4d = False
    f.line4e = False
    f.line5 = zero
    f.all_wages_excluded_from_state_unemployment_tax = False
    f.line10 = zero
    f.line11 = zero
    f.line13 = zero
    f.line16a = zero
    f.line16b = zero
    f.line16c = zero
    f.line16d = zero
    f.part6 = False
    f.sign_name = ''
    f.sign_title = ''
    f.sign_phone = ''


def compute(form):
    f = form
    f.line6 = f.line4 + f.line5
    f.line7 = f.line3 - f.line6
    f.line8 = cents(f.line7 * Decimal('0.006'))

    if f.all_wages_excluded_from_state_unemployment_tax:
        f.line9 = cents(f.line7 * Decimal('.054'))
    else:
        f.line9 = Decimal('0.00')

    f.line12 = f.line8 + f.line9 + f.line10 + f.line11

    if f.line12 > f.line13:
        f.line14 = f.line12 - f.line13
        f.line15 = zero
    else:
        f.line14 = zero
        f.line15 = f.line13 - f.line12

    if f.line12 > cents('500.00'):
        f.line17 = f.line16a + f.line16b + f.line16c + f.line16d
        # Make this a warning?  assert f.line12 == f.line17
    else:
        f.line16a = f.line16b = f.line16c = f.line16d = ''
        f.line17 = zero


def fill_out(form, pdf):
    f = form

    pdf.load('us.f940--{}.pdf'.format(f.form_version))
    pdf.pages = 1, 2

    if form.form_version == '2012':
        return _old_2012_fill_out(f, pdf)

    pdf.pattern = 'topmostSubform[0].Page1[0].EntityArea[0].Text3{}[0]'
    for letter, digit in zip(' abcdefgh', f.ein.replace('-', '')):
        pdf[letter.strip()] = digit

    pdf.pattern = 'topmostSubform[0].Page1[0].EntityArea[0].Text{}[0]'
    pdf[5] = f.name
    pdf[6] = f.trade_name
    pdf[7] = f.address
    pdf[8] = f.city
    pdf[9] = f.state
    pdf[10] = f.zip
    # TODO: Foreign address

    pdf.pattern = 'topmostSubform[0].Page1[0].#subform[{}].Check_Box{}[0]'
    pdf[5, 23] = '1' if f.line4a else 'Off'
    pdf[5, 24] = '1' if f.line4b else 'Off'
    pdf[6, 25] = '1' if f.line4c else 'Off'
    pdf[6, 26] = '1' if f.line4d else 'Off'
    pdf.pattern = 'topmostSubform[0].Page1[0].Check_Box{}[0]'
    pdf[23] = '1' if f.line4e else 'Off'

    pdf.pattern = 'topmostSubform[0].Page1[0].Text{}[0]'
    pdf[16] = f.line1a[0]
    pdf[17] = f.line1a[1]
    # TODO: check marks on lines 1b and 2

    pdf['21'], pdf['21a'] = zzstr(f.line3)
    pdf['22'], pdf['22a'] = zzstr(f.line4)
    # TODO: check boxes on line 4
    pdf['28'], pdf['28a'] = zzstr(f.line5)
    pdf['29'], pdf['29a'] = zzstr(f.line6)
    pdf['500'], pdf['500a'] = zzstr(f.line7)
    pdf['31'], pdf['31a'] = zzstr(f.line8)

    pdf['32'], pdf['32a'] = zzstr(f.line9)
    pdf['33'], pdf['33a'] = zzstr(f.line10)
    pdf['34'], pdf['34a'] = zzstr(f.line11)

    pdf['35'], pdf['35a'] = zzstr(f.line12)
    pdf['36'], pdf['36a'] = zzstr(f.line13)
    pdf['37'], pdf['37a'] = zzstr(f.line14)
    pdf['38'], pdf['38a'] = zzstr(f.line15)

    # TODO: Part 5
    # TODO: Part 6 designee

    pdf.pattern = 'topmostSubform[0].Page2[0].p2-cb1[{}]'
    pdf[1] = 'Off' if f.part6 else '2'

    pdf.pattern = 'topmostSubform[0].Page2[0].Text{}[0]'
    pdf['59'] = f.sign_name
    pdf['61'] = f.sign_title
    pdf['64'] = f.sign_phone


def _old_2012_fill_out(f, pdf):
    canvas = pdf.get_canvas(1)
    canvas.setFont('Helvetica', 12)

    def put(x, y, value):
        # Font per http://www.irs.gov/instructions/i940/ch01.html
        canvas.setFont('Courier', 12)
        if isinstance(value, Decimal):
            dollars, cents = str(value).split('.')
            canvas.drawString(x - 6 - canvas.stringWidth(dollars), y, dollars)
            canvas.drawString(x + 4, y, cents)
        else:
            value = unicode(value)
            canvas.drawString(x, y, value)

    digits = [ c for c in f.ein if c.isdigit() ]
    for i, digit in enumerate(digits[:2]):
        put(158 + 26.5 * i, 713, digit)
    for i, digit in enumerate(digits[2:]):
        put(223 + 25.5 * i, 713, digit)

    put(140, 689, f.name)
    put(82, 641, f.address)
    put(82, 614, f.city)
    put(282, 614, f.state)
    put(320, 614, f.zip)

    put(460, 557, f.line1a[0])
    put(496, 557, f.line1a[1])

    stride = 24

    put(551, 472, f.line3)
    #line4?
    put(406, 400, f.line5),
    put(551, 286 + 4 * stride, f.line6)
    put(551, 286 + 3 * stride, f.line7)
    put(551, 288 + 2 * stride, f.line8)

    if f.line9:
        put(551, 293, f.line9)

    # TODO: line10
    # TODO: line11

    put(551, 205, f.line12)
    put(551, 205 - stride, f.line13)

    put(551, 142, f.line14)
    put(551, 142 - stride, f.line15)

    canvas = pdf.get_canvas(2)

    put(36, 725, f.name)
    put(400, 725, f.ein)

    put(442, 659, f.line16a)
    put(442, 659 - 1 * stride, f.line16b)
    put(442, 659 - 2 * stride, f.line16c)
    put(442, 659 - 3 * stride, f.line16d)
    put(442, 659 - 4 * stride, f.line17)

    put(59, 452, f.part6_no)

    put(386, 365, f.sign_name)
    put(386, 365 - 1 * stride, f.sign_title)
    put(428, 365 - 2 * stride, f.sign_phone)
