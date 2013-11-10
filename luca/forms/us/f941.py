from decimal import Decimal
from luca.kit import cents, validate, zero, zzstr

title = u"Form 941: Employer's QUARTERLY Federal Tax Return"
versions = u'2012',


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
    f.line16_month1 = zero
    f.line16_month2 = zero
    f.line16_month3 = zero
    f.Part_4 = False
    f.signer_name = u''
    f.signer_title = u''
    f.signer_phone = u''


def compute(form):
    f = form
    validate.year(f.year)
    validate.quarter(f.quarter)
    f.line4 = not (f.line5a1 or f.line5b1 or f.line5c1)

    social_security_rate = Decimal('0.104' if int(f.year) < 2013 else '0.124')
    medicare_rate = Decimal('0.029')

    f.line5a2 = cents(f.line5a1 * social_security_rate)
    f.line5b2 = cents(f.line5b1 * social_security_rate)
    f.line5c2 = cents(f.line5c1 * medicare_rate)

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

    total = f.line16_month1 + f.line16_month2 + f.line16_month3
    f.line16_total = total


def fill_out(form, pdf):
    f = form

    pdf.load('us.f941--{}.pdf'.format(f.year))
    pdf.pages = 1, 2

    page = 1

    def name(n):
        return 'f{}_{:02}_0_[0]'.format(page, n)

    def pair(n, value):
        pdf[name(n)], pdf[name(n + 1)] = zzstr(value)

    for i in range(9):
        pdf[name(i + 1)] = f.ein.replace('-', '')[i : i+1]

    pdf[name(16)] = str(f.line1 or '')
    pdf[name(10)] = f.name
    pdf[name(11)] = f.trade_name
    pdf[name(12)] = f.address
    pdf[name(13)] = f.city
    pdf[name(14)] = f.state
    pdf[name(15)] = f.zip

    pdf['c1_1_0_[0]'] = 'Report1' if f.quarter == 1 else 'Off'
    pdf['c1_1_0_[1]'] = 'Report2' if f.quarter == 2 else 'Off'
    pdf['c1_1_0_[2]'] = 'Report3' if f.quarter == 3 else 'Off'
    pdf['c1_1_0_[3]'] = 'Report4' if f.quarter == 4 else 'Off'

    pair(17, f.line2)
    pair(19, f.line3)

    pdf['c1_5_0_[0]'] = '1' if f.line4 else 'Off'

    pair(21, f.line5a1)
    pair(23, f.line5a2)
    pair(25, f.line5b1)
    pair(27, f.line5b2)
    pair(29, f.line5c1)
    pair(31, f.line5c2)
    pair(33, f.line5d)
    pair(60, f.line5e)

    dollars, cents = zzstr(f.line6)
    pdf[name(105)] = dollars
    pdf[name(36)] = cents

    pair(37, f.line7)
    pair(39, f.line8)
    pair(41, f.line9)
    pair(54, f.line10)
    pair(56, f.line11)
    pair(45, f.line12a)

    pdf[name(47)] = str(f.line12b or '')

    pair(43, f.line13)
    pair(58, f.line14)
    pair(64, f.line15)

    page = 2

    pdf[name(75) if f.year < 2013 else 'd2_75_0_[0]'] = f.name
    pdf[name(14)] = f.ein

    pdf['c2_01_0_[0]'] = 'Chck1' if f.line16 == 'a' else 'Off'
    pdf['c2_01_0_[1]'] = 'Chck2' if f.line16 == 'b' else 'Off'
    pdf['c2_01_0_[2]'] = 'Chck3' if f.line16 == 'c' else 'Off'

    pdf.pattern = '.f2_{:02}_0_[0]'
    pdf[3], pdf[4] = zzstr(f.line16_month1)
    pdf[5], pdf[6] = zzstr(f.line16_month2)
    pdf[7], pdf[8] = zzstr(f.line16_month3)
    pdf[9], pdf[10] = zzstr(f.line16_total)

    # TODO: support Part 3
    # TODO: allow "yes" and further information for Part 4

    pdf.pattern = '{}'

    pdf['c2_06_0_[0]'] = 'Yes' if f.Part_4 else 'Off'
    pdf['c2_06_0_[1]'] = 'Off' if f.Part_4 else 'No'

    pdf[name(44)] = f.signer_name
    pdf[name(66)] = f.signer_title
    pdf[name(48)] = f.signer_phone
