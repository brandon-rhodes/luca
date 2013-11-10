from decimal import Decimal
from luca.kit import cents

sevenk = Decimal('7000.00')
eighthpercent = Decimal('.008')
sixthpercent = Decimal('.006')

title = u"Form 940: Employer's Annual Federal Unemployment (FUTA) Tax Return"
versions = u'2012',


def compute(form):
    f = form
    f.line6 = f.line5
    f.line7 = f.line3 - f.line6
    f.line8 = cents(f.line7 * Decimal('0.006'))

    if f.all_wages_excluded_from_state_unemployment_tax:
        f.line9 = cents(f.line7 * Decimal('.054'))
    else:
        f.line9 = Decimal('0.00')

    f.line12 = f.line8 + f.line9 + f.line10 + f.line11

    if f.line12 > f.line13:
        f.line14 = f.line12 - f.line13
        f.line15 = ''
    else:
        f.line14 = ''
        f.line15 = f.line13 - f.line12

    if f.line12 > Decimal('500.00'):
        f.line17 = f.line16a + f.line16b + f.line16c + f.line16d
        assert f.line12 == f.line17
    else:
        f.line16a = f.line16b = f.line16c = f.line16d = ''
        f.line17 = ''


def fill_out(form, pdf):
    f = form

    pdf.load('us.f940--{}.pdf'.format(f.form_version))
    pdf.pages = 1, 2

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
