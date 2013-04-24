from decimal import Decimal
from luca.kit import cents, zero, zzstr


def defaults(form):
    f = form
    f.name = u''
    f.trade_name = u''
    f.address = u''
    f.city = u''
    f.state = u''
    f.zip = u''
    f.ein = u''
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
    f.line16 = 'a'
    f.Part_4 = False
    f.signer_name = u''
    f.signer_title = u''
    f.signer_phone = u''


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


def fill(form, fields):
    f = form
    page = 1

    def name(n):
        return 'f{}_{:02}_0_[0]'.format(page, n)

    def put(n, value):
        fields[name(n)], fields[name(n + 1)] = zzstr(value)

    for i in range(9):
        fields[name(i + 1)] = f.ein.replace('-', '')[i : i+1]

    fields[name(16)] = str(f.line1 or '')
    fields[name(10)] = f.name
    fields[name(11)] = f.trade_name
    fields[name(12)] = f.address
    fields[name(13)] = f.city
    fields[name(14)] = f.state
    fields[name(15)] = f.zip

    Q = 4
    fields['c1_1_0_[0]'] = 'Report1' if Q == 1 else 'Off'
    fields['c1_1_0_[1]'] = 'Report2' if Q == 2 else 'Off'
    fields['c1_1_0_[2]'] = 'Report3' if Q == 3 else 'Off'
    fields['c1_1_0_[3]'] = 'Report4' if Q == 4 else 'Off'

    put(17, f.line2)
    put(19, f.line3)
    fields['c1_5_0_[0]'] = '1' if f.line4 else 'Off'
    put(21, f.line5a1)
    put(23, f.line5a2)
    put(25, f.line5b1)
    put(27, f.line5b2)
    put(29, f.line5c1)
    put(31, f.line5c2)
    put(33, f.line5d)
    put(60, f.line5e)
    dollars, cents = zzstr(f.line6)
    fields[name(105)] = dollars
    fields[name(36)] = cents
    put(37, f.line7)
    put(39, f.line8)
    put(41, f.line9)
    put(54, f.line10)
    put(56, f.line11)
    put(45, f.line12a)
    fields[name(47)] = str(f.line12b or '')
    put(43, f.line13)
    put(58, f.line14)
    put(64, f.line15)

    page = 2

    fields[name(75)] = f.name
    fields[name(14)] = f.ein

    fields['c2_01_0_[0]'] = 'Chck1' if f.line16 == 'a' else 'Off'

    # TODO: allow other options for Part 2
    # TODO: support Part 3
    # TODO: allow "yes" and further information for Part 4

    fields['c2_06_0_[0]'] = 'Yes' if f.Part_4 else 'Off'
    fields['c2_06_0_[1]'] = 'Off' if f.Part_4 else 'No'

    fields[name(44)] = f.signer_name
    fields[name(66)] = f.signer_title
    fields[name(48)] = f.signer_phone


def draw(form, canvas):
    canvas.showPage()
    canvas.showPage()
    return 1, 2
