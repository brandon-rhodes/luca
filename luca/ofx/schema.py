"""Build an OFX XML request."""

from datetime import datetime

class ElementMaker(object):
    """Each attribute lookup creates an `_Element`.

    >>> E = ElementMaker(False)
    >>> E.bold('Thomas Paine')
    '<bold>Thomas Paine</bold>'

    """
    def __init__(self, use_sgml):
        self.use_sgml = use_sgml

    def __getattr__(self, name):
        return _Element(name, self.use_sgml)

class _Element(object):
    """An element: when called, returns arguments wrapped in <tag></tag>.

    Normally `_Element` instances are not created manually, but by an
    instance of the `_E` convenience factory.  If `use_sgml` is false,
    then both the beginning and end tags are always added.

    >>> _Element('date', False)('2012')
    '<date>2012</date>'
    >>> _Element('date', False)('<year>2012</year>')
    '<date><year>2012</year></date>'

    But if `use_sgml` is true, then simple strings which do not
    themselves contain elements will lack a closing tag, but larger
    elements will continue to include a closing tag.

    >>> _Element('date', True)('2012')
    '<date>2012'
    >>> _Element('date', True)('<year>2012')
    '<date><year>2012</date>'

    """
    def __init__(self, name, use_sgml):
        self.name = name
        self.use_sgml = use_sgml

    def __call__(self, *args):
        text = ''.join(str(a) for a in args)
        if self.use_sgml and not text.startswith('<'):
            return '<{0}>{1}'.format(self.name, text)
        else:
            return '<{0}>{1}</{0}>'.format(self.name, text)

def build_sonrq(E, userid, userpass, fi, app, language='ENG'):
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

def build_acctreq(E, dtacctup='19700101000000'):
    return E.ACCTINFOTRNRQ(
        E.TRNUID('1'),
        E.ACCTINFORQ(
            E.DTACCTUP(dtacctup),
            )
        )

def build_bankacctfrom(E, bankid, acctid, accttype):
    return E.BANKACCTFROM(
        E.BANKID(bankid), # Routing transit or other FI
        E.ACCTID(acctid),
        E.ACCTTYPE(accttype),
        )

def build_stmttrnrq(E, bankacctfrom):
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

def build_ccstmtrq(E, ccacctfrom):
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

def build_invstmttrnrq(E, invacctfrom):
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
