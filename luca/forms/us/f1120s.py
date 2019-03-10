# TODO: Table 4a and 4b
# TODO: Schedule L
# TODO: Schedule M-1
from luca.forms.formlib import Form
from luca.kit import validate, zero, zstr, zzstr


title = u'Form 1120S: U.S. Income Tax Return for an S Corporation'
versions = u'2012', u'2013', u'2014'

# Note that only a bare minimum of fields are supported for 2010: those
# I needed for a quick filing of an amended return.  If you also need to
# make emergency use of the form for that year, uncomment the following
# line:
#
# versions = versions + (u'2010',)


def defaults(form):
    if form.form_version < u'2018':
        return defaults_pre_2018(form)

    f = form

    f.beginning_date = ''
    f.ending_date = ''
    f.ending_year = ''
    f.ein = ''
    f.name = ''
    f.street = ''
    f.city_state_zip = ''

    f.lineA = f.lineB = ''
    f.lineC = False
    f.lineE = ''
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
    f.B.line2_product_or_service = ''
    f.B.line3 = False
    # 4a and 4b tables go here if we ever implement them
    f.B.line4a = []
    f.B.line4b = []
    f.B.line5ai = 0
    f.B.line5aii = 0
    f.B.line5bi = 0
    f.B.line5bii = 0
    f.B.line6 = False
    f.B.line7 = False
    f.B.line8 = zero
    f.B.line9 = False
    f.B.line10 = True
    f.B.line11 = True
    f.B.line12 = False
    f.B.line13 = False
    f.B.line14a = False
    f.B.line14b = None
    f.B.line15 = False

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

