"""Delta Community Credit Union PDF statements."""

import re
from datetime import date
from decimal import Decimal

_checking_transaction_re = re.compile(ur"""
    \s+
    (\d\d)/(\d\d)\s+       # "Posting Date"
    (?:(\d\d)/(\d\d)\s+)?  # "Effective Date"
    ([^$]*)\s+             # "Transaction Description"
    (\d+\.\d\d)(-?)\s+     # "Transaction Amount"
    (\d+\.\d\d)$           # "NEW BALANCE"
    """, re.VERBOSE)

def import_dccu_checking_pdf(text, Transaction):
    """Parse a Delta Community Credit Union checking account statement."""

    if u'www.DeltaCommunityCU.com' not in text:
        return None
    if u'ACCOUNTS ARE NON-TRANSFERABLE EXCEPT ON THE BOOKS' not in text:
        return None

    id_minimum_len = len('01/08 24325453009900018833450')
    id_start_index = len('01/08 ')
    transactions = []
    lines = iter(text.splitlines())
    i = 0

    for line in lines:
        match = _checking_transaction_re.match(line)
        if match:
            t = Transaction()
            month = int(match.group(1))
            day = int(match.group(2))
            t.date = date(2013, month, day)
            t.description = [match.group(5).strip()]
            t.amount = Decimal(match.group(6))
            if match.group(7) != u'-':
                t.amount = -t.amount
            transactions.append(t)
            i = match.start(5)
        elif i and line[:i].isspace() and not line[i:i+1].isspace():
            more = line.strip()
            if more.startswith('Based on Average Daily Balance'):
                continue
            if len(more) > id_minimum_len:
                id = more[id_start_index : id_minimum_len]
                if id.isdigit():
                    more = more[:id_start_index - 1] + more[id_minimum_len:]
            t.description.append(more)
        elif i:
            i = 0

    for t in transactions:
        if t.description[0] == u'Card Fee' and len(t.description) > 1:
            del t.description[0]
        t.description = ' - '.join(t.description)

    return transactions


_visa_transaction_re = re.compile(ur"""
    \s*(\d*)          # "Reference Number"
    \s+(\d\d)/(\d\d)  # "Trans Date"
    \s+(\d\d)/(\d\d)  # "Post Date"
    \s+([^$]*)        # "Description"
    \$(\d+\.\d\d)$    # "Amount"
    """, re.VERBOSE)

def import_dccu_visa_pdf(text, Transaction):
    """Parse a Delta Community Credit Union Visa statement."""

    if u'www.DeltaCommunityCU.com' not in text:
        return None
    if u'Business Credit Card Statement' not in text:
        return None

    transactions = []
    lines = iter(text.splitlines())
    i = 0

    for line in lines:
        match = _visa_transaction_re.match(line)
        if match:
            t = Transaction()
            month = int(match.group(2))
            day = int(match.group(3))
            t.date = date(2013, month, day)
            description = match.group(6).strip()
            if description.endswith(' **'):
                description = description[:-3].strip()
            t.description = [description]
            t.amount = Decimal(match.group(7))
            t.comments = []
            transactions.append(t)
            i = match.start(6)
        elif i and line[:i].isspace() and not line[i:i+1].isspace():
            t.description.append(line.strip())
        elif i:
            i = 0

    for t in transactions:
        if t.description[0] == u'Card Fee' and len(t.description) > 1:
            del t.description[0]
        last = t.description[-1]
        if last.startswith('Card ') and last[5:].isdigit():
            del t.description[-1]
        t.description = ' - '.join(t.description)

    return transactions


importers = [import_dccu_checking_pdf, import_dccu_visa_pdf]
