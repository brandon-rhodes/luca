from luca.kit import Decimal, dollars

title = u'Ohio Form IT-1040: Individual Income Tax Return'
versions = u'2012', u'2013'

zero = Decimal('0')
deductions = ('35a 35b 36 37a 37b 38a 38b 38c 39 '
              '40 41a 41b 42 43a 43b 43c 44 45').split()
nonbusiness_credits = range(48, 57)

# TODO: someday also support Section B (Long Schedule SE)

def defaults(form):
    f = form

    f.ssn = ''
    f.spouse_ssn = ''
    f.first_name = ''
    f.middle_initial = ''
    f.last_name = ''
    f.spouse_first_name = ''
    f.spouse_middle_initial = ''
    f.spouse_last_name = ''
    f.address = ''
    f.city = ''
    f.state = ''
    f.zip = ''
    f.county = ''
    # TODO: separate home address, and foreign address
    f.email = ''

    f.residency_status = 'full-year'
    f.nonresident_state = ''
    f.spouse_residency_status = 'full-year'
    f.spouse_nonresident_state = ''
    f.filing_status = 'single'
    f.political_party_fund = False
    f.spouse_political_party_fund = False
    f.school_district_number = ''

    f.exemptions = 1

    if f.form_version == u'2012':
        return defaults_2012(form)

    f.line1 = zero
    f.line2 = zero
    f.line6 = zero  # TODO: someday, do tax table automatically
    f.line7 = zero
    f.line9 = zero
    f.line13 = zero
    f.line14 = zero
    f.line15 = zero
    f.line16 = zero

    f.line18 = zero
    f.line19 = zero
    f.line21 = zero
    f.line22 = zero
    f.line23 = zero
    f.line26 = zero
    f.line27 = zero
    f.line30 = zero

def defaults_2012(form):
    f = form
    f.line1 = zero
    f.line6 = zero
    f.line11_percent = zero
    f.line14 = zero
    f.line16 = zero
    f.line17 = zero
    f.line19 = zero
    f.line20 = zero
    f.line21a = zero
    f.line21b = zero
    f.line21c = zero
    f.line21d = zero
    f.line24 = zero
    f.line25a = zero
    f.line25b = zero
    f.line25c = zero
    f.line25d = zero
    f.line28 = zero  # TODO: compute instead?

    f.line31 = zero
    f.line32 = zero
    for letter in 'abcdefg':
        f['line33', letter] = zero
    for number in deductions:
        f['line', number] = zero

    for number in nonbusiness_credits:
        f['line', number] = zero

    f.line58 = zero
    f.line61 = zero
    f.line63 = zero

def compute(form):
    f = form
    if f.form_version == u'2012':
        return compute_2012(form)

    f.line3 = dollars(f.line1 + f.line2)
    f.line4 = f.exemptions * dollars('1700')
    f.line5 = dollars(max(0, f.line3 - f.line4))
    f.line8 = dollars(max(0, f.line6 - f.line7))
    f.line10 = dollars(max(0, f.line8 - f.line9))
    f.line10a = f.line10
    f.line11_percent = (20 if f.line5 <= 25000 else
                        15 if f.line5 <= 50000 else
                        10 if f.line5 <= 75000 else 5)
    f.line11 = dollars(min(650, f.line10a * f.line11_percent / 100))
    f.line12 = f.line10a - f.line11
    f.line17 = max(zero, f.line12 - f.line13 - f.line14 - f.line15 - f.line16)

    f.line20 = f.line17 + f.line18 + f.line19
    f.line24 = f.line21 + f.line22 + f.line23
    if f.line24 >= f.line20:
        f.line25 = f.line24 - f.line20
        f.line28 = f.line25 - f.line26 - f.line27
        f.line29 = zero
    else:
        f.line25 = zero
        f.line28 = zero
        f.line29 = f.line20 - f.line24
    if f.line28:
        f.line31 = zero
        f.line32 = f.line28 - f.line30
    else:
        f.line31 = f.line29 + f.line30
        f.line32 = zero

