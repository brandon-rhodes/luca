from luca.forms.formlib import Form
from luca.kit import zero, zstr


title = u'Miscellaneous Income'


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
        setattr(f, 'line{}'.format(n), zero)
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


def fill(form, fields):
    f = form

    # The pdftk "fill_form" command seems to ignore "\r" characters
    # so we have to draw the payer ourselves; see draw() below.
    #
    # fields['f1_001[0]'].all = f.payer

    fields['f1_002[0]'].all = f.payer_number
    fields['f1_003[0]'].all = f.recipient_number
    fields['f1_004[0]'].all = f.recipient_name
    fields['f1_005[0]'].all = f.recipient_street
    fields['f1_006[0]'].all = f.recipient_city_state_zip
    fields['f1_007[0]'].all = f.account_number
    fields['f1_008[0]'].all = zstr(f.line15a)
    fields['f1_009[0]'].all = zstr(f.line15b)
    fields['f1_010[0]'].all = zstr(f.line1)
    fields['f1_011[0]'].all = zstr(f.line2)
    fields['f1_012[0]'].all = zstr(f.line3)
    fields['f1_013[0]'].all = zstr(f.line4)
    fields['f1_014[0]'].all = zstr(f.line5)
    fields['f1_015[0]'].all = zstr(f.line6)
    fields['f1_016[0]'].all = zstr(f.line7)
    fields['f1_017[0]'].all = zstr(f.line8)
    fields['c1_02_0_[0]'].all = 'Yes' if f.line9 else 'Off'
    fields['f1_018[0]'].all = zstr(f.line10)
    fields['f1_101[0]'].all = zstr(f.line11)
    fields['Box12[0]'].all = f.line12
    fields['f1_019[0]'].all = zstr(f.line13)
    fields['f1_020[0]'].all = zstr(f.line14)

    if len(f.states) > 0:
        fields['f1_021[0]'].all = zstr(f.states[0].line16)
        fields['f1_023[0]'].all = zstr(f.states[0].line17)
        fields['f1_025[0]'].all = zstr(f.states[0].line18)

    if len(f.states) > 1:
        fields['f1_022[0]'].all = zstr(f.states[1].line16)
        fields['f1_024[0]'].all = zstr(f.states[1].line17)
        fields['f1_026[0]'].all = zstr(f.states[1].line18)

    if len(f.states) > 2:
        raise ValueError('Form 1099-MISC only supports two states')


def draw(form, canvas):
    f = form
    lines = f.payer.splitlines()

    for page in range(1, 8):
        if page in (2, 3, 4, 6, 7):
            canvas.setFont('Courier', 9)
            for i, line in enumerate(lines):
                canvas.drawString(54, 728 - i * 10, line)
        canvas.showPage()

    return 3, 4, 5, 6, 7
