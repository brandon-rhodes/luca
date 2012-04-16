import re
from decimal import Decimal
from . import types

sgmlre = re.compile(r'<(/?)([^>]+)>([^<]*)')
tag_with_text = re.compile(r'<([^>]+)>([^<]+)')

def unescape(text):
    """Replace SGML character escapes in `text` with literal character."""
    return text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

def tags(sgml, tag):
    """Return contiguous blocks of text from <tag> to </tag> in `text`."""
    return re.findall('(?s)<{0}>.*?</{0}>'.format(tag), sgml)

def texts(sgml):
    """Return tags and the text inside of them in `sgml`."""
    for tag, text in tag_with_text.findall(sgml):
        yield tag, unescape(text)

def tokenize(sgml):
    """Parse SGML into a list of (end, tag, text) tuples."""
    return sgmlre.findall(sgml)

def accounts(ofx):
    """Return the list of accounts in the `ofx` text."""
    accounts = []
    for sgml in (tags(ofx, 'BANKACCTFROM') +
                 tags(ofx, 'CCACCTFROM') +
                 tags(ofx, 'INVACCTFROM')):
        attrs = dict(texts(sgml))
        attrs['FROM'] = sgml  # save raw SGML too, for use in requests
        accounts.append(types.Account(attrs))
    return accounts

def activity(ofx):
    """Return activity."""
    balances = {}
    transactions = {}
    values = {}
    tranlist = []
    for end, tag, text in tokenize(ofx):
        if end:
            if tag == 'BANKACCTFROM':
                key = (
                    values.pop('BANKID'),
                    values.pop('ACCTID'),
                    values.pop('ACCTTYPE'),
                    )
            elif tag == 'STMTTRN':
                transaction = types.Transaction(
                    values.pop('TRNTYPE'),
                    values.pop('DTPOSTED'),
                    Decimal(values.pop('TRNAMT')),
                    values.pop('FITID'),
                    values.pop('CHECKNUM', None),
                    values.pop('NAME', None),
                    )
                tranlist.append(transaction)
            elif tag == 'STMTRS':
                balances[key] = Decimal(values.pop('BALAMT'))
                transactions[key] = tranlist
                for transaction in tranlist:
                    transaction.key = key
                key = None
                tranlist = []
        elif text:
            values[tag] = unescape(text)
    return balances, transactions
