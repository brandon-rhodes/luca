"""Build an OFX XML request."""

from datetime import datetime
from lxml.builder import E

def build_sonrq(userid, userpass, fi, app, language='ENG'):
    return E.SONRQ(
        E.DTCLIENT(datetime.now().strftime('%Y%m%d%H%M%S')),
        E.USERID(userid),
        E.USERPASS(userpass),
        E.LANGUAGE(language),
        E.FI(
            E.ORG(fi.org),
            E.FID(fi.fid),
            ),
        E.APPID(app.appid),
        E.APPVER(app.appver),
        )

def build_acctreq(dtacctup='19700101000000'):
    return E.ACCTINFOTRNRQ(
        E.TRNUID('1'),
        E.ACCTINFORQ(
            E.DTACCTUP(dtacctup),
            )
        )

def build_bankacctfrom(bankid, acctid, accttype):
    return E.BANKACCTFROM(
        E.BANKID(bankid), # Routing transit or other FI
        E.ACCTID(acctid),
        E.ACCTTYPE(accttype),
        )

def build_stmttrnrq(bankacctfrom):
    return E.STMTTRNRQ(
        E.TRNUID('1'),
        E.STMTRQ(
            bankacctfrom,
            E.INCTRAN(
                E.INCLUDE('Y')
                ),
            #E.INCTRANIMG('Y')
            ),
        )

def build_ccstmtrq(acctid):
    return E.CCSTMTTRNRQ(
        E.TRNUID('1'),
        E.CCSTMTRQ(
            E.CCACCTFROM(
                E.ACCTID(acctid),
                ),
            E.INCTRAN(
                #E.DTSTART('20090101'),
                #E.DTEND('20100410'),
                E.INCLUDE('Y'),
                ),
            ),
        )
