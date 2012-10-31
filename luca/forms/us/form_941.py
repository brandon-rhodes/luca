
filename = 'f941.pdf'

def compute(data):
    pass

def draw(data, canvas):
    canvas.setFont('Helvetica', 12)

    def put(x, y, text):
        if '.' in text and text[-1].isdigit():
            dollars, cents = text.split('.')
            canvas.drawString(x - 6 - canvas.stringWidth(dollars), y, dollars)
            canvas.drawString(x + 4, y, cents)
        else:
            canvas.drawString(x, y, text)

    put(140, 688, data.name)

    digits = [ c for c in data.ein if c.isdigit() ]
    for i, digit in enumerate(digits[:2]):
        put(158 + 26.5 * i, 713, digit)
    for i, digit in enumerate(digits[2:]):
        put(223 + 25.5 * i, 713, digit)

    put(82, 641, data.address)
    put(82, 614, data.city)
    put(282, 614, data.state)
    put(320, 614, data.zip)

    put(418.5, 683.25, data.q1)
    put(418.5, 648.75, data.q3)

    stride = 18

    put(552, 552, data.line1)
    put(552, 552 - stride, data.line2)
    put(552, 552 - 2 * stride, data.line3)
    put(272, 462, data.line5a1)
    put(409, 462, data.line5a2)
    put(272, 462 - stride, data.line5b1)
    put(409, 462 - stride, data.line5b2)
    put(272, 462 - 2 * stride, data.line5c1)
    put(409, 462 - 2 * stride, data.line5c2)
    put(552, 402, data.line5d)
    put(552, 402 - stride, data.line5e)
    put(552, 402 - 2 * stride, data.line6)
    put(552, 402 - 6 * stride, data.line10)
    put(552, 192, data.line14)

    canvas.showPage()

    put(36, 725, data.name)
    put(400, 725, data.ein)

    put(117.5, 662, data.line18a)

    put(65.75, 317.25, data.part4_no)

    put(434, 251, data.sign_name)
    put(434, 227, data.sign_title)
    put(464, 196, data.sign_phone)

    canvas.showPage()