def defaults_pre_2018(form):
    f = form

    f.beginning_date = ''
    f.ending_date = ''
    f.ending_year = ''
    f.ein = ''
    f.name = ''
    f.street = ''
    f.city_state_zip = ''

    f.lineA = f.lineB = ''
    f.lineC = False
    f.lineE = ''
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
    f.B.line2_product_or_service = ''
    f.B.line3 = False
    # 4a and 4b tables go here if we ever implement them
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
    validate.year(int(f.form_version))

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
    if form.form_version < u'2018':
        return fill_out_pre_2018(form, pdf)

    f = form
    pdf.load('us.f1120s--{}.pdf'.format(f.form_version))

    last_split = [0]

    def split(value, i=None, j=None):
        if i is None:
            i = last_split[0] + 2
        last_split[0] = i
        if j is None:
            j = i + 1
        pdf[i], pdf[j] = zzstr(value)

    pdf.pattern = '.f1_{}[0]'

    pdf[1] = f.beginning_date
    pdf[2] = f.ending_date
    pdf[3] = f.ending_year

    pdf[4] = f.name
    pdf[5] = f.street
    pdf[6] = f.city_state_zip
    pdf[7] = f.lineA

    pdf[8] = f.ein
    pdf[9] = f.lineE
    split(f.lineF, 10)

    pdf[12] = str(f.lineI)
    split(f.line1a, 13)
    split(f.line1b)
    split(f.line1c)
    for i in range(2, 21+1):
        split(f['line', i])
    split(f.line22a)
    split(f.line22b)
    split(f.line22c)
    split(f.line23a)
    split(f.line23b)
    split(f.line23c)
    split(f.line23d)
    split(f.line24)
    split(f.line25)
    split(f.line26)
    split(f.line27_credited)
    split(f.line27)

    pdf.pattern = 'ABC[0].f1_{}[0]'

    pdf[8] = f.lineB  # same name as line D

    pdf.pattern = 'topmostSubform[0].Page1[0].{}'

    pdf['c1_01_0_[0]'] = 'Yes' if f.lineC else 'Off'
    pdf['c1_2[0]'] = '1' if f.lineG else 'Off'
    pdf['c1_2[1]'] = 'Off' if f.lineG else '2'

    for i in range(1, 5+1):
        checked = str(i) in f.lineH
        pdf['c1_0{}_0_[0]'.format(i + 2)] = 'Yes' if checked else 'Off'

    pdf['p1_t85[0]'] = f.signer_title  # note the underscore!
    pdf['c1_9_0_[0]'] = 'Yes' if f.discuss else 'Off'
    pdf['c1_9_0_[1]'] = 'Off' if f.discuss else 'No'

    pdf.pattern = 'topmostSubform[0].Page2[0].{}'

    pdf['c2_01_0_[0]'] = '1' if f.B.line1 == 'a' else 'Off'
    pdf['c2_01_0_[1]'] = '2' if f.B.line1 == 'b' else 'Off'
    if f.B.line1 not in ('a', 'b'):
        pdf['c2_01_0_[2]'] = '3'
        pdf['f2_1[0]'] = f.B.line1
    pdf['f2_2[0]'] = f.B.line2_activity
    pdf['f2_3[0]'] = f.B.line2_product_or_service
    pdf['c2_02[0]'] = '1' if f.B.line3 else 'Off'
    pdf['c2_02[1]'] = 'Off' if f.B.line3 else '2'
    pdf['c2_03[0]'] = '1' if f.B.line4a else 'Off'
    pdf['c2_03[1]'] = 'Off' if f.B.line4a else '2'
    pdf['c2_04[0]'] = '1' if f.B.line4b else 'Off'
    pdf['c2_04[1]'] = 'Off' if f.B.line4b else '2'
    pdf['c2_05[0]'] = '1' if (f.B.line5ai or f.B.line5aii) else 'Off'
    pdf['c2_05[1]'] = 'Off' if (f.B.line5ai or f.B.line5aii) else '2'
    pdf['c2_06[0]'] = '1' if (f.B.line5bi or f.B.line5bii) else 'Off'
    pdf['c2_06[1]'] = 'Off' if (f.B.line5bi or f.B.line5bii) else '2'

    def truefalse(value, field, yes_suffix='[0]', no_suffix='[1]'):
        pdf[field + yes_suffix] = '1' if value else 'Off'
        pdf[field + no_suffix] = 'Off' if value else '2'

    truefalse(f.B.line6, 'c2_06')
    truefalse(f.B.line7, 'c2_07')
    truefalse(f.B.line9, 'c2_09')
    truefalse(f.B.line10, 'c2_10')
    truefalse(f.B.line11, 'c2_11')

    pdf.pattern = 'topmostSubform[0].Page3[0].schb[0].{}'

    truefalse(f.B.line12, 'c3_1')
    truefalse(f.B.line13, 'c3_2')
    truefalse(f.B.line14a, 'c3_3')
    truefalse(f.B.line14b, 'c3_4')
    truefalse(f.B.line15, 'c3_5')

    pdf.pattern = 'f3_{}[0]'

    split(f.K.line1, 3)
    split(f.K.line2)

    split(f.K.line3a)
    split(f.K.line3b)

    split(f.K.line3c)
    split(f.K.line4)
    split(f.K.line5a)

    split(f.K.line5b)

    split(f.K.line6)
    split(f.K.line7)
    split(f.K.line8a)

    split(f.K.line8b)
    split(f.K.line8c)

    split(f.K.line9)
    pdf[31] = zstr(f.K.line10_type)
    split(f.K.line10, 32)

    split(f.K.line11)
    split(f.K.line12a)
    split(f.K.line12b)
    # several fields skipped that I don't need

    pdf.pattern = 'f4_{}[0]'

    split(f.K.line16c, 17) # half of meals
    split(f.K.line18, 29)

    # TODO: Schedule L
    # TODO: Schedule M-1

    pdf.pattern = 'f5_{}[0]'

    pdf[19] = zstr(f.M2.line1a)
    pdf[20] = zstr(f.M2.line1b)
    pdf[21] = zstr(f.M2.line1c)

    pdf[23] = zstr(f.M2.line2a)

    pdf[24] = zstr(f.M2.line3a)
    #pdf[121] = zstr(f.M2.line3b)

    pdf[26] = zstr(f.M2.line4a)

    pdf[27] = zstr(f.M2.line5a)
    #pdf[124] = zstr(f.M2.line5b)

    pdf[29] = zstr(f.M2.line6a)
    pdf[30] = zstr(f.M2.line6b)
    pdf[31] = zstr(f.M2.line6c)

    pdf[33] = zstr(f.M2.line7a)
    pdf[34] = zstr(f.M2.line7b)
    pdf[35] = zstr(f.M2.line7c)

    pdf[37] = zstr(f.M2.line8a)
    pdf[38] = zstr(f.M2.line8b)
    pdf[29] = zstr(f.M2.line8c)

