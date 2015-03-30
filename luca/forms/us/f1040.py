from luca.kit import Decimal, dsum, zero, zzstr
from luca.taxes import TaxSchedule

title = u'Form 1040: U.S. Individual Income Tax Return'
versions = u'2012', u'2013', u'2014'

filing_statuses = 'S MJ MS HoH QW'.split()
exemptions = {
    u'2012': Decimal('3800.00'),
    u'2013': Decimal('3900.00'),
    u'2014': Decimal('3950.00'),
    }

def lines(seq):
    if isinstance(seq, str):
        seq = seq.split()
    return ['line{}'.format(suffix) for suffix in seq]

income_lines = lines('7 8a 8b 9a 9b 10 11 12 13 14 15a 15b '
                     '16a 16b 17 18 19 20a 20b 21')
income_tally = lines('7 8a 9a 10 11 12 13 14 15b 16b 17 18 19 20b 21')
adjustments = lines('23 24 25 26 27 28 29 30 31a 32 33 34 35')

class info2013:
    credits = lines(range(47, 54))
    other_taxes = lines('56 57 58 59a 59b 60')
    payments = lines(range(62, 64) + ['64a', '64b'] + range(65, 72))

class info2014:
    credits = lines(range(48, 55))
    other_taxes = lines('57 58 59 60a 60b 61 62')
    payments = lines([64, 65, '66a', '66b'] + range(67, 74))

info_dict = {u'2012': info2013, u'2013': info2013, u'2014': info2014}

def defaults(form):
    f = form
    v = info_dict[f.form_version]

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

    for line in (income_lines + adjustments + v.credits
                 + v.other_taxes + v.payments):
        setattr(f, line, zero)

    f.line21_text = u''
    f.line32b = u''

    f.line40 = zero
    f.line45 = zero

    f.line76a = zero
    f.line77 = zero
    f.line79 = zero

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

    self_employment_tax = zero
    line27 = zero
    for f in forms.get('us.f1040sse', ()):
        self_employment_tax += f.line5
        line27 += f.line6
    for f in forms.get('us.f1040sse_long', ()):
        self_employment_tax += f.line12
        line27 += f.line13
    if f.form_version <= u'2013':
        eq('line56', self_employment_tax)
    else:
        eq('line57', self_employment_tax)
    eq('line27', line27)


def compute(form):
    f = form
    v = info_dict[f.form_version]

    f.line6ab = bool(f.line6a) + bool(f.line6b)
    # TODO: dependents
    f.line6d = f.line6ab
    f.line22 = dsum(getattr(f, line) for line in income_tally)
    f.line36 = dsum(getattr(f, line) for line in adjustments)
    f.line37 = f.line22 - f.line36
    f.line38 = f.line37
    # TODO: standard deduction
    f.line41 = f.line38 - f.line40
    exemption = exemptions[f.form_version]
    f.line42 = f.line6d * exemption
    f.line43 = max(f.line41 - f.line42, zero)
    if form.form_version == u'2012':
        f.line44 = tax_from_tax_table(f.line43, f.filing_status)
    else:
        schedule = schedules[form.form_version][f.filing_status]
        f.line44 = schedule.compute_tax_on(f.line43)

    if f.form_version < u'2014':
        return _compute_pre_2014(f, v)

    f.line46 = zero
    f.line47 = f.line44 + f.line45 + f.line46
    f.line55 = dsum(getattr(f, line) for line in v.credits)
    f.line56 = f.line47 - f.line55
    f.line63 = f.line56 + dsum(getattr(f, line) for line in v.other_taxes)
    f.line74 = dsum(getattr(f, line) for line in v.payments) - f.line66b
    if f.line74 > f.line63:
        f.line75 = f.line74 - f.line63
        f.line78 = zero
        # TODO: asking for refund etc
    elif f.line63 > f.line74:
        f.line75 = zero
        f.line78 = f.line63 - f.line74

def _compute_pre_2014(f, v):
    f.line46 = f.line44 + f.line45
    f.line54 = dsum(getattr(f, line) for line in v.credits)
    f.line55 = f.line46 - f.line54
    f.line61 = f.line55 + dsum(getattr(f, line) for line in v.other_taxes)
    f.line72 = dsum(getattr(f, line) for line in v.payments) - f.line64b
    if f.line72 > f.line61:
        f.line73 = f.line72 - f.line61
        # TODO: asking for refund etc
    elif f.line61 > f.line72:
        f.line76 = f.line61 - f.line72

