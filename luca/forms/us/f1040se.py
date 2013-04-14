from luca.forms.formlib import Form
from luca.kit import Decimal, cents

title = u"Supplemental Income and Loss"
filename = 'f1040se--2012.pdf'
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

def fill(form, fields):
    f = form

    fields['p1-t1['] = [f.name, f.name]
    fields['t2['] = [f.ssn, f.ssn]

    yesno(f.is_1099_required, fields['c1_01[0]'])
    yesno(f.is_1099_required, fields['c1_03[0]'])

    # Part I: Income or Loss From Rental Real Estate and Royalties

    for i, subform_name in enumerate('ABC'):
        sub = getattr(form.Part_I, subform_name)
        cols = slice(2*i, 2*(i+1))

        fields['Pg1Table1a['][i] = sub.address
        fields['Pg1Table1b['][i] = sub.type

        row = fields['Table_Line2[0].{}[0]'.format(subform_name.lower())]
        row[0] = z(sub.fair_rental_days)
        row[1] = z(sub.personal_use_days)
        row[2] = sub.qjv

        for j in range(3, 23):
            pattern = 'Line{}['.format(j)
            value = getattr(sub, 'line{}'.format(j))
            fields[pattern][cols] = zz(value)

    fields['Page1[0].p1-t505['], fields['Page1[0].p1-t504['] = zz(f.line23a)
    fields['Page1[0].p1-t176['], fields['Page1[0].p1-t177['] = zz(f.line23b)
    fields['Page1[0].p1-t508['], fields['Page1[0].p1-t509['] = zz(f.line23c)
    fields['Page1[0].p1-t510['], fields['Page1[0].p1-t511['] = zz(f.line23d)
    fields['Page1[0].p1-t512['], fields['Page1[0].p1-t513['] = zz(f.line23e)

    fields['Page1[0].p1-t507['], fields['Page1[0].p1-t506['] = zz(f.line24)
    fields['Page1[0].p1-t178['], fields['Page1[0].p1-t179['] = zz(-f.line25)
    fields['Page1[0].p1-t180['], fields['Page1[0].p1-t181['] = zz(f.line26)

    # Part II: Income or Loss From Partnerships and S Corporations

    table = fields['Line28TableA-E']

    for i, letter in enumerate('ABCD'):
        row = table[5*i : 5*(i+1)]
        sub = getattr(f.Part_II, letter)
        row[0] = sub.name
        row[1] = sub.type
        row[2] = '1' if sub.is_foreign else 'Off'
        row[3] = sub.ein
        row[4] = '1' if sub.any_not_at_risk else 'Off'

    table = fields['Line28TableF-J']

    for i, letter in enumerate('ABCD'):
        row = table[10*i : 10*(i+1)]
        sub = getattr(f.Part_II, letter)
        row[0:2] = zz(sub.f)
        row[2:4] = zz(sub.g)
        row[4:6] = zz(sub.h)
        row[6:8] = zz(sub.i)
        row[8:10] = zz(sub.j)

    fields['.p2-t57['], fields['.p2-t58['] = zz(f.line29ag)
    fields['.p2-t59['], fields['.p2-t60['] = zz(f.line29aj)

    fields['.p2-t61['], fields['.p2-t62['] = zz(f.line29bf)
    fields['.p2-t63['], fields['.p2-t64['] = zz(f.line29bh)
    fields['.p2-t65['], fields['.p2-t66['] = zz(f.line29bi)

    fields['.p2-t67['], fields['.p2-t68['] = zz(f.line30)
    fields['.p2-t69['], fields['.p2-t70['] = zz(f.line31)
    fields['.p2-t71['], fields['.p2-t72['] = zz(f.line32)

    # TODO: Part III
    # TODO: Part IV

    fields['.p2-t117['], fields['.p2-t118['] = zz(f.line40)
    fields['.p2-t119['], fields['.p2-t120['] = zz(f.line41)
    fields['.p2-t121['], fields['.p2-t122['] = zz(f.line42)
    fields['.p2-t123['], fields['.p2-t124['] = zz(f.line43)

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
