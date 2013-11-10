title = (u'Form W-9: Request for Taxpayer Identification Number'
         ' and Certification')
versions = u'2011',


def defaults(form):
    f = form
    f.name = ''
    f.business_name = ''
    f.classification = ''
    f.classification_llc = ''
    f.classification_other = ''
    f.is_exempt = False
    f.street = ''
    f.city_state_zip = ''
    f.requesters_name_and_address = ''
    f.account_numbers = ''
    f.tin = ''
    f.date = ''


def fill_out(form, pdf):
    f = form
    pdf.load('us.fw9--{}.pdf'.format(f.form_version))

    pdf['topmostSubform[0].Page1[0].c1_01[0]'] = '8' if f.is_exempt else 'Off'

    pdf.pattern = 'f1_{:02}_0_[0]'

    pdf[1] = f.name
    pdf[2] = f.business_name
    pdf[18] = f.classification_llc
    pdf[50] = f.classification_other
    pdf[4] = f.street
    pdf[5] = f.city_state_zip
    pdf[6] = f.requesters_name_and_address
    pdf[7] = f.account_numbers
    #pdf[8] = f.name

    pdf.pattern = 'topmostSubform[0].Page1[0].FedClassification[0].c1_01[{}]'

    pdf[0] = '1' if f.classification == 'Individual/sole proprietor' else 'Off'
    pdf[1] = '2' if f.classification == 'C Corporation' else 'Off'
    pdf[2] = '3' if f.classification == 'S Corporation' else 'Off'
    pdf[3] = '4' if f.classification == 'Partnership' else 'Off'
    pdf[4] = '5' if f.classification == 'Trust/estate' else 'Off'
    pdf[5] = '6' if f.classification == 'LLC' else 'Off'
    pdf[6] = '7' if f.classification == 'Other' else 'Off'

    fields = f.tin.split('-')
    if len(fields) == 3:
        pdf.pattern = 'topmostSubform[0].Page1[0].social[0].f1_{:02}[0]'
        pdf[7], pdf[8], pdf[9] = fields
    elif len(fields) == 2:
        pdf.pattern = ('topmostSubform[0].Page1[0]'
                       '.Employeridentifi[0].f1_{:02}[0]')
        pdf[10], pdf[11] = fields
