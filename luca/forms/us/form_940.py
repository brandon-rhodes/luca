from decimal import Decimal
from itertools import groupby

from publican.engine.kit import Date, cents, years_range, zero

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


grids = {
 1: """
  ein-
  name-
  x x line3
  x line5
  x x line6
  x x line7a
  x line7b line7c
  x line7d line7e
  x x line8
  x x line11
  x x line12
  x x line14
  """,
 }

stride = 24

pdf_fields = [
 (140,688, 'name'),
 (156,713, 'ein', 24),
 (552,472, 'line3'),
 (406,400, 'line5'),
 (552,288 + 4 * stride, 'line6'),
 (552,288 + 3 * stride, 'line7a'),
 (364,288 + 2 * stride, 'line7b'), (552,288 + 2 * stride, 'line7c'),
 (364,288 + stride, 'line7d'), (552,288 + stride, 'line7e'),
 (552,288, 'line8'),
 (552,192, 'line11'),
 (552,156, 'line12'),
 (552,92, 'line14'),
 ]
