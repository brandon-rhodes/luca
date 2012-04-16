"""Build an OFX XML request."""

from datetime import datetime

class _E(object):
    """Support `E()`: each attribute lookup creates a `_Tag`."""
    def __getattr__(self, name):
        return _Element(name)

class _Element(object):
    """An element: when called, returns arguments wrapped in <tag></tag>."""
    def __init__(self, name):
        self.name = name

    def __call__(self, *args):
        jargs = ''.join(str(a) for a in args)
        return '<{0}>{1}</{0}>'.format(self.name, jargs)

E = _E()

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
                #E.DTSTART('20090101'),
                #E.DTEND('20100410'),
                E.INCLUDE('Y')
                ),
            #E.INCTRANIMG('Y')  # TODO: support archiving check images
            ),
        )

def build_ccstmtrq(ccacctfrom):
    return E.CCSTMTTRNRQ(
        E.TRNUID('1'),
        E.CCSTMTRQ(
            ccacctfrom,
            E.INCTRAN(
                #E.DTSTART('20090101'),
                #E.DTEND('20100410'),
                E.INCLUDE('Y'),
                ),
            ),
        )

def build_invstmttrnrq(invacctfrom):
    return E.INVSTMTTRNRQ(
        E.TRNUID('1'),
        E.INVSTMTRQ(
            invacctfrom,
            E.INCTRAN(
                #E.DTSTART('20090101'),
                #E.DTEND('20100410'),
                E.INCLUDE('Y'),
                ),
            E.INCOO('N'),
            E.INCPOS(
                #E.DTASOF(...),
                E.INCLUDE('Y'),
                ),
            E.INCBAL('Y'),
            ),
        )