def fill_out(form, pdf):
    pdf.load('us.f1040--{}.pdf'.format(form.form_version))

    if form.form_version < u'2014':
        return fill_out_2013_and_before(form, pdf)

    f = form
    #v = info_dict[f.form_version]

    pdf.pattern = 'f1_{:02}[0]'

    pdf[4] = f.first_name
    pdf[5] = f.last_name
    pdf[6] = f.ssn.replace('-', '')
    pdf[7] = f.spouse_first_name
    pdf[8] = f.spouse_last_name
    pdf[9] = f.spouse_ssn.replace('-', '')

    pdf.pattern = 'f1-{:02}[0]'

    pdf[10] = f.address
    pdf[11] = f.apartment_number
    pdf[12] = f.city_state_zip
    pdf[13] = f.foreign_country
    pdf[14] = f.foreign_province
    pdf[15] = f.foreign_postal_code

    pdf.pattern = '{}'

    pdf['Lines1-3[0].c1_03[0]'] = ('S' if f.filing_status == 'S' else 'Off')
    pdf['Lines1-3[0].c1_03[1]'] = ('MJ' if f.filing_status == 'MJ' else 'Off')
    pdf['Lines1-3[0].c1_03[2]'] = ('MS' if f.filing_status == 'MS' else 'Off')
    pdf['Page1[0].c1_03[0]'] = ('HoH' if f.filing_status == 'HoH' else 'Off')
    pdf['Page1[0].c1_03[1]'] = ('QW' if f.filing_status == 'QW' else 'Off')

    if f.filing_status == 'MS':
        pdf['Lines1-3[0].f1-16[0]'] = f.spouse_ssn

    pdf['c1_04[0]'] = ('1' if f.line6a else 'Off')
    pdf['c1_05[0]'] = ('1' if f.line6b else 'Off')

    # TODO: Dependents

    pdf.pattern = 'Page1[0].f1_{:02}[0]'

    pdf[30] = f.line6ab
    pdf[34] = f.line6d

    i = 35
    for n in ('7 8a 8b 9a 9b 10 11 12 13 14 15a 15b 16a 16b 17 18 19 '
              '20a 20b 21 22 23 24 25 26 27 28 29 '
              '30 31a 32 33 34 35 36 37').split():
        pdf[i], pdf[i+1] = zzstr(f['line', n])
        if n in ('21', '31a'):
            i += 3
        else:
            i += 2

    pdf.pattern = '{}'
    pdf['f1-_51[0]'] = zzstr(f.line13)[0]

    pdf.pattern = '.f2_{:02}[0]'

    i = 1
    for n in ([38] + range(40, 60) + '60a 60b'.split() + range(61, 66)
              + '66a 66b'.split() + range(67, 76) + '76a 77 78 79'.split()):
        pdf[i], pdf[i+1] = zzstr(f['line', n])
        if n == '76a':
            i += 4
        elif n in (38, 43, 53, 61, 72):
            i += 3
        else:
            i += 2

def fill_out_2013_and_before(form, pdf):
    f = form
    v = info_dict[f.form_version]

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
            if f.form_version <= u'2012':
                n = 108
            else:
                n = 106
        else:
            n += 2

    pdf.pattern = '{}'

    pdf['Page1[0].p1-t84[0]'] = f.line21_text

    pdf.pattern = 'p2-t{}[0]'

    n = 1
    for line in (lines([38] + range(40, 47)) + v.credits + lines('54 55')
                 + v.other_taxes + lines('61') + v.payments + lines('72 73 74a')
                 + lines(range(75, 78))):
        pdf[n], pdf[n+1] = zzstr(getattr(f, line, zero)) # todo: remove default
        if f.form_version == u'2013':
            if n == 1:
                n = 4
            elif n == 60:
                n = 65
            elif n == 65:  # TODO: more fields are wrong here; look for [1]'s
                n = 62
            else:
                n += 2
        elif f.form_version == u'2012':
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
            raise ValueError('not found in tax table')

schedules = {
    u'2013': {
        u'S': TaxSchedule([
            (0, 10),
            (8925, 15),
            (36250, 25),
            (87850, 28),
            (183250, 33),
            (398350, 35),
            (400000, '39.6'),
        ]),
        u'MJ': TaxSchedule([
            (0, 10),
            (17850, 15),
            (72500, 25),
            (146400, 28),
            (223050, 33),
            (398350, 35),
            (450000, '39.6'),
        ]),
        u'MS': TaxSchedule([
            (0, 10),
            (8925, 15),
            (36250, 25),
            (73200, 28),
            (111525, 33),
            (199175, 35),
            (225000, '39.6'),
        ]),
        u'HH': TaxSchedule([
            (10, 0),
            (12750, 15),
            (48600, 25),
            (125450, 28),
            (203150, 33),
            (398350, 35),
            (425000, '39.6'),
        ]),
    },
    u'2014': {
        u'S': TaxSchedule([
            (0, 10),
            (9075, 15),
            (36900, 25),
            (89350, 28),
            (186350, 33),
            (405100, 35),
            (406750, '39.6'),
        ]),
        u'MJ': TaxSchedule([
            (0, 10),
            (18150, 15),
            (73800, 25),
            (148850, 28),
            (226850, 33),
            (405100, 35),
            (457600, '39.6'),
        ]),
        u'MS': TaxSchedule([
            (0, 10),
            (9075, 15),
            (36900, 25),
            (74425, 28),
            (113425, 33),
            (202550, 35),
            (228800, '39.6'),
        ]),
        u'HH': TaxSchedule([
            (0, 10),
            (12950, 15),
            (49400, 25),
            (127500, 28),
            (206600, 33),
            (405100, 35),
            (432200, '39.6'),
        ]),
    },
}
