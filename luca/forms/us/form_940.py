from decimal import Decimal
from itertools import groupby

from luca.kit import cents

sevenk = Decimal('7000.00')
eighthpercent = Decimal('.008')
sixthpercent = Decimal('.006')

title = u"Employer's Annual Federal Unemployment (FUTA) Tax Return"
filename = 'f940--2011.pdf'

def periods(company):
    return list(years_range(company.incorporation_date, company.today))


def tally(company, period, filing):

    tlist = list(company.transactions(
        within=period,
        debit_type='business',
        credit_type='employee',
        ))
    wages = sum(t.amount for t in tlist)

    p = filing.new_page(1)

    p.ein = company.ein
    p.name = company.name

    p.line3 = wages

    get_employee_id = lambda t: t.credit_account.id
    tlist.sort(key=get_employee_id)
    p.line5 = cents(sum(max(0, sum(t.amount for t in sublist) - sevenk)
                        for k, sublist in groupby(tlist, get_employee_id)))

    p.line6 = p.line5
    p.line7a = p.line3 - p.line6

    p.line7b = sevenk  # TODO
    p.line7d = zero     # TODO

    p.line7c = cents(p.line7b * eighthpercent)
    p.line7e = cents(p.line7d * sixthpercent)

    p.line8 = p.line7c + p.line7e
    p.line11 = zero     # TODO
    p.line12 = p.line8 + p.line11
    p.line14 = p.line12

    # TODO: page 2

    filing.balance_due = p.line14
    filing.due_date = Date(period.end.year + 1, 1, 31).next_business_day()

    return filing


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

    f.line17 = f.line16a + f.line16b + f.line16c + f.line16d

    assert f.line12 == f.line17


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

    digits = [ c for c in f.ein if c.isdigit() ]
    for i, digit in enumerate(digits[:2]):
        put(158 + 26.5 * i, 713, digit)
    for i, digit in enumerate(digits[2:]):
        put(223 + 25.5 * i, 713, digit)

    put(140, 688, f.name)
    put(82, 641, f.address)
    put(82, 614, f.city)
    put(282, 614, f.state)
    put(320, 614, f.zip)

    put(460, 557, f.line1a[0])
    put(496, 557, f.line1a[1])

    stride = 24

    put(552, 472, f.line3)
    #line4?
    put(406, 400, f.line5),
    put(552, 286 + 4 * stride, f.line6)
    put(552, 286 + 3 * stride, f.line7)
    put(552, 288 + 2 * stride, f.line8)

    if f.line9:
        put(552, 293, f.line9)

    # TODO: line10
    # TODO: line11

    put(552, 205, f.line12)
    put(552, 205 - stride, f.line13)

    put(552, 142, f.line14)
    put(552, 142 - stride, f.line15)

    canvas.showPage()

    put(36, 725, f.name)
    put(400, 725, f.ein)

    put(442, 659, f.line16a)
    put(442, 659 - 1 * stride, f.line16b)
    put(442, 659 - 2 * stride, f.line16c)
    put(442, 659 - 3 * stride, f.line16d)
    put(442, 659 - 4 * stride, f.line17)

    put(58.5, 451.5, f.part6_no)

    put(386, 365, f.sign_name)
    put(386, 365 - 1 * stride, f.sign_title)
    put(428, 365 - 2 * stride, f.sign_phone)

    canvas.showPage()
