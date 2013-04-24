from decimal import Decimal
from luca.kit import cents, zero


def defaults(form):
    f = form
    f.name = ''
    f.ein = ''
    f.line1 = 0
    f.line2 = zero
    f.line3 = zero
    f.line5a1 = f.line5b1 = f.line5c1 = zero
    f.line5e = zero
    f.line7 = zero
    f.line8 = zero
    f.line9 = zero
    f.line11 = zero
    f.line12a = zero
    f.line12b = 0
    f.line16 = 1
    f.Part_4 = False
    f.signer_name = ''
    f.signer_title = ''
    f.signer_phone = ''
    f.signing_date = ''


def compute(form):
    f = form
    f.line4 = not (f.line5a1 or f.line5b1 or f.line5c1)
    f.line5a2 = cents(f.line5a1 * Decimal('0.104'))
    f.line5b2 = cents(f.line5b1 * Decimal('0.104'))
    f.line5c2 = cents(f.line5c1 * Decimal('0.029'))
    f.line5d = f.line5a2 + f.line5b2 + f.line5c2
    f.line6 = f.line3 + f.line5d + f.line5e
    f.line10 = f.line6 + f.line7 + f.line8 + f.line9
    f.line13 = f.line11 + f.line12a
    if f.line10 > f.line13:
        f.line14 = f.line10 - f.line13
        f.line15 = zero
    else:
        f.line14 = zero
        f.line15 = f.line13 - f.line10
    # TODO: refuse to let them check box 1 on line16 if they do not qualify


def draw(form, canvas):
    f = form

    def put(x, y, value):
        # Font per http://www.irs.gov/instructions/i941/ch01.html
        canvas.setFont('Courier', 10)
        if isinstance(value, Decimal):
            dollars, cents = str(value).split('.')
            canvas.drawString(x - 6 - canvas.stringWidth(dollars), y, dollars)
            canvas.drawString(x + 4, y, cents)
        else:
            value = unicode(value)
            canvas.drawString(x, y, value)


    digits = [ c for c in f.ein if c.isdigit() ]
    for i, digit in enumerate(digits[:2]):
        put(158 + 26.5 * i, 714, digit)
    for i, digit in enumerate(digits[2:]):
        put(223 + 25.5 * i, 714, digit)

    put(140, 690, f.name)
    put(82, 642, f.address)
    put(82, 615, f.city)
    put(282, 615, f.state)
    put(320, 615, f.zip)

    step = (683.25 - 648.75) / 2
    origin = 685 + step
    for i in range(1, 5):
        put(420, origin - i * step, 'X' if f.quarter == i else '')

    stride = 18

    put(552, 552, f.line1)
    put(552, 552 - stride, f.line2)
    put(552, 552 - 2 * stride, f.line3)
    put(272, 462, f.line5a1)
    put(409, 462, f.line5a2)
    put(272, 462 - stride, f.line5b1)
    put(409, 462 - stride, f.line5b2)
    put(272, 462 - 2 * stride, f.line5c1)
    put(409, 462 - 2 * stride, f.line5c2)
    put(552, 402, f.line5d)
    put(552, 402 - stride, f.line5e)
    put(552, 402 - 2 * stride, f.line6)
    put(552, 402 - 6 * stride, f.line10)
    put(552, 192, f.line14)

    canvas.showPage()

    put(36, 725, f.name)
    put(400, 725, f.ein)

    put(118, 662.5, f.line16)

    # TODO: support the checkboxes and fields in Part 3
    # TODO: support paid-preparer fields in Part 4
    put(66.5, 318.5, f.Part_4)

    put(434, 252, f.signer_name)
    put(434, 228, f.signer_title)
    put(464, 197.5, f.signer_phone)

    canvas.showPage()
