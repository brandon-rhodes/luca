from luca.forms.formlib import Form
from luca.kit import cents, zzstr

title = u"Form 1040 Schedule E: Supplemental Income and Loss"
versions = '2012',
zero = cents(0)

def defaults(form):
    f = form
    f.ssn = ''
    f.name = ''
    f.is_1099_required = False
    f.is_1099_filed = False

    f.Part_I = Form()
    f.Part_II = Form()

    for letter in 'ABC':
        setattr(f.Part_I, letter, Form())
        sub = getattr(f.Part_I, letter)
        sub.address = ''
        sub.type = ''
        sub.fair_rental_days = 0
        sub.personal_use_days = 0
        sub.qjv = ''
        for i in range(3, 20):
            setattr(sub, 'line%d' % i, zero)

    for letter in 'ABCD':
        setattr(f.Part_II, letter, Form())
        sub = getattr(f.Part_II, letter)
        sub.name = ''
        sub.type = ''
        sub.is_foreign = False
        sub.ein = ''
        sub.any_not_at_risk = False
        for col in 'fghij':
            setattr(sub, col, zero)

    f.line40 = zero
    f.line42 = zero
    f.line43 = zero

def compute(form):
    f = form

    # Part I: Income or Loss From Rental Real Estate and Royalties

    subforms = [ getattr(f.Part_I, letter) for letter in 'ABC' ]

    for sub in subforms:
        expenses = zero
        for j in range(5, 19):
            expenses += getattr(sub, 'line{}'.format(j))

        sub.line20 = expenses
        sub.line21 = sub.line3 + sub.line4 - expenses
        sub.line22 = zero  # TODO: loss after limitation from Form 8582

    f.line23a = sum(sub.line3 for sub in subforms)
    f.line23b = sum(sub.line4 for sub in subforms)
    f.line23c = sum(sub.line12 for sub in subforms)
    f.line23d = sum(sub.line18 for sub in subforms)
    f.line23e = sum(sub.line20 for sub in subforms)

    f.line24 = sum(max(sub.line21, zero) for sub in subforms)
    f.line25 = sum(min(sub.line21, zero) for sub in subforms)
    f.line26 = f.line24 + f.line25

    # Part II: Income or Loss From Partnerships and S Corporations

    subforms = [ getattr(f.Part_II, letter) for letter in 'ABCD' ]

    f.line29ag = sum(sub.g for sub in subforms)
    f.line29aj = sum(sub.j for sub in subforms)

    f.line29bf = sum(sub.f for sub in subforms)
    f.line29bh = sum(sub.h for sub in subforms)
    f.line29bi = sum(sub.i for sub in subforms)

    f.line30 = f.line29ag + f.line29aj
    f.line31 = f.line29bf + f.line29bh + f.line29bi
    f.line32 = f.line30 - f.line31

    # TODO: Part III

    f.line37 = zero

    # TODO: Part IV

    f.line39 = zero

    # Part V: Summary

    f.line41 = f.line26 + f.line32 + f.line37 + f.line39 + f.line40

def fill_out(form, pdf):
    f = form
    pdf.load('us.f1040se--{}.pdf'.format(f.form_version))

    pdf['p1-t1['] = [f.name, f.name]
    pdf['t2['] = [f.ssn, f.ssn]

    pdf['c1_01['] = yesno(f.is_1099_required)
    pdf['c1_03['] = yesno(f.is_1099_required)

    # Part I: Income or Loss From Rental Real Estate and Royalties

    subforms = [getattr(form.Part_I, letter) for letter in 'ABC']

    pdf['Pg1Table1a'] = [s.address for s in subforms]
    pdf['Pg1Table1b'] = [str(s.type) for s in subforms]
    pdf['Table_Line2[0]'] = concat(
            [z(s.fair_rental_days), z(s.personal_use_days), z(s.qjv)]
            for s in subforms
            )

    pdf.pattern = 'Pg1Table2[0].Line{}[0]'

    for j in range(3, 5):
        attr = 'line{}'.format(j)
        pdf[j] = concat(zzstr(getattr(s, attr)) for s in subforms)

    pdf.pattern = 'Pg1Table3[0].Line{}[0]'

    for j in range(5, 23):
        attr = 'line{}'.format(j)
        pdf[j] = concat(zzstr(getattr(s, attr)) for s in subforms)

    pdf.pattern = 'Page1[0].p1-t{}['

    pdf[505], pdf[504] = zzstr(f.line23a)
    pdf[176], pdf[177] = zzstr(f.line23b)
    pdf[508], pdf[509] = zzstr(f.line23c)
    pdf[510], pdf[511] = zzstr(f.line23d)
    pdf[512], pdf[513] = zzstr(f.line23e)

    pdf[507], pdf[506] = zzstr(f.line24)
    pdf[178], pdf[179] = zzstr(-f.line25)
    pdf[180], pdf[181] = zzstr(f.line26)

    # Part II: Income or Loss From Partnerships and S Corporations

    pdf.pattern = '{}'

    subforms = [getattr(f.Part_II, letter) for letter in 'ABCD']

    pdf['Line28TableA-E[0]'] = concat(
        [s.name, s.type, onoff(s.is_foreign), s.ein, onoff(s.any_not_at_risk)]
        for s in subforms
        )

    pdf['Line28TableF-J[0]'] = concat(
        concat([zzstr(s.f), zzstr(s.g), zzstr(s.h), zzstr(s.i), zzstr(s.j)])
        for s in subforms
        )

    pdf['.p2-t57['], pdf['.p2-t58['] = zzstr(f.line29ag)
    pdf['.p2-t59['], pdf['.p2-t60['] = zzstr(f.line29aj)

    pdf['.p2-t61['], pdf['.p2-t62['] = zzstr(f.line29bf)
    pdf['.p2-t63['], pdf['.p2-t64['] = zzstr(f.line29bh)
    pdf['.p2-t65['], pdf['.p2-t66['] = zzstr(f.line29bi)

    pdf['.p2-t67['], pdf['.p2-t68['] = zzstr(f.line30)
    pdf['.p2-t69['], pdf['.p2-t70['] = zzstr(f.line31)
    pdf['.p2-t71['], pdf['.p2-t72['] = zzstr(f.line32)

    # TODO: Part III
    # TODO: Part IV

    pdf['.p2-t117['], pdf['.p2-t118['] = zzstr(f.line40)
    pdf['.p2-t119['], pdf['.p2-t120['] = zzstr(f.line41)
    pdf['.p2-t121['], pdf['.p2-t122['] = zzstr(f.line42)
    pdf['.p2-t123['], pdf['.p2-t124['] = zzstr(f.line43)

# General-purpose functions that will probably be factored out of here:

def concat(lists):
    return sum(lists, [])

def yesno(value):
    return ('Yes' if value else 'Off', 'Off' if value else 'No')

def onoff(value):
    return '1' if value else 'Off'

def z(value):
    if not value:
        return u''
    return unicode(value)
