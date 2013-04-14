from luca.kit import Decimal, cents

title = u'Schedule C (Form 1040): Profit or Loss From Business'
filename = 'f1040sc--2012.pdf'
zero = cents(0)

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

def compute(form):
    f = form

    # Part I: Income

    f.line3 = f.line1 - f.line2
    f.line5 = f.line3 - f.line4
    f.line7 = f.line5 + f.line6

    # Part II: Expenses

    f.line28 = sum(getattr(f, attr) for attr in _expense_lines())
    f.line29 = f.line7 - f.line28
    f.line31 = f.line29 - f.line30

    # Part III: Cost of Goods Sold

    f.line40 = f.line35 + f.line36 + f.line37 + f.line38 + f.line39
    f.line42 = f.line40 - f.line41

    # Part IV: Information on Your Vehicle
    # TODO

    # Part V: Other Expenses

    f.line48 = sum((value for expense, value in f.Part_V), zero)

def fill(form, fields):
    f = form
    page = 1

    def put(n, value):
        sa, sb = zz(value)
        fields['f%d_%03d[' % (page, n+0)] = sa
        fields['f%d_%03d[' % (page, n+1)] = sb

    fields['f1_001['] = f.name
    fields['f1_002['] = f.ssn

    fields['f1_003['] = f.A
    fields['f1_004['] = f.B
    fields['f1_005['] = f.C
    fields['f1_006['] = f.D

    fields['f1_007['] = f.E_text1
    fields['f1_008['] = f.E_text2

    fields['.c1_01['] = '0' if f.F == 'cash' else 'Off'
    fields['.c1_02['] = '0' if f.F == 'accrual' else 'Off'
    fields['.c1_03['] = '0' if f.F == 'other' else 'Off'
    fields['f1_009['] = f.F_text

    fields['.c1_04[0]'] = 'Yes' if f.G else 'Off'
    fields['.c1_04[1]'] = 'Off' if f.G else 'No'

    fields['.c1_05[0]'] = '1' if f.H else 'Off'

    fields['.c1_06[0]'] = 'Yes' if f.I else 'Off'
    fields['.c1_06[1]'] = 'Off' if f.I else 'No'

    fields['.c1_07[0]'] = 'Yes' if f.J else 'Off'
    fields['.c1_07[1]'] = 'Off' if f.J else 'No'

    # Part I: Income

    fields['.c1_08_0_['] = '1' if f.line1_box else 'Off'
    put(10, f.line1)
    n = 18
    for i in range(2, 8):
        put(n, getattr(f, 'line{}'.format(i)))
        n += 2

    # Part II: Expenses

    n = 30
    for attr in _expense_lines():
        put(n, getattr(f, attr))
        if n == 74:
            n = 84
        else:
            n += 2

    put(76, f.line28)
    put(78, f.line29)
    put(80, f.line30)
    put(82, f.line31)

    if f.line31 < zero:
        fields['.c1_08['] = '1' if f.line32 == 'a' else 'Off'
        fields['.c1_09['] = '1' if f.line32 == 'b' else 'Off'

    # Part III: Cost of Goods Sold

    page = 2

    fields['.c2_01['] = '1' if f.line33 == 'a' else 'Off'
    fields['.c2_02['] = '1' if f.line33 == 'b' else 'Off'
    fields['.c2_03['] = '1' if f.line33 == 'c' else 'Off'

    fields['.c2_04[0]'] = 'Yes' if f.line34 else 'Off'
    fields['.c2_04[1]'] = 'Off' if f.line34 else 'No'

    n = 1
    for i in range(35, 43):
        put(n, getattr(f, 'line{}'.format(i)))
        n += 2

    # Part IV: Information on Your Vehicle
    # TODO

    # Part V: Other Expenses

    n = 23
    for text, value in f.Part_V:
        setattr(f, 'f2_%03d' % n, text)
        put(n + 1, value)

    put(50, f.line48)

# Helper functions.

def _expense_lines():
    for n in range(8, 28):
        if n in (16, 20, 24, 27):
            yield 'line{}a'.format(n)
            yield 'line{}b'.format(n)
        else:
            yield 'line{}'.format(n)

# General-purpose functions that will probably be factored out of here:

def yesno(value, fields):
    if value:
        fields[0] = 'Yes'
    else:
        fields[1] = 'No'

def z(value):
    if not value:
        return u''
    return unicode(value)

def zz(value):
    if not isinstance(value, Decimal):
        return value
    if not value:
        return (u'', u'')
    return unicode(value).split('.')
