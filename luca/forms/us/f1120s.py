from decimal import Decimal
from luca.kit import cents, validate, zero, zzstr


def defaults(form):
    f = form

    f.year = 2012
    f.ein = ''
    f.name = ''
    f.street = ''
    f.city_state_zip = ''

    f.A = f.B = f.E = ''
    f.C = False
    f.F = zero
    f.G = False
    f.H = 1
    f.I = 1

    f.line1a = f.line1b = f.line2 = f.line4 = f.line5 = zero
    for n in range(7, 20):
        setattr(f, 'line{}'.format(n), zero)
    f.line22a = f.line22b = f.line23a = f.line23b = f.line23c = zero
    f.line24 = zero
    f.line27_credited = zero

    f.signer_title = ''
    f.discuss = False

    f.B = Form()
    f.B.line1 = 'a'
    f.B.line2a = ''
    f.B.line2b = ''
    f.B.line3 = False
    # TODO: tables beneath line 4a and line4b
    f.B.line4a = []
    f.B.line4b = []
    f.B.line5ai = 0
    f.B.line5aii = 0
    f.B.line5bi = 0
    f.B.line5bii = 0
    f.B.line6 = False
    f.B.line7 = False
    f.B.line8 = zero
    f.B.line9 = zero
    f.B.line10 = True
    f.B.line11 = zero
    f.B.line12 = False
    f.B.line13a = False
    f.B.line13b = False

    f.K = Form()
    f.K.line1 = f.K.line2 = zero
    f.K.line3a = f.K.line3b = zero
    f.K.line4 = f.K.line5a = f.K.line5c = f.K.line6 = f.K.line7 = zero
    f.K.line8a = f.K.line8b = f.K.line8c = f.K.line9 = f.K.line10 = zero
    f.K.line11 = f.K.line12a = f.K.line12b = f.K.line12c = f.K.line12d = zero
    f.K.line12c_type = ''
    f.K.line13a = f.K.line13b = f.K.line13c = f.K.line13d = zero
    f.K.line13e = f.K.line13f = f.K.line13g = zero
    f.K.line13d_type = ''
    f.K.line13e_type = ''
    f.K.line13g_type = ''
    for i in range(ord('a'), ord('n') + 1):
        setattr(f.K, 'line14' + chr(i), zero)
    for i in range(ord('a'), ord('f') + 1):
        setattr(f.K, 'line15' + chr(i), zero)
    for i in range(ord('a'), ord('e') + 1):
        setattr(f.K, 'line16' + chr(i), zero)
    f.K.line17a = f.K.line17b = f.K.line17c = zero
    f.K.line18 = (
        sum(getattr(f.K, 'line{}'.format(i)) for i in range(1, 10 + 1))
        - f.K.line11 - f.K.line12a - f.K.line12b - f.K.line12c
        - f.K.line12d - f.line14l
        )


def compute(form):
    f = form
    validate.year(f.year)

    f.line1c = f.line1a - f.line1b
    f.line3 = f.line1c - f.line2
    f.line6 = f.line3 + f.line4 + f.line5

    f.line21 = sum(getattr(f, 'line{}'.format(n)) for n in range(7, 20))

    f.line22c = f.line22a + f.line22b
    f.line23d = f.line23a + f.line23b + f.line23c
    owed = f.line22c + f.line24 - f.line23d
    if owed >= 0:
        f.line25 = owed
        f.line26 = zero
        f.line27 = zero
    else:
        f.line25 = zero
        f.line26 = -owed
        f.line27 = -owed - f.line27_credited

    f.K.line3c = f.K.line3a - f.K.line3b
    
