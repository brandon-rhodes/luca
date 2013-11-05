"""Delta Community Credit Union PDF statements."""

import re
from datetime import date
from decimal import Decimal

transaction_start_re = re.compile(ur"""
    \s*(\d*)          # "Reference Number"
    \s+(\d\d)/(\d\d)  # "Trans Date"
    \s+(\d\d)/(\d\d)  # "Post Date"
    \s+([^$]*)        # "Description"
    \$(\d+\.\d\d)$    # "Amount"
    """, re.VERBOSE)

def import_dccu_visa_pdf(text, Transaction):
    """Parse a Delta Community Credit Union Visa statement."""

    transactions = []
    lines = iter(text.splitlines())
    i = 0

    for line in lines:
        match = transaction_start_re.match(line)
        if match:
            t = Transaction()
            month = int(match.group(2))
            day = int(match.group(3))
            t.date = date(2013, month, day)
            description = match.group(6).strip()
            if description.endswith(' **'):
                description = description[:-3].strip()
            t.description = description
            t.amount = Decimal(match.group(7))
            t.comments = []
            t.category = None
            transactions.append(t)
            i = match.start(6)
        elif i and line[:i].isspace() and not line[i:i+1].isspace():
            t.comments.append(line.strip())
        elif i:
            i = 0

    for t in transactions:
        if t.description == u'Card Fee' and t.comments:
            t.description = t.comments.pop(0)

    return transactions
