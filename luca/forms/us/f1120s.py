from luca.forms.formlib import Form
from luca.kit import validate, zero, zstr, zzstr


def defaults(form):
    f = form

    f.year = 2012
    f.ein = ''
    f.name = ''
    f.street = ''
    f.city_state_zip = ''

    f.lineA = f.lineB = f.lineE = ''
    f.lineC = False
    f.lineF = zero
    f.lineG = False
    f.lineH = '12345'
    f.lineI = 1

    f.line1a = f.line1b = f.line2 = f.line4 = f.line5 = zero
    for n in range(7, 20):
        f['line', n] = zero
    f.line22a = f.line22b = f.line23a = f.line23b = f.line23c = zero
    f.line24 = zero
    f.line27_credited = zero

    f.signer_title = ''
    f.discuss = False

    f.B = Form()
    f.B.line1 = 'a'
    f.B.line2_activity = ''
    f.B.line2_service = ''
    f.B.line3 = False
    # TODO: tables beneath line 4a and line4b
    f.B.line4a = []
    f.B.line4b = []
    f.B.line5ai = 0
    f.B.line5aii = 0
    f.B.line5bi = 0
    f.B.line5bii = 0
    f.B.line6 = False
    f.B.line7 = False
    f.B.line8 = zero
    f.B.line9 = zero
    f.B.line10 = True
    f.B.line11 = zero
    f.B.line12 = False
    f.B.line13a = False
    f.B.line13b = False

    f.K = Form()
    f.K.line2 = zero
    f.K.line3a = f.K.line3b = zero
    f.K.line4 = f.K.line5a = f.K.line5b = f.K.line6 = f.K.line7 = zero
    f.K.line8a = f.K.line8b = f.K.line8c = f.K.line9 = f.K.line10 = zero
    f.K.line10_type = ''
    f.K.line11 = f.K.line12a = f.K.line12b = f.K.line12c = f.K.line12d = zero
    f.K.line12c_type = ''
    f.K.line12d_type = ''
    f.K.line13a = f.K.line13b = f.K.line13c = f.K.line13d = zero
    f.K.line13e = f.K.line13f = f.K.line13g = zero
    f.K.line13d_type = ''
    f.K.line13e_type = ''
    f.K.line13g_type = ''
    for i in range(ord('a'), ord('m') + 1):
        f.K['line14', chr(i)] = zero
    f.K.line14n_accounting = 'a'
    for i in range(ord('a'), ord('f') + 1):
        f.K['line15', chr(i)] = zero
    for i in range(ord('a'), ord('e') + 1):
        f.K['line16', chr(i)] = zero
    f.K.line17a = f.K.line17b = f.K.line17c = zero

    # TODO: Schedule L
    # TODO: Schedule M-1

    f.M2 = Form()
    f.M2.line1a = zero
    f.M2.line3a = zero
    f.M2.line5a = zero
    f.M2.line7a = zero

    f.M2.line1b = zero
    f.M2.line3b = zero
    f.M2.line5b = zero
    f.M2.line7b = zero

    f.M2.line1c = zero
    f.M2.line7c = zero


def compute(form):
    f = form
    validate.year(f.year)

    f.line1c = f.line1a - f.line1b
    f.line3 = f.line1c - f.line2
    f.line6 = f.line3 + f.line4 + f.line5

    f.line20 = sum(f['line', n] for n in range(7, 20))
    f.line21 = f.line6 - f.line20

    f.line22c = f.line22a + f.line22b
    f.line23d = f.line23a + f.line23b + f.line23c
    owed = f.line22c + f.line24 - f.line23d
    if owed >= 0:
        f.line25 = owed
        f.line26 = zero
        f.line27 = zero
    else:
        f.line25 = zero
        f.line26 = -owed
        f.line27 = -owed - f.line27_credited

    f.K.line1 = f.line21
    f.K.line3c = f.K.line3a - f.K.line3b
    f.K.line18 = (
        f.K.line1 + f.K.line2 + f.K.line3c + f.K.line4
        + f.K.line5a + f.K.line6 + f.K.line7 + f.K.line8a
        + f.K.line9 + f.K.line10
        - f.K.line11 - f.K.line12a - f.K.line12b - f.K.line12c
        - f.K.line12d - f.K.line14l
        )

    f.M2.line2a = abs(f.line21) if f.line21 > 0 else zero
    f.M2.line4a = abs(f.line21) if f.line21 < 0 else zero
    f.M2.line6a = (f.M2.line1a + f.M2.line2a + f.M2.line3a
                   - f.M2.line4a - f.M2.line5a)
    f.M2.line8a = f.M2.line6a - f.M2.line7a

    f.M2.line6b = f.M2.line1b + f.M2.line3b - f.M2.line5b
    f.M2.line8b = f.M2.line6b - f.M2.line7b

    f.M2.line6c = f.M2.line1c
    f.M2.line8c = f.M2.line6c - f.M2.line7c


