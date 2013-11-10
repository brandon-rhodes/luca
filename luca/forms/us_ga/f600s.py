from decimal import Decimal
from luca.forms.formlib import Form
from luca.kit import dollars, zero


title = u'Georgia Form 600S: Corporation Tax Return'
versions = u'2012',


def defaults(form):
    f = form
    f.income_beginning = u''
    f.income_ending = u''
    f.net_worth_beginning = u''
    f.net_worth_ending = u''
    f.type = 'original'
    # TODO: Boolean "change" fields
    f.ein = u''
    f.name = u''
    f.incorporation_date = u''
    f.withholding_number = u''
    f.nonresident_withholding_number = u''
    f.address = u''
    f.incorporation_state = u''
    f.sales_tax_number = u''
    f.city = u''
    f.state = u''
    f.zip = u''
    f.date_admitted = u''
    f.naics_code = u''
    f.books_city = u''
    f.books_state = u''
    f.books_phone = u''
    f.kind_of_business = u''
    f.total_shareholders = u''
    f.nonresident_shareholders = u''
    f.federal_ordinary_income = zero
    # TODO: latest taxable year

    f.s1 = s1 = Form()
    # TODO: schedule 2
    f.s3 = s3 = Form()
    f.s4 = s4 = Form()
    # TODO: schedule 5
    # TODO: schedule 6
    # TODO: schedule 7
    f.s8 = s8 = Form()
    f.s9 = s9 = Form()
    # TODO: schedule 10
    # TODO: schedule 11

    s1.line1 = zero

    s3.line1 = zero
    s3.line2 = zero
    s3.line3 = zero
    s3.line5 = Decimal('1.00')
    s3.line7 = zero  # TODO: do tax table lookup automatically

    s4.line2c = zero
    s4.line3c = zero  # TODO: implement Schedule 10?
    s4.line4c = zero

    s8.line1 = zero
    s8.line2 = zero
    s8.line3a = zero
    s8.line3b = zero
    s8.line4a = zero
    s8.line4b = zero
    s8.line4c = zero
    s8.line4d = zero
    s8.line4e = zero
    s8.line4f = zero
    s8.line5 = zero
    s8.line6 = zero

    s9.line2 = zero
    s9.line4 = Decimal('1.00')
    s9.line6 = zero

def compute(form):
    f = form
    d = dollars
    s1, s3, s4, s8, s9 = f.s1, f.s3, f.s4, f.s8, f.s9

    s1.line2 = d(Decimal('0.06') * s1.line1)

    # TODO: schedule 2

    s3.line4 = d(s3.line1) + d(s3.line2) + d(s3.line3)
    s3.line6 = d(s3.line4 * s3.line5)

    s4.line1a = s1.line2
    s4.line1b = s3.line7
    s4.line1c = d(s4.line1a + s4.line1b)
    balance = d(s4.line1c) - d(s4.line2c) - d(s4.line3c) - d(s4.line4c)
    s4.line5c = max(zero, + balance)
    s4.line6c = max(zero, - balance)
    # TODO: penalty computation
    s4.line10c = s4.line5c # + penalties
    # TODO: refund

    s8.line3c = d(s8.line3a) - d(s8.line3b)
    s8.line7 = sum(d(s8['line', n]) for n
                   in '1 2 3c 4a 4b 4c 4d 4e 4f 5 6'.split())
    s8.line8 = zero  # TODO: schedule 5
    s8.line9 = s8.line7 + s8.line8
    s8.line10 = zero  # TODO: schedule 6
    s8.line11 = s8.line9 - s8.line10

    s9.line1 = s8.line11
    s9.line3 = s9.line1 - d(s9.line2)
    s9.line5 = d(s9.line3 * s9.line4)
    s9.line7 = s9.line5 + d(s9.line6)

def fill_out(form, pdf):
    f = form
    pdf.load('us_ga.f600s--{}.pdf'.format(f.form_version))
    pdf.pattern = None

    pdf['FEIN'] = f.ein
    pdf['FEIN_COPY'] = f.ein

    pdf['CORP_NAME'] = f.name.upper()
    pdf['CORP_NAME_COPY'] = f.name.upper()

    pdf['2011_DATE_BEG'] = f.income_beginning
    pdf['2011_DATE_END'] = f.income_ending
    pdf['2012_DATE_BEG'] = f.net_worth_beginning
    pdf['2012_DATE_END'] = f.net_worth_ending
    pdf['CB_TYPEOFRETURN'] = f.type
    # TODO: Boolean "change" fields
    pdf['DATE_OF_INCORPORATION'] = f.incorporation_date
    pdf['PAYROLL_WTH_NUM'] = f.withholding_number
    pdf['NONRES_WTH_NUM'] = f.nonresident_withholding_number
    pdf['CORP_ADDRESS'] = f.address.upper()
    pdf['STATE_INCORPORATED'] = f.incorporation_state
    pdf['SALES_TAX_REG_NUM'] = f.sales_tax_number
    pdf['CITY'] = f.city.upper()
    pdf['STATE'] = f.state
    pdf['ZIP5'] = f.zip
    pdf['DATE_ADMITTED_IN_GA'] = f.date_admitted
    pdf['NAICS'] = f.naics_code
    pdf['BOOKS_CITY_LOC'] = f.books_city.upper()
    pdf['BOOKS_STATE_LOC'] = f.books_state
    pdf['PHONE'] = f.books_phone
    pdf['KIND_OF_BUSINESS'] = f.kind_of_business.upper()
    pdf['TTL_SH'] = f.total_shareholders
    pdf['TTL_NONRES_SH'] = f.nonresident_shareholders
    pdf['FED_ORD_INCOME'] = str(dollars(f.federal_ordinary_income))

    for sname in 's1 s3 s4 s8 s9'.split():
        s = getattr(form, sname)
        for attr, value in s.__dict__.items():
            if not attr.startswith('line'):
                continue
            n = attr.replace('line', '')
            if sname == 's4':
                letter = n[-1]
                n = n[:-1]
                fieldname = '{}{}.{}'.format(sname, letter, n).upper()
            else:
                fieldname = '{}.{}'.format(sname, n).upper()
            if isinstance(value, Decimal):
                value = str(dollars(value))
            pdf[fieldname] = value

    pdf.pattern = '{}'
    pdf['CREDITCODE'] = u''  # clean up pre-filled values on last page
