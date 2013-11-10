from luca.kit import dsum, zero, zzstr

title = u'Form 1040 Schedule C: Profit or Loss From Business'
versions = u'2012',

def defaults(form):
    f = form
    f.name = ''
    f.ssn = ''
    for letter in 'ABCD':
        setattr(f, letter, '')
    f.E_text1 = ''
    f.E_text2 = ''
    f.F = 'cash'
    f.F_text = ''
    for letter in 'GHIJ':
        setattr(f, letter, False)

    # Part I: Income

    f.line1_box = False
    f.line1 = f.line2 = f.line4 = f.line6 = zero

    # Part II: Expenses

    for attr in _expense_lines():
        setattr(f, attr, zero)

    f.line30 = zero
    f.line32 = 'a'

    # Part III: Cost of Goods Sold

    f.line33 = 'a'
    f.line34 = False
    for n in range(35, 40):
        setattr(f, 'line{}'.format(n), zero)
    f.line41 = zero

    # Part IV: Information on Your Vehicle
    # TODO

    # Part V: Other Expenses

    f.Part_V = [['', zero], ['', zero]]

def check(form, forms, eq):
    matches = forms['us.f8829']
    if matches:
        f8829 = matches[0]
        eq('line30', f8829.line35)

    if form.line31 > 0:
        if not forms.get('us.f1040sse', ()):
            print ('Error: Schedule C line 41 is more than zero; you need to '
                   'file Schedule SE')

def compute(form):
    f = form

    # Part I: Income

    f.line3 = f.line1 - f.line2
    f.line5 = f.line3 - f.line4
    f.line7 = f.line5 + f.line6

    # Part II: Expenses

    f.line28 = dsum(getattr(f, attr) for attr in _expense_lines())
    f.line29 = f.line7 - f.line28
    f.line31 = f.line29 - f.line30

    # Part III: Cost of Goods Sold

    f.line40 = f.line35 + f.line36 + f.line37 + f.line38 + f.line39
    f.line42 = f.line40 - f.line41

    # Part IV: Information on Your Vehicle
    # TODO

    # Part V: Other Expenses

    f.line48 = dsum(value for expense, value in f.Part_V)

def fill_out(form, pdf):
    f = form
    pdf.load('us.f1040sc--{}.pdf'.format(f.form_version))

    pdf.pattern = 'f1_{:03}['

    pdf[1] = f.name
    pdf[2] = f.ssn

    pdf[3] = f.A
    pdf[4] = f.B
    pdf[5] = f.C
    pdf[6] = f.D

    pdf[7] = f.E_text1
    pdf[8] = f.E_text2
    pdf[9] = f.F_text

    pdf.pattern = '{}'

    pdf['.c1_01['] = '0' if f.F == 'cash' else 'Off'
    pdf['.c1_02['] = '0' if f.F == 'accrual' else 'Off'
    pdf['.c1_03['] = '0' if f.F == 'other' else 'Off'

    pdf['.c1_04[0]'] = 'Yes' if f.G else 'Off'
    pdf['.c1_04[1]'] = 'Off' if f.G else 'No'

    pdf['.c1_05[0]'] = '1' if f.H else 'Off'

    pdf['.c1_06[0]'] = 'Yes' if f.I else 'Off'
    pdf['.c1_06[1]'] = 'Off' if f.I else 'No'

    pdf['.c1_07[0]'] = 'Yes' if f.J else 'Off'
    pdf['.c1_07[1]'] = 'Off' if f.J else 'No'

    # Part I: Income

    pdf['.c1_08_0_['] = '1' if f.line1_box else 'Off'

    pdf.pattern = 'f1_{:03}['

    pdf[10], pdf[11] = zzstr(f.line1)

    n = 18
    for i in range(2, 8):
        pdf[n], pdf[n+1] = zzstr(getattr(f, 'line{}'.format(i)))
        n += 2

    # Part II: Expenses

    n = 30
    for attr in _expense_lines():
        pdf[n], pdf[n+1] = zzstr(getattr(f, attr))
        if n == 74:
            n = 84
        else:
            n += 2

    pdf[76], pdf[77] = zzstr(f.line28)
    pdf[78], pdf[79] = zzstr(f.line29)
    pdf[80], pdf[81] = zzstr(f.line30)
    pdf[82], pdf[83] = zzstr(f.line31)

    pdf.pattern = '{}'

    if f.line31 < zero:
        pdf['.c1_08['] = '1' if f.line32 == 'a' else 'Off'
        pdf['.c1_09['] = '1' if f.line32 == 'b' else 'Off'

    # Part III: Cost of Goods Sold

    pdf['.c2_01['] = '1' if f.line33 == 'a' else 'Off'
    pdf['.c2_02['] = '1' if f.line33 == 'b' else 'Off'
    pdf['.c2_03['] = '1' if f.line33 == 'c' else 'Off'

    pdf['.c2_04[0]'] = 'Yes' if f.line34 else 'Off'
    pdf['.c2_04[1]'] = 'Off' if f.line34 else 'No'

    pdf.pattern = 'f2_{:03}['

    n = 1
    for i in range(35, 43):
        pdf[n], pdf[n+1] = zzstr(getattr(f, 'line{}'.format(i)))
        n += 2

    # Part IV: Information on Your Vehicle
    # TODO

    # Part V: Other Expenses

    n = 23
    for text, value in f.Part_V:
        pdf[n] = text
        pdf[n+1], pdf[n+2] = zzstr(value)
        n += 3

    pdf[50], pdf[51] = zzstr(f.line48)

# Helper functions.

def _expense_lines():
    for n in range(8, 28):
        if n in (16, 20, 24, 27):
            yield 'line{}a'.format(n)
            yield 'line{}b'.format(n)
        else:
            yield 'line{}'.format(n)
