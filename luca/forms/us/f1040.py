from luca.kit import cents, dsum, zero, zzstr

title = u'Form 1040: U.S. Individual Income Tax Return'

filing_statuses = 'S MJ MS HoH QW'.split()

def lines(string):
    return ['line' + suffix for suffix in string.split()]

income_lines = lines('7 8a 8b 9a 9b 10 11 12 13 14 15a 15b '
                     '16a 16b 17 18 19 20a 20b 21 22')
income_tally = lines('7 8a 9a 10 11 12 13 14 15b 16b 17 18 19 20b 21')

def defaults(form):
    f = form
    f.form_version = u'2012'
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

    for line in income_lines[:-1]:
        setattr(f, line, zero)

    f.line21_text = u''

def check(form, forms, eq):
    nothing = [None]

    f1040sb = forms.get('us.f1040sb', nothing)[0]
    if f1040sb:
        eq('line8a', f1040sb.line4)
        eq('line9a', f1040sb.line6)
        # TODO: further instructions about if it comes out negative

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


def compute(form):
    f = form
    f.line6ab = bool(f.line6a) + bool(f.line6b)
    # TODO: dependents
    f.line6d = f.line6ab
    f.line22 = dsum(getattr(f, line) for line in income_tally)

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
    for line in income_lines:
        pdf[n], pdf[n+1] = zzstr(getattr(f, line))
        n += 2
        if n == 84:
            pdf[n] = f.line21_text
            n += 1
