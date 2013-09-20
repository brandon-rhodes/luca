from luca.kit import Decimal, dsum, zero, zzstr

title = u'Form 1040: U.S. Individual Income Tax Return'
versions = u'2012',

filing_statuses = 'S MJ MS HoH QW'.split()

def lines(seq):
    if isinstance(seq, str):
        seq = seq.split()
    return ['line{}'.format(suffix) for suffix in seq]

income_lines = lines('7 8a 8b 9a 9b 10 11 12 13 14 15a 15b '
                     '16a 16b 17 18 19 20a 20b 21')
income_tally = lines('7 8a 9a 10 11 12 13 14 15b 16b 17 18 19 20b 21')
adjustments = lines('23 24 25 26 27 28 29 30 31a 32 33 34 35')
credits = lines(range(47, 54))
other_taxes = lines('56 57 58 59a 59b 60')
payments = lines(range(62, 64) + ['64a', '64b'] + range(65, 72))

def defaults(form):
    f = form
    f.ssn = u''
    f.spouse_ssn = u''

    f.first_name = u''
    f.last_name = u''
    f.spouse_first_name = u''
    f.spouse_last_name = u''
    f.address = u''
    f.apartment_number = u''
    f.city_state_zip = u''
    f.foreign_country = u''
    f.foreign_province = u''
    f.foreign_postal_code = u''

    f.filing_status = u'S'

    f.line6a = False
    f.line6b = False

    for line in income_lines + adjustments + credits + other_taxes + payments:
        setattr(f, line, zero)

    f.line21_text = u''
    f.line32b = u''

    f.line40 = zero
    f.line45 = zero


def check(form, forms, eq):
    nothing = [None]

    f1040sa = forms.get('us.f1040sa', nothing)[0]
    if f1040sa:
        eq('line40', f1040sa.line29)

    f1040sb = forms.get('us.f1040sb', nothing)[0]
    if f1040sb:
        eq('line8a', f1040sb.line4)
        eq('line9a', f1040sb.line6)

    f1040sc = forms.get('us.f1040sc', nothing)[0]
    if f1040sc:
        if f1040sc.line31 > zero:
            eq('line12', f1040sc.line31)
        # TODO: further instructions about if it comes out negative

    f1040sd = forms.get('us.f1040sd', nothing)[0]
    if f1040sd:
        if f1040sd.line16 > zero:
            eq('line13', f1040sd.line16)
        else:
            eq('line13', -f1040sd.line21)

    f1040se = forms.get('us.f1040se', nothing)[0]
    if f1040se:
        eq('line17', f1040se.line41)

    f1040sse = forms.get('us.f1040sse', nothing)[0]
    if f1040sse:
        eq('line56', f1040sse.line5)
        eq('line27', f1040sse.line6)


def compute(form):
    f = form
    f.line6ab = bool(f.line6a) + bool(f.line6b)
    # TODO: dependents
    f.line6d = f.line6ab
    f.line22 = dsum(getattr(f, line) for line in income_tally)
    f.line36 = dsum(getattr(f, line) for line in adjustments)
    f.line37 = f.line22 - f.line36
    f.line38 = f.line37
    # TODO: standard deduction
    f.line41 = f.line38 - f.line40
    f.line42 = f.line6d * Decimal('3800.00')
    f.line43 = max(f.line41 - f.line42, zero)
    f.line44 = tax_from_tax_table(f.line43, f.filing_status)
    f.line46 = f.line44 + f.line45
    f.line54 = dsum(getattr(f, line) for line in credits)
    f.line55 = f.line46 - f.line54
    f.line61 = f.line55 + dsum(getattr(f, line) for line in other_taxes)
    f.line72 = dsum(getattr(f, line) for line in payments) - f.line64b
    if f.line72 > f.line61:
        f.line73 = f.line72 - f.line61
        # TODO: asking for refund etc
    elif f.line61 > f.line72:
        f.line76 = f.line61 - f.line72


def fill_out(form, pdf):
    f = form
    pdf.load('us.f1040--{}.pdf'.format(f.form_version))

    pdf.pattern = 'p1-t{}['

    pdf[4] = f.first_name
    pdf[5] = f.last_name
    pdf[6] = f.spouse_first_name
    pdf[7] = f.spouse_last_name
    pdf[8] = f.address
    pdf[9] = f.apartment_number
    pdf[10] = f.city_state_zip
    pdf['011'] = f.foreign_country
    pdf['012'] = f.foreign_province
    pdf['013'] = f.foreign_postal_code

    pdf[11] = f.ssn.replace('-', '')
    pdf[14] = f.spouse_ssn.replace('-', '')

    # TODO: checkboxes for the Presidential Election Campaign (or not?)

    pdf.pattern = '{}'

    pdf['c1_04['] = [(status if f.filing_status == status else u'Off')
                       for status in filing_statuses]
    # TODO: text fields that go along with filing statuses

    pdf['c1_05[0]'] = '1' if f.line6a else 'Off'
    pdf['c1_06[0]'] = '1' if f.line6b else 'Off'

    pdf.pattern = 'p1-t{}['

    pdf[19] = str(f.line6ab)
    # TODO: dependents
    pdf[45] = str(f.line6d)

    n = 46
    for line in income_lines + lines('22') + adjustments + lines('36 37'):
        pdf[n], pdf[n+1] = zzstr(getattr(f, line))
        if n == 82:
            n = 85
        elif n == 103:
            n = 108
        else:
            n += 2

    pdf.pattern = '{}'

    pdf['Page1[0].p1-t84[0]'] = f.line21_text

    pdf.pattern = 'p2-t{}[0]'

    n = 1
    for line in (lines([38] + range(40, 47)) + credits + lines('54 55')
                 + other_taxes + lines('61') + payments + lines('72 73 74a')
                 + lines(range(75, 78))):
        pdf[n], pdf[n+1] = zzstr(getattr(f, line, zero)) # todo: remove default
        if n == 1:
            n = 4
        elif n == 20:
            n = 24
        elif n == 32:
            n = 37
        elif n == 45 and pdf.pattern == 'p2-t{}[0]':
            pdf.pattern = 'p2-t{}[1]'
        elif n == 45 and pdf.pattern == 'p2-t{}[1]':
            pdf.pattern = 'p2-t{}[2]'
        elif n == 45 and pdf.pattern == 'p2-t{}[2]':
            pdf.pattern = 'p2-t{}[0]'
            n = 47
        elif n == 49:
            n = 53
        elif n == 69 and pdf.pattern == 'p2-t{}[0]':
            pdf.pattern = 'p2-t{}[1]'
        elif n == 69 and pdf.pattern == 'p2-t{}[1]':
            pdf.pattern = 'p2-t{}[0]'
            n = 71
        elif n == 77:
            n = 105
        else:
            n += 2


def tax_from_tax_table(taxable_income, filing_status):
    import csv
    import os
    here = os.path.dirname(__file__)
    with open(os.path.join(here, 'f1040-tax-table.csv')) as f:
        for row in csv.DictReader(f):
            minimum = Decimal(row['At Least'])
            maximum = Decimal(row['But Less Than'])
            if minimum <= taxable_income < maximum:
                return Decimal(row[filing_status] + '.00')
        else:
            return Decimal('1.23')