def compute_2012(form):
    f = form

    # Schedule A

    f.line34 = f.line31 + f.line32 + sum(f['line33', x] for x in 'abcdefg')
    f.line46 = sum(f['line', number] for number in deductions)
    f.line47 = f.line34 - f.line46

    # Schedule B

    f.line57 = sum(f['line', number] for number in nonbusiness_credits)

    # Start of main page

    f.line2 = f.line47
    f.line3 = f.line1 + f.line2
    f.line4 = f.exemptions * dollars('1700')
    f.line5 = max(zero, f.line3 - f.line4)
    f.line7 = f.line57
    f.line8 = max(zero, f.line6 - f.line7)
    f.line9 = f.exemptions * dollars('20')
    f.line10 = max(zero, f.line8 - f.line9)
    f.line10a = f.line10
    f.line11 = min(dollars('650'), dollars(f.line10a * f.line11_percent / 100))
    f.line12 = f.line10a - f.line11

    # Schedule C

    f.line59 = f.line3
    f.line60_factor = (f.line58 / f.line59).quantize(Decimal('0.0001'))
    f.line60 = dollars(f.line12 * f.line60_factor)
    f.line62 = min(f.line60, f.line61)

    # Schedule D

    f.line64 = f.line3
    f.line65_factor = (f.line63 / f.line64).quantize(Decimal('0.0001'))
    f.line65 = dollars(f.line12 * f.line65_factor)

    # Summary of credits

    f.line66 = zero
    f.line67 = f.line62
    f.line68 = f.line65
    f.line69 = f.line66 + f.line67 + f.line68

    # Main page continued

    f.line13 = f.line69
    f.line15 = max(zero,
                   f.line12 - f.line13 - f.line14)
    f.line18 = f.line15 + f.line16 + f.line17
    f.line22 = (f.line19 + f.line20 + f.line21a
                + f.line21b + f.line21c
                + f.line21d)

    if f.line22 > f.line18:
        f.line23 = max(zero, f.line22 - f.line18)
        f.line26 = (f.line23 - f.line24 - f.line25a
                    - f.line25b - f.line25c
                    - f.line25d)
        f.line27 = zero
        f.line29 = zero
        f.line30 = f.line26 - f.line28
    else:
        f.line23 = zero
        f.line26 = zero
        f.line27 = f.line18 - f.line22
        f.line29 = f.line27 + f.line28
        f.line30 = zero

def fill_out(form, pdf):
    f = form
    pdf.load('us_oh.it1040--{}.pdf'.format(f.form_version))
    pdf.pages = [1, 2]

    if f.form_version == u'2012':
        return fill_out_2012(form, pdf)

    pdf[1], pdf[2], pdf[3] = f.ssn.split('-')
    pdf[5], pdf[6], pdf[7] = f.spouse_ssn.split('-')
    pdf[9] = str(f.school_district_number)
    for n, field in enumerate([
            f.first_name, f.middle_initial, f.last_name,
            f.spouse_first_name, f.spouse_middle_initial, f.spouse_last_name,
            f.address, f.city, f.state, f.zip, f.county[:4]
            ], 10):
        pdf[n] = field

    for n in range(21, 25 + 1):
        pdf[n] = ''
    pdf[26] = f.email

    def yes(value1, value2):
        return 'Yes' if value1 == value2 else 'Off'

    pdf[27] = (1 if f.residency_status == 'full-year' else
               2 if f.residency_status == 'part-year' else
               3)
    pdf[28] = f.nonresident_state
    pdf[29] = (1 if f.spouse_residency_status == 'full-year' else
               2 if f.spouse_residency_status == 'part-year' else
               3)
    pdf[30] = f.spouse_nonresident_state

    pdf[31] = (1 if f.filing_status == 'single' else
               2 if f.filing_status == 'jointly' else
               3)
    for n in range(32, 34 + 1):
        pdf[n] = ''

    pdf[36] = 1 if f.political_party_fund else 2
    pdf[37] = 1 if f.spouse_political_party_fund else 2

    pdf[41] = str(f.exemptions)

    starts = {1: 38, 4: 42, 6: 45, 11: 52, 28: 79, 29: 73}
    lines = [attr for attr in dir(f)
             if attr.startswith('line') and attr[-1].isdigit()]
    lines.sort(key=lambda attr: int(attr[4:]))

    for attr in lines:
        n = int(attr[4:])
        if n in starts:
            m = starts[n]
        else:
            m += 1
        value = getattr(f, attr)
        if isinstance(value, Decimal):
            value = str(value).replace('.00', '')
        pdf[m] = value

    pdf[50] = f.line10a
    pdf[51] = f.line11_percent

    pdf['mber'] = pdf[81] = pdf[83] = ''  # date and preparer fields
    for n in range(68, 71 + 2):
        pdf[n] = ''  # fund donation fields

