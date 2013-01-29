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
    canvas.setFont('Helvetica', 12)

    def put(x, y, value):
        if isinstance(value, Decimal):
            dollars, cents = str(value).split('.')
            canvas.drawString(x - 6 - canvas.stringWidth(dollars), y, dollars)
            canvas.drawString(x + 4, y, cents)
        else:
            value = unicode(value)
            canvas.drawString(x, y, value)

    put(140, 688, f.name)

    digits = [ c for c in f.ein if c.isdigit() ]
    for i, digit in enumerate(digits[:2]):
        put(158 + 26.5 * i, 713, digit)
    for i, digit in enumerate(digits[2:]):
        put(223 + 25.5 * i, 713, digit)

    put(82, 641, f.address)
    put(82, 614, f.city)
    put(282, 614, f.state)
    put(320, 614, f.zip)

    step = (683.25 - 648.75) / 2
    origin = 683.25 + step
    for i in range(1, 5):
        put(418.5, origin - i * step, 'X' if f.quarter == i else '')

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

    put(117.5, 662, f.line18a)

    put(65.75, 317.25, f.part4_no)

    put(434, 251, f.sign_name)
    put(434, 227, f.sign_title)
    put(464, 196, f.sign_phone)

    canvas.showPage()
