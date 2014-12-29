import csv
import re
from datetime import datetime
from decimal import Decimal
from .model import Transaction

date_match = re.compile(r'(0?[1-9]|1[012])'
                        r'/(0?[1-9]|[12]\d|3[01])'
                        r'/(19\d\d|20\d\d)$').match

amount_match = re.compile(r'([+-]?)\$?(\d[\d,]*\.\d\d)$').match

def importer(csvfile):
    """Parse a generic CSV containing transaction data."""

    dialect = csv.Sniffer().sniff(csvfile.read())
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

    balances = []
    transactions = []

    for row in reader:
        # TODO: better way to detect header line
        if row[0] == 'Type':
            continue

        # print row
        date = amount = None
        description = []

        for field in row:
            m = date_match(field)
            if m:
                date = datetime.strptime(field, '%m/%d/%Y').date()
                continue
            a = amount_match(field)
            if a:
                amount = Decimal(a.group(1) + a.group(2).replace(',', ''))
                continue
            field = field.strip()
            if field:
                description.append(field)

        if date is None:
            raise ValueError('cannot find date: {}'.format(row))
        if amount is None:
            raise ValueError('cannot find amount: {}'.format(row))

        t = Transaction()
        t.account = 'Checking'
        t.date = date
        t.description = ' '.join(description)
        t.amount = amount

        transactions.append(t)

    return balances, transactions
