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
