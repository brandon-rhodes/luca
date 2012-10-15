"""Build an OFX XML request."""

import re
import urllib2

from .schema import (ElementMaker, build_sonrq, build_acctreq,
                     build_stmttrnrq, build_ccstmtrq, build_invstmttrnrq)

headers = {
    211: '''\
<?xml version="1.0"?>
<?OFX OFXHEADER="200" VERSION="211" SECURITY="NONE"\
 OLDFILEUID="NONE" NEWFILEUID="NONE"?>
''',
    103: '''\
OFXHEADER:100
DATA:OFXSGML
VERSION:103
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE

''',
    }

blankline = '\n'

def element_maker_for(institution):
    use_sgml = institution.version < 200
    return ElementMaker(use_sgml)

def _download(institution, username, password, messages):

    E = element_maker_for(institution)
    sonrq = build_sonrq(E, username, password, institution, institution.app)

    ofx = E.OFX(E.SIGNONMSGSRQV1(sonrq), *messages)

    data = headers[institution.version] + ofx
    data = data.replace('\n', '\r\n')
    r = urllib2.Request(institution.url, data)
    r.add_header('Content-Type', 'application/x-ofx')

    try:
        u = urllib2.urlopen(r)
    except urllib2.HTTPError as e:
        print '-----------'
        for key, value in r.header_items():
            print '{}: {}'.format(key, value)
        print
        print r.get_data()
        print '-----------'
        print e
        print e.headers
        print e.read()
        print '-----------'
        exit(1)

    try:
        return u.read()
    finally:
        u.close()

def download_accounts(institution, username, password):
    E = element_maker_for(institution)
    return _download(institution, username, password, [
            E.SIGNUPMSGSRQV1(build_acctreq(E)),
            ])

def download_activity(institution, username, password, accounts):

    def make_request(account):
        f = account.from_element

        # The First National Bank of Pandora includes an extra element
        # in its account description that it cannot then digest when the
        # BANKACCTFROM is re-submitted.
        f = re.sub(r'<ORCC.NICKNAME>[^<]*', '', f)

        if f.startswith('<BANKACCTFROM'):
            return E.BANKMSGSRQV1(build_stmttrnrq(E, f))
        elif f.startswith('<CCACCTFROM'):
            return E.CREDITCARDMSGSRQV1(build_ccstmtrq(E, f))
        elif f.startswith('<INVACCTFROM'):
            return E.INVSTMTMSGSRQV1(build_invstmttrnrq(E, f))
        else:
            raise ValueError('no idea how to wrap:', f)

    E = element_maker_for(institution)
    requests = [make_request(a) for a in accounts]
    return _download(institution, username, password, requests)
