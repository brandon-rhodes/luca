from luca.kit import Decimal, dollars, zero

title = u'Ohio Form SD-100: Individual Income Tax Return'
versions = u'2012', u'2013'

deductions = ('35a 35b 36 37a 37b 38a 38b 38c 39 '
              '40 41a 41b 42 43a 43b 43c 44 45').split()
nonbusiness_credits = range(48, 57)

# TODO: someday also support Section B (Long Schedule SE)

def defaults(form):
    f = form

    f.ssn = ''
    f.spouse_ssn = ''
    f.school_district_number = ''
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

    f.residency = 'full-year'
    f.spouse_residency = 'full-year'
    # TODO: dates of nonresidency in case of a mid-year move
    f.filing_status = 'single'
    f.tax_type = 'traditional'

    if f.form_version == u'2012':
        return defaults_2012(form)

    f.line1 = zero
    f.line2_rate = zero
    f.line3 = zero
    f.line5 = zero
    f.line7 = zero
    f.line8 = zero
    f.line11 = zero
    f.line14 = zero

def defaults_2012(form):
    f = form
    f.line1 = zero
    f.line2 = zero
    f.line4_rate = zero
    f.line5 = zero
    f.line7 = zero
    f.line9 = zero
    f.line10 = zero
    f.line13 = zero
    f.line16 = zero
    f.line19 = ''
    f.line20 = ''
    f.line21 = ''
    f.line22 = ''

def compute(form):
    f = form

    if f.form_version == u'2012':
        return compute_2012(form)

    f.line2 = dollars(f.line1 * f.line2_rate / 100)
    f.line4 = f.line2 - f.line3
    f.line6 = f.line4 + f.line5
    f.line9 = f.line7 + f.line8
    if f.line9 > f.line6:
        f.line10 = f.line9 - f.line6
        f.line12 = f.line10 - f.line11
        f.line13 = zero
        f.line15 = zero
        f.line16 = f.line12 - f.line14
    else:
        f.line10 = zero
        f.line12 = zero
        f.line13 = f.line6 - f.line9
        f.line15 = f.line13 + f.line14
        f.line16 = zero

def compute_2012(form):
    f = form
    d = dollars
    f.line3 = d(f.line1) - d(f.line2)
    f.line3a = d(f.line3)
    f.line4 = d(f.line3a * f.line4_rate)
    f.line6 = f.line4 - d(f.line5)
    f.line8 = f.line6 + d(f.line7)
    f.line11 = d(f.line9) + d(f.line10)
    if f.line11 > f.line8:
        f.line12 = f.line11 - f.line8
        f.line14 = f.line12 - f.line13
        f.line15 = u''
        f.line16 = u''
        f.line17 = u''
        f.line18 = f.line14 - f.line16
    else:
        f.line12 = u''
        f.line14 = u''
        f.line15 = f.line8 - f.line11
        f.line17 = f.line15 + f.line16
        f.line18 = u''

def fill_out(form, pdf):
    f = form
    pdf.load('us_oh.sd100--{}.pdf'.format(f.form_version))
    pdf.pages = 1, 2

    if f.form_version == u'2012':
        return fill_out_2012(form, pdf)

    pdf.pattern = None

    pdf[1], pdf[2], pdf[3] = f.ssn.split('-')
    pdf[5], pdf[6], pdf[7] = f.spouse_ssn.split('-')
    pdf[9] = f.school_district_number

    for n, value in enumerate([
            f.first_name, f.middle_initial, f.last_name,
            f.spouse_first_name, f.spouse_middle_initial, f.spouse_last_name,
            f.address, f.city, f.state, f.zip, f.county.upper()[:4],
            ], 10):
        pdf[n] = value

    pdf[26] = (1 if f.residency == 'full-year' else
               2 if f.residency == 'part-year' else
               3)
    pdf[29] = (1 if f.spouse_residency == 'full-year' else
               2 if f.spouse_residency == 'part-year' else
               3)

    pdf[32] = (1 if f.filing_status == 'single' else
               2 if f.filing_status == 'jointly' else
               3)
    pdf[36] = (1 if f.tax_type == 'traditional' else 2)

    pdf[38] = f.line2_rate

    starts = {1: 37, 2: 39, 7: 46}
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

    pdf[45] = str(f.line6).replace('.00', '')

def fill_out_2012(form, pdf):
    f = form

    # Fields on both page 1 and page 2

    pdf['PrimarySSN'] = f.ssn
    pdf['SD#'] = f.school_district_number

    # Fields on page 1

    # pdf['F0020PrimaryDecd']
    pdf['F0030SecondarySSN'] = f.spouse_ssn
    # pdf['F0040SecondaryDecd']
    # pdf['F0050holdTaxYR']
    pdf['F0070PrimaryFirstName'] = f.first_name
    pdf['F0080PrimaryMI'] = f.middle_initial
    pdf['F0090PrimaryLastName'] = f.last_name
    pdf['F0100SpouseFirstName'] = f.spouse_first_name
    pdf['F0110SpouseMI'] = f.spouse_middle_initial
    pdf['F0120SpouseLastName'] = f.spouse_last_name
    pdf['F0130MailingAddress'] = f.address
    pdf['F0140City'] = f.city
    pdf['F0150State'] = f.state
    pdf['F0160MailingAddressZipcode'] = f.zip
    pdf['F0170MailingAddressCounty'] = f.county.upper()[:4]
    # pdf['F0180HomeAddress']
    # pdf['F0190HomeAddressZip']
    # pdf['F0200HomeAddressCounty']
    # pdf['F0210ForeignCountry']
    # pdf['F0220Foreignpostalcode']

    def yes(condition):
        return 'Yes' if condition else 'Off'

    r = f.residency
    pdf['F0230PrimaryFullYear'] = yes(r == 'full-year')
    pdf['F0240PrimaryPartYear'] = yes(r == 'part-year')
    pdf['F0250PrimaryNonresident'] = yes(r == 'nonresident')

    r = f.spouse_residency
    pdf['F0270SpouseFullYear'] = yes(r == 'full-year')
    pdf['F0280SpousePartYear'] = yes(r == 'part-year')
    pdf['F0290SpouseNonresident'] = yes(r == 'nonresident')

    # pdf['F0260primary_SDresidency_status']
    # pdf['F0300spouse_SDresidency_status']
    # pdf['F0350filing_status']

    pdf['F0310Single'] = yes(f.filing_status == 'single')
    pdf['F0320MarriedFilingJointly'] = yes(f.filing_status == 'joint')
    pdf['F0330MarriedFilingSeparately'] = yes(f.filing_status == 'separate')
    # pdf['F0340MFS SSN']

    pdf['Traditionaltax'] = yes(f.tax_type == 'traditional')
    pdf['Earnedincomeonlytax'] = yes(f.tax_type == 'earned-income')

    for attr in dir(f):
        if attr.startswith('line'):
            value = getattr(f, attr)
            if isinstance(value, Decimal):
                value = str(dollars(value)).replace('.00', '')
            pdf[attr.capitalize()] = value
