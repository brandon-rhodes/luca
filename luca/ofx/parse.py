import re
from . import types

sgmlre = re.compile(r'<(/?)([^>]+)>([^<]*)')

def tokenize(sgml):
    """Parse SGML into a list of (end, tag, text) tuples."""
    return sgmlre.findall(sgml)

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
            values[tag] = text
    return accounts

def activity(ofx):
    """Return activity."""
    balances = {}
    values = {}
    for end, tag, text in tokenize(ofx):
        if end:
            if tag == 'BANKACCTFROM':
                key = (
                    values.pop('BANKID'),
                    values.pop('ACCTID'),
                    values.pop('ACCTTYPE'),
                    )
            elif tag == 'STMTRS':
                balances[key] = values.pop('BALAMT')
                key = None
        elif text:
            values[tag] = text
    return balances
