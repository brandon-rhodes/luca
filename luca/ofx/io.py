"""Build an OFX XML request."""

import urllib2

from .applications import Money2007
from .schema import (E, build_sonrq, build_acctreq, build_stmttrnrq,
                     build_ccstmtrq, build_invstmttrnrq)

headers = {
    211: '''\
<?xml version="1.0"?>
<?OFX OFXHEADER="200" VERSION="211" SECURITY="NONE"
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

def _fetch(institution, username, password, messages):

    sonrq = build_sonrq(username, password, institution, Money2007)

    ofx = E.OFX(E.SIGNONMSGSRQV1(sonrq), *messages)

    data = headers[institution.version] + ofx
    data = data.replace('\n', '\r\n')

    r = urllib2.Request(institution.url, data)
    r.add_header('Content-Type', 'application/x-ofx')

    try:
        f = urllib2.urlopen(r)
    except Exception, e:
        print e
        print '-----------'
        print e.read()
        print '-----------'
        exit(1)

    response = f.read()
    f.close()
    return response

def fetch_accounts(institution, username, password):
    return _fetch(institution, username, password, [
            E.SIGNUPMSGSRQV1(build_acctreq()),
            ])

def fetch_activity(institution, username, password, accounts):

    def wrap(account):
        f = account.from_element
        if f.startswith('<BANKACCTFROM'):
            return E.BANKMSGSRQV1(build_stmttrnrq(f))
        elif f.startswith('<CCACCTFROM'):
            return E.CREDITCARDMSGSRQV1(build_ccstmtrq(f))
        elif f.startswith('<INVACCTFROM'):
            return E.INVSTMTMSGSRQV1(build_invstmttrnrq(f))
        else:
            raise ValueError('no idea how to wrap:', f)

    return _fetch(institution, username, password, [wrap(a) for a in accounts])
