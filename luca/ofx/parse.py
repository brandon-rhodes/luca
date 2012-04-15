import re
from decimal import Decimal
from . import types

sgmlre = re.compile(r'<(/?)([^>]+)>([^<]*)')

def tokenize(sgml):
    """Parse SGML into a list of (end, tag, text) tuples."""
    return sgmlre.findall(sgml)

def unescape(text):
    """Replace SGML character escapes in `text` with literal character."""
    return text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

def accounts(ofx):
    """Return the list of accounts in the `ofx` text."""
    accounts = []
    values = {}
    for end, tag, text in tokenize(ofx):
        if end:
            if tag == 'BANKACCTFROM':
                account = types.Account(
                    values.pop('BANKID'),
                    values.pop('ACCTID'),
                    values.pop('ACCTTYPE'),
                    )
                accounts.append(account)
        elif text:
            values[tag] = unescape(text)
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
