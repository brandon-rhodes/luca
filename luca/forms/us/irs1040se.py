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

    for c in 'ABC':
        setattr(f, c, Form())
        sub = getattr(f, c)
        sub.address = ''
        sub.type = ''
        sub.fair_rental_days = 0
        sub.personal_use_days = 0
        sub.qjv = ''
        for i in range(3, 20):
            setattr(sub, 'line%d' % i, zero)

def compute(form):
    f = form

    subforms = [ getattr(f, letter) for letter in 'ABC' ]

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

def fill(form, fields):
    f = form

    fields['p1-t1['] = [f.name, f.name]
    fields['t2['] = [f.ssn, f.ssn]

    yesno(f.is_1099_required, fields['c1_01[0]'])
    yesno(f.is_1099_required, fields['c1_03[0]'])

    for i, subform_name in enumerate('ABC'):
        sub = getattr(form, subform_name)
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