def fill_out_pre_2018(form, pdf):
    f = form
    pdf.load('us.f1120s--{}.pdf'.format(f.form_version))

    def split(i, value, j=None):
        if j is None:
            j = i + 1
        pdf[i], pdf[j] = zzstr(value)

    pdf.pattern = '.p1-t{}[0]'

    pdf[1] = f.beginning_date
    pdf[2] = f.ending_date
    pdf[3] = f.ending_year

    pdf[4] = f.name
    pdf[5] = f.street
    pdf[6] = f.city_state_zip
    pdf[7] = f.lineA
    pdf[8] = f.lineB

    pdf[9] = f.ein
    pdf[11] = f.lineE
    split(12, f.lineF)

    pdf[14] = str(f.lineI)
    split(15, f.line1a)
    split(17, f.line1b)
    split(19, f.line1c)
    for i in range(2, 21+1):
        split(2*i + 17, f['line', i])
    split(61, f.line22a)
    split(63, f.line22b)
    split(65, f.line22c)
    split(67, f.line23a)
    split(69, f.line23b)
    split(71, f.line23c)
    split(73, f.line23d)
    split(75, f.line24)
    split(77, f.line25)
    split(79, f.line26)
    split(81, f.line27_credited)
    split(83, f.line27)

    pdf.pattern = 'topmostSubform[0].Page1[0].{}'

    pdf['ABC[0].c1_01_0_[0]'] = 'Yes' if f.lineC else 'Off'
    pdf['c1_02_0_[0]'] = 'Yes' if f.lineG else 'Off'
    pdf['c1_02_0_[1]'] = 'Off' if f.lineG else 'No'

    for i in range(1, 5+1):
        checked = str(i) in f.lineH
        pdf['c1_0{}_0_[0]'.format(i + 2)] = 'Yes' if checked else 'Off'

    pdf['p1_t85[0]'] = f.signer_title  # note the underscore!
    pdf['c1_9_0_[0]'] = 'Yes' if f.discuss else 'Off'
    pdf['c1_9_0_[1]'] = 'Off' if f.discuss else 'No'

    pdf.pattern = 'topmostSubform[0].Page2[0].{}'

    pdf['c2_01_0_[0]'] = 'A' if f.B.line1 == 'a' else 'Off'
    pdf['c2_01_0_[1]'] = 'B' if f.B.line1 == 'b' else 'Off'
    if f.B.line1 not in ('a', 'b'):
        pdf['c2_01_0_[2]'] = 'C'
        pdf['p2-t19[0]'] = f.B.line1
    if f.form_version >= u'2014':
        pdf['f2_2[0]'] = f.B.line2_activity
        pdf['f2_3[0]'] = f.B.line2_product_or_service
    else:
        pdf['p2-t20'] = f.B.line2_activity
        pdf['p2-t21'] = f.B.line2_product_or_service
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
    pdf['p2-t22[1]'] = zstr(f.B.line11)
    pdf['c2_13_0_[0]'] = 'Yes' if f.B.line12 else 'Off'
    pdf['c2_13_0_[1]'] = 'Off' if f.B.line12 else 'No'
    if f.form_version == u'2012':
        pdf['c2_80_0_[0]'] = 'Yes' if f.B.line13a else 'Off'
        pdf['c2_80_0_[1]'] = 'Off' if f.B.line13a else 'No'
    elif f.form_version == u'2016':
        pdf['c2_300[0]'] = 'Yes' if f.B.line13a else 'Off'
        pdf['c2_300[1]'] = 'Off' if f.B.line13a else 'No'
    else:
        pdf['c2_13a_0_[0]'] = 'Yes' if f.B.line13a else 'Off'
        pdf['c2_13a_0_[1]'] = 'Off' if f.B.line13a else 'No'
    pdf['c2_07_0_[0]'] = 'Yes' if f.B.line13b else 'Off'
    pdf['c2_07_0_[1]'] = 'Off' if f.B.line13b else 'No'

    if f.form_version == u'2010':
        pdf.pattern = '.p2-t{}[0]'

        split(24, f.K.line1)
        split(34, f.K.line4)
        split(55, f.K.line11)
        split(125, f.K.line16c)
        split(127, f.K.line16d)
        split(131, f.K.line17a)
        split(137, f.K.line18)

        pdf.pattern = '.p4-t{}[0]'

        pdf[87] = zstr(f.M2.line1a)
        pdf[90] = zstr(f.M2.line2a)
        pdf[91] = zstr(f.M2.line3a)
        pdf[93] = zstr(f.M2.line4a)
        pdf[94] = zstr(f.M2.line5a)
        pdf[96] = zstr(f.M2.line6a)
        pdf[99] = zstr(f.M2.line7a)
        pdf[102] = zstr(f.M2.line8a)

    else:
        pdf.pattern = '.p3-t{}[0]'

        split(100, f.K.line1)
        split(102, f.K.line2)

        split(104, f.K.line3a)
        split(106, f.K.line3b)

        split(108, f.K.line3c)
        split(110, f.K.line4)
        split(112, f.K.line5a)

        split(114, f.K.line5b)

        split(116, f.K.line6)
        split(118, f.K.line7)
        split(120, f.K.line8a)

        split(122, f.K.line8b)
        split(124, f.K.line8c)

        split(126, f.K.line9)
        pdf[128] = zstr(f.K.line10_type)
        split(129, f.K.line10)
        split(131, f.K.line11)
        split(133, f.K.line12a)
        split(135, f.K.line12b)
        pdf[137] = zstr(f.K.line12c_type)
        split(138, f.K.line12c)
        pdf[140] = zstr(f.K.line12d_type)
        split(141, f.K.line12d, j=145)
        split(146, f.K.line13a)
        split(148, f.K.line13b)
        split(150, f.K.line13c)
        pdf[152] = zstr(f.K.line13d_type)
        split(153, f.K.line13d)
        pdf[155] = zstr(f.K.line13e_type)
        split(156, f.K.line13e)
        split(158, f.K.line13f)
        pdf[160] = zstr(f.K.line13g_type)
        split(161, f.K.line13g)

        pdf[163] = zstr(f.K.line14a)
        split(164, f.K.line14b)
        split(166, f.K.line14c)
        split(168, f.K.line14d)
        split(170, f.K.line14e)
        split(172, f.K.line14f)
        split(174, f.K.line14g)
        split(176, f.K.line14h)
        split(178, f.K.line14i)
        split(180, f.K.line14j)
        split(182, f.K.line14k)
        split(184, f.K.line14l)
        split(186, f.K.line14m)

        split(188, f.K.line15a)
        split(190, f.K.line15b)
        split(192, f.K.line15c)
        split(194, f.K.line15d)
        split(196, f.K.line15e)
        split(198, f.K.line15f)

        split(200, f.K.line16a)
        split(202, f.K.line16b)
        split(204, f.K.line16c) # penalties, fines; half of meals
        split(206, f.K.line16d)
        split(208, f.K.line16e)

        pdf.pattern = '{}'

        if f.K.line14l:
            pdf['c3_01_0_[0]'] = 'A' if f.K.line14n_accounting == 'a' else 'Off'
            pdf['c3_01_0_[1]'] = 'B' if f.K.line14n_accounting == 'b' else 'Off'

        pdf.pattern = 'p4-t{}[0]'

        split(100, f.K.line17a)
        split(102, f.K.line17b)
        split(104, f.K.line17c)

        split(106, f.K.line18)

        # TODO: Schedule L
        # TODO: Schedule M-1

        pdf.pattern = 'p5-t{:03}[0]'

        pdf[116] = zstr(f.M2.line1a)
        pdf[117] = zstr(f.M2.line1b)
        pdf[118] = zstr(f.M2.line1c)

        pdf[119] = zstr(f.M2.line2a)

        pdf[120] = zstr(f.M2.line3a)
        pdf[121] = zstr(f.M2.line3b)

        pdf[122] = zstr(f.M2.line4a)

        pdf[123] = zstr(f.M2.line5a)
        pdf[124] = zstr(f.M2.line5b)

        pdf[125] = zstr(f.M2.line6a)
        pdf[126] = zstr(f.M2.line6b)
        pdf[127] = zstr(f.M2.line6c)

        pdf[128] = zstr(f.M2.line7a)
        pdf[129] = zstr(f.M2.line7b)
        pdf[130] = zstr(f.M2.line7c)

        pdf[131] = zstr(f.M2.line8a)
        pdf[132] = zstr(f.M2.line8b)
        pdf[133] = zstr(f.M2.line8c)
