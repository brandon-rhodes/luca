"""Build an OFX XML request."""

import urllib2
from lxml import etree
from lxml.builder import E

from .applications import Money2007
from .schema import (build_acctreq, build_ccstmtrq, build_sonrq,
                     build_stmttrnrq)

GENERIC_XML_HEADER = '''<?xml version="1.0"?>
<?OFX OFXHEADER="200" VERSION="211" SECURITY="NONE"
 OLDFILEUID="NONE" NEWFILEUID="NONE"?>
'''

GENERIC_103_HEADER = '''OFXHEADER:100
DATA:OFXSGML
VERSION:103
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE
'''

BLANKLINE = '\n'

def _fetch(institution, username, password, messages):

    sonrq = build_sonrq(username, password, institution, Money2007)

    ofx = E.OFX(E.SIGNONMSGSRQV1(sonrq), *messages)

    data = GENERIC_103_HEADER + BLANKLINE + etree.tostring(ofx)
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
    return _fetch(institution, username, password, [
            E.BANKMSGSRQV1(build_stmttrnrq(account.bankacctfrom))
            for account in accounts
            ])
