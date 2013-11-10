from luca.forms.formlib import Form
from luca.kit import zero, zstr


title = u'Form 1099-MISC: Miscellaneous Income'
versions = u'2012',


def defaults(form):
    f = form
    f.payer = ''
    f.payer_number = ''
    f.recipient_number = ''
    f.recipient_name = ''
    f.recipient_street = ''
    f.recipient_city_state_zip = ''
    f.account_number = ''
    for n in range(1, 9):
        f['line', n] = zero
    f.line9 = False
    f.line10 = zero
    f.line11 = zero
    f.line12 = ''
    f.line13 = zero
    f.line14 = zero
    f.line15a = zero
    f.line15b = zero
    f.states = [Form(), Form()]
    for state in f.states:
        state.line16 = zero
        state.line17 = zero
        state.line18 = zero


def compute(form):
    pass


def fill_out(form, pdf):
    f = form
    pdf.load('us.f1099msc--{}.pdf'.format(f.form_version))

    # The pdftk "fill_form" command seems to ignore "\r" characters
    # so we have to draw the payer ourselves; see draw() below.
    #
    # fields['f1_001[0]'].all = f.payer

    pdf.pattern = 'f1_{:03}[0]'
    pdf[1] = f.payer

    pdf[2] = f.payer_number
    pdf[3] = f.recipient_number
    pdf[4] = f.recipient_name
    pdf[5] = f.recipient_street
    pdf[6] = f.recipient_city_state_zip
    pdf[7] = f.account_number
    pdf[8] = zstr(f.line15a)
    pdf[9] = zstr(f.line15b)
    pdf[10] = zstr(f.line1)
    pdf[11] = zstr(f.line2)
    pdf[12] = zstr(f.line3)
    pdf[13] = zstr(f.line4)
    pdf[14] = zstr(f.line5)
    pdf[15] = zstr(f.line6)
    pdf[16] = zstr(f.line7)
    pdf[17] = zstr(f.line8)
    pdf[18] = zstr(f.line10)
    pdf[101] = zstr(f.line11)
    pdf[19] = zstr(f.line13)
    pdf[20] = zstr(f.line14)

    if len(f.states) > 0:
        pdf[21] = zstr(f.states[0].line16)
        pdf[23] = zstr(f.states[0].line17)
        pdf[25] = zstr(f.states[0].line18)

    if len(f.states) > 1:
        pdf[22] = zstr(f.states[1].line16)
        pdf[24] = zstr(f.states[1].line17)
        pdf[26] = zstr(f.states[1].line18)

    if len(f.states) > 2:
        raise ValueError('Form 1099-MISC only supports two states')

    pdf.pattern = '{}'
    pdf['c1_02_0_[0]'] = 'Yes' if f.line9 else 'Off'
    pdf['Box12[0]'] = f.line12