def fill_out_2012(form, pdf):
    f = form
    pdf.load('us_oh.it1040--{}.pdf'.format(f.form_version))
    pdf.pages = [1, 2]
    if f.line2:
        pdf.pages.append(3)
    if f.line7 or f.line13:
        pdf.pages.append(4)

    pdf['PrimarySSN'] = f.ssn.upper()
    pdf['SecondarySSN'] = f.spouse_ssn.upper()
    pdf['PrimaryFirst'] = f.first_name.upper()
    pdf['PrimaryMI'] = f.middle_initial.upper()
    pdf['PrimaryLast'] = f.last_name.upper()
    pdf['SpouseFirst'] = f.spouse_first_name.upper()
    pdf['SpouseMI'] = f.spouse_middle_initial.upper()
    pdf['SpouseLast'] = f.spouse_last_name.upper()
    pdf['MailingAddress'] = f.address.upper()
    pdf['City'] = f.city.upper()
    pdf['State'] = f.state.upper()
    pdf['MailingAddressZip'] = f.zip.upper()
    pdf['MailingAddressCounty'] = f.county[:4].upper()
    pdf['E-mail Address'] = f.email

    def yes(value1, value2):
        return 'Yes' if value1 == value2 else 'Off'

    pdf['PrimaryFullYear'] = yes(f.residency_status, 'full-year')
    pdf['PrimaryPartYear'] = yes(f.residency_status, 'part-year')
    pdf['PrimaryNonresident'] = yes(f.residency_status, 'nonresident')
    pdf['PrimaryNonresidentState'] = f.nonresident_state

    pdf['SpouseFullYear'] = yes(f.spouse_residency_status, 'full-year')
    pdf['SpousePartYear'] = yes(f.spouse_residency_status, 'part-year')
    pdf['SpouseNonresident'] = yes(f.spouse_residency_status,
                                        'nonresident')
    pdf['SpouseNonresidentState'] = f.spouse_nonresident_state

    pdf['Single'] = yes(f.filing_status, 'single')
    pdf['MarriedFilingJointly'] = yes(f.filing_status, 'jointly')
    pdf['MarriedFilingSeparately'] = yes(f.filing_status, 'separately')

    pdf['PrimaryPoliticalFundYes'] = yes(f.political_party_fund, True)
    pdf['PrimaryPoliticalFundNo'] = yes(f.political_party_fund, False)

    pdf['SpousePoliticalFundYes'] = yes(f.spouse_political_party_fund, True)
    pdf['SpousePoliticalFundNo'] = yes(f.spouse_political_party_fund, False)

    pdf['School'] = str(f.school_district_number)
    pdf['exemptions'] = str(f.exemptions)
    pdf['dispVal'] = str(int(f.line11_percent))

    for attr in dir(f):
        if attr.startswith('line'):
            value = getattr(f, attr)
            if isinstance(value, Decimal):
                value = str(value).replace('.00', '')
            pdf[attr.capitalize()] = value
