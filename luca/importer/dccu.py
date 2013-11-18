"""Delta Community Credit Union PDF statements."""

import re
from datetime import date, timedelta
from decimal import Decimal
from .model import Balance, Transaction, can_import_texts_containing

one_day = timedelta(days=1)

_checking_beginning_re = re.compile(ur"""
    \s+
    (\d\d)/(\d\d)\s+       # "Posting Date"
    (ID\ \d\d\d\d\ .*)     # (Account name)
    Balance\ Forward\s+
    (\d+\.\d\d)$           # "NEW BALANCE"
    """, re.VERBOSE)

_checking_ending_re = re.compile(ur"""
    \s+
    (\d\d)/(\d\d)\s+       # "Posting Date"
    Ending\ Balance\s+
    (\d+\.\d\d)$           # "NEW BALANCE"
    """, re.VERBOSE)

_checking_transaction_re = re.compile(ur"""
    \s+
    (\d\d)/(\d\d)\s+       # "Posting Date"
    (?:(\d\d)/(\d\d)\s+)?  # "Effective Date"
    ([^$]*)\s+             # "Transaction Description"
    (\d+\.\d\d)(-?)\s+     # "Transaction Amount"
    (\d+\.\d\d)$           # "NEW BALANCE"
    """, re.VERBOSE)

@can_import_texts_containing(
    u'www.DeltaCommunityCU.com',
    u'P.O. Box 20541 Atlanta, GA 30320-2541',
    )
def import_dccu_checking_pdf(text):
    """Parse a Delta Community Credit Union checking account statement."""

    account = None
    id_minimum_len = len('01/08 96873230009628183520165')
    id_start_index = len('01/08 ')
    balances = []
    transactions = []
    lines = iter(text.splitlines())
    indent = 0

    for line in lines:
        match = _checking_beginning_re.match(line)
        if match:
            group = match.group
            account = group(3).strip()
            b = Balance()
            b.account = account
            b.date = date(year=2013, month=int(group(1)), day=int(group(2)))
            b.amount = Decimal(group(4))
            balances.append(b)
            indent = 0
            continue
        match = _checking_ending_re.match(line)
        if match:
            group = match.group
            b = Balance()
            b.account = account
            end_date = date(year=2013, month=int(group(1)), day=int(group(2)))
            b.date = end_date + one_day
            b.amount = Decimal(group(3))
            balances.append(b)
            indent = 0
            continue
        match = _checking_transaction_re.match(line)
        if match:
            group = match.group
            t = Transaction()
            t.account = account
            t.date = date(year=2013, month=int(group(1)), day=int(group(2)))
            t.description = [group(5).strip()]
            t.amount = Decimal(group(6))
            if group(7) == u'-':
                t.amount = -t.amount
            transactions.append(t)
            indent = match.start(5)
        elif (indent and line[:indent].isspace()
              and not line[indent:indent+1].isspace()):
            more = line.strip()
            if more.startswith('Annual Percentage Yield Earned'):
                continue
            if more.startswith('Based on Average Daily Balance'):
                continue
            if len(more) > id_minimum_len:
                id = more[id_start_index : id_minimum_len]
                if id.isdigit():
                    more = more[:id_start_index - 1] + more[id_minimum_len:]
            t.description.append(more)
        elif indent:
            indent = 0

    for t in transactions:
        if t.description[0] == u'Card Fee' and len(t.description) > 1:
            del t.description[0]
        t.description = ' - '.join(t.description)

    return balances, transactions


_visa_balances_re = re.compile(ur"""
    \s*
    Previous\ Balance
    \s+
    \$(?P<previous_balance>[\d,]+\.\d\d)
    \s+
    New\ Balance
    \s+
    \$(?P<new_balance>[\d,]+\.\d\d)$
    """, re.VERBOSE)

_visa_transaction_re = re.compile(ur"""
    \s*
    (\d+\s+)?                  # "Reference Number"
    (\d\d)/(\d\d)\s+           # "Trans Date"
    (\d\d)/(\d\d)\s+           # "Post Date"
    (.*)                       # "Description"
    \(?\$([\d,]+\.\d\d)(\)?)$  # "Amount"
    """, re.VERBOSE)

@can_import_texts_containing(
    u'www.DeltaCommunityCU.com',
    u'Business Credit Card Statement',
    )
def import_dccu_visa_pdf(text):
    """Parse a Delta Community Credit Union Visa statement."""

    account = 'DCCU Business Visa'
    balances = []
    transactions = []
    lines = iter(text.splitlines())
    i = 0

    for line in lines:
        line = line.rstrip()
        stripped_line = line.lstrip()

        match = _visa_balances_re.match(line)
        if match:
            b = Balance()
            b.account = account
            b.amount = - Decimal(match.group('new_balance').replace(',', ''))
            continue

        if stripped_line.startswith('Statement Closing Date'):
            closing = stripped_line.split()[3].split('/')  # '01/10/2013'
            closing_year = int(closing[2])
            closing_month = int(closing[0])
            closing_day = int(closing[1])
            closing_date = date(closing_year, closing_month, closing_day)
            b.date = closing_date + one_day
            balances.append(b)
            continue

        match = _visa_transaction_re.match(line)
        if match:
            group = match.group
            t = Transaction()
            t.account = account
            month = int(group(4))
            day = int(group(5))
            year = closing_year - 1 if month > closing_month else closing_year
            t.date = date(year, month, day)
            description = group(6).strip()
            if description.endswith(' **'):
                description = description[:-3].strip()
            t.description = [description]
            t.amount = Decimal(group(7).replace(',', ''))
            if not group(8):
                t.amount = - t.amount
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

    return balances, transactions


importers = [import_dccu_checking_pdf, import_dccu_visa_pdf]