def fill_out(form, pdf):
    f = form
    pdf.load('us.f1120s--{}.pdf'.format(f.year))

    def field(n):
        return 'p{}-t{}[0]'.format(page, n)

    def pair(n, value):
        pdf[field(n)], pdf[field(n + 1)] = zzstr(value)

    page = 1

    # TODO: dates for non-calendar tax year

    pdf['p1-t4['] = f.name
    pdf['p1-t5['] = f.street
    pdf['p1-t6['] = f.city_state_zip

    pdf['p1-t7['] = f.lineA
    pdf['p1-t8['] = f.lineB
    pdf['c1_01_0_[0]'] = 'Yes' if f.lineC else 'Off'
    pdf['p1-t9['] = f.ein
    pdf['p1-t11['] = f.lineE
    pair(12, f.lineF)

    pdf['c1_02_0_[0]'] = 'Yes' if f.lineG else 'Off'
    pdf['c1_02_0_[1]'] = 'Off' if f.lineG else 'No'
    for i in range(1, 5+1):
        checked = str(i) in f.lineH
        pdf['c1_0{}_0_[0]'.format(i + 2)] = 'Yes' if checked else 'Off'
    pdf['p1-t14['] = str(f.lineI)

    pair(15, f.line1a)
    pair(17, f.line1b)
    pair(19, f.line1c)
    for i in range(2, 21+1):
        pair(2*i + 17, f['line', i])
    pair(61, f.line22a)
    pair(63, f.line22b)
    pair(65, f.line22c)
    pair(67, f.line23a)
    pair(69, f.line23b)
    pair(71, f.line23c)
    pair(73, f.line23d)
    pair(75, f.line24)
    pair(77, f.line25)
    pair(79, f.line26)
    pair(81, f.line27_credited)
    pair(83, f.line27)
    pdf['p1_t85'] = f.signer_title
    pdf['c1_9_0_[0]'] = 'Yes' if f.discuss else 'Off'
    pdf['c1_9_0_[1]'] = 'Off' if f.discuss else 'No'

    pdf['c2_01_0_[0]'] = 'A' if f.B.line1 == 'a' else 'Off'
    pdf['c2_01_0_[1]'] = 'B' if f.B.line1 == 'b' else 'Off'
    if f.B.line1 not in ('a', 'b'):
        pdf['c2_01_0_[2]'] = 'C'
        pdf['p2-t19['] = f.B.line1
    pdf['p2-t20['] = f.B.line2_activity
    pdf['p2-t21['] = f.B.line2_product
    pdf['c2_04_0_[0]'] = 'Yes' if f.B.line3 else 'Off'
    pdf['c2_04_0_[1]'] = 'Off' if f.B.line3 else 'No'
    pdf['c2_06_0_[0]'] = 'Yes' if f.B.line4a else 'Off'
    pdf['c2_06_0_[1]'] = 'Off' if f.B.line4a else 'No'
    pdf['c2_08_0_[0]'] = 'Yes' if f.B.line4b else 'Off'
    pdf['c2_08_0_[1]'] = 'Off' if f.B.line4b else 'No'
    pdf['c2_10_0_[0]'] = 'Yes' if (f.B.line5ai or f.B.line5aii) else 'Off'
    pdf['c2_10_0_[1]'] = 'Off' if (f.B.line5ai or f.B.line5aii) else 'No'
    pdf['c2_112_0_[0]'] = 'Yes' if (f.B.line5bi or f.B.line5bii) else 'Off'
    pdf['c2_112_0_[1]'] = 'Off' if (f.B.line5bi or f.B.line5bii) else 'No'
    pdf['c2_15_0_[0]'] = 'Yes' if f.B.line6 else 'Off'
    pdf['c2_15_0_[1]'] = 'Off' if f.B.line6 else 'No'
    pdf['c2_11_0_[0]'] = 'Yes' if f.B.line7 else 'Off'
    pdf['p2-t22[0]'] = zstr(f.B.line8)
    pdf['p2-t23[0]'] = zstr(f.B.line9)
    pdf['c2_100_0_[0]'] = 'Yes' if f.B.line10 else 'Off'
    pdf['c2_101_0_[0]'] = 'Yes' if f.B.line11 else 'Off'
    pdf['c2_101_0_[1]'] = 'Off' if f.B.line11 else 'No'
    pdf['p2-t22[0]'] = zstr(f.B.line11)
    pdf['c2_13_0_[0]'] = 'Yes' if f.B.line12 else 'Off'
    pdf['c2_13_0_[1]'] = 'Off' if f.B.line12 else 'No'
    pdf['c2_80_0_[0]'] = 'Yes' if f.B.line13a else 'Off'
    pdf['c2_80_0_[1]'] = 'Off' if f.B.line13a else 'No'
    pdf['c2_07_0_[0]'] = 'Yes' if f.B.line13b else 'Off'
    pdf['c2_07_0_[1]'] = 'Off' if f.B.line13b else 'No'

    def pair(i, value, j=None):
        if j is None:
            j = i + 1
        pdf['p3-t{}[0]'.format(i)], pdf['p3-t{}[0]'.format(j)] = zzstr(value)

    pair(100, f.K.line1)
    pair(102, f.K.line2)

    pair(104, f.K.line3a)
    pair(106, f.K.line3b)

    pair(108, f.K.line3c)
    pair(110, f.K.line4)
    pair(112, f.K.line5a)

    pair(114, f.K.line5b)

    pair(116, f.K.line6)
    pair(118, f.K.line7)
    pair(120, f.K.line8a)

    pair(122, f.K.line8b)
    pair(124, f.K.line8c)

    pair(126, f.K.line9)
    pdf['p3-t128[0]'] = zstr(f.K.line10_type)
    pair(129, f.K.line10)
    pair(131, f.K.line11)
    pair(133, f.K.line12a)
    pair(135, f.K.line12b)
    pdf['p3-t137[0]'] = zstr(f.K.line12c_type)
    pair(138, f.K.line12c)
    pdf['p3-t140[0]'] = zstr(f.K.line12d_type)
    pair(141, f.K.line12d, j=145)
    pair(146, f.K.line13a)
    pair(148, f.K.line13b)
    pair(150, f.K.line13c)
    pdf['p3-t152[0]'] = zstr(f.K.line13d_type)
    pair(153, f.K.line13d)
    pdf['p3-t155[0]'] = zstr(f.K.line13e_type)
    pair(156, f.K.line13e)
    pair(158, f.K.line13f)
    pdf['p3-t160[0]'] = zstr(f.K.line13g_type)
    pair(161, f.K.line13g)

    pdf['p3-t163[0]'] = zstr(f.K.line14a)
    pair(164, f.K.line14b)
    pair(166, f.K.line14c)
    pair(168, f.K.line14d)
    pair(170, f.K.line14e)
    pair(172, f.K.line14f)
    pair(174, f.K.line14g)
    pair(176, f.K.line14h)
    pair(178, f.K.line14i)
    pair(180, f.K.line14j)
    pair(182, f.K.line14k)
    pair(184, f.K.line14l)
    pair(186, f.K.line14m)
    if f.K.line14l:
        pdf['c3_01_0_[0]'] = 'A' if f.K.line14n_accounting == 'a' else 'Off'
        pdf['c3_01_0_[1]'] = 'B' if f.K.line14n_accounting == 'b' else 'Off'

    pair(188, f.K.line15a)
    pair(190, f.K.line15b)
    pair(192, f.K.line15c)
    pair(194, f.K.line15d)
    pair(196, f.K.line15e)
    pair(198, f.K.line15f)

    pair(200, f.K.line16a)
    pair(202, f.K.line16b)
    pair(204, f.K.line16c) # penalties, fines; half of meals
    pair(206, f.K.line16d)
    pair(208, f.K.line16e)

    def pair(i, value):
        pdf['p4-t{}[0]'.format(i)], pdf['p4-t{}[0]'.format(i+1)] = zzstr(value)

    pair(100, f.K.line17a)
    pair(102, f.K.line17b)
    pair(104, f.K.line17c)

    pair(106, f.K.line18)

    # TODO: Schedule L
    # TODO: Schedule M-1

    def put(i, value):
        pdf['p5-t{:03}[0]'.format(i)] = zstr(value)

    put(116, f.M2.line1a)
    put(117, f.M2.line1b)
    put(118, f.M2.line1c)

    put(119, f.M2.line2a)

    put(120, f.M2.line3a)
    put(121, f.M2.line3b)

    put(122, f.M2.line4a)

    put(123, f.M2.line5a)
    put(124, f.M2.line5b)

    put(125, f.M2.line6a)
    put(126, f.M2.line6b)
    put(127, f.M2.line6c)

    put(128, f.M2.line7a)
    put(129, f.M2.line7b)
    put(130, f.M2.line7c)

    put(131, f.M2.line8a)
    put(132, f.M2.line8b)
    put(133, f.M2.line8c)
