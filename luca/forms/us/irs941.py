from decimal import Decimal
from luca.kit import cents

filename = 'f941.pdf'

Decimal('7.325').quantize

def compute(form):
    f = form
    f.line5a1 = f.line2
    f.line5c1 = f.line2
    f.line5a2 = cents(f.line5a1 * Decimal(0.104))
    f.line5b2 = cents(f.line5b1 * Decimal(0.104))
    f.line5c2 = cents(f.line5c1 * Decimal(0.029))
    f.line5d = cents(f.line5a2 + f.line5c2) # + f.line5b2
    f.line6 = cents(f.line3 + f.line5d) #+ f.line5e
    f.line10 = cents(f.line6)
    f.line14 = cents(f.line10) # - f.line13

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

    put(118, 662.5, f.line16a)

    put(66.5, 318.5, f.part4_no)

    put(434, 252, f.sign_name)
    put(434, 228, f.sign_title)
    put(464, 197.5, f.sign_phone)

    canvas.showPage()
