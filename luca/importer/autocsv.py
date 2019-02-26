from __future__ import print_function

import csv
import re
import sys
from datetime import datetime
from decimal import Decimal
from .model import Transaction

date_match = re.compile(r'(0?[1-9]|1[012])'
                        r'/(0?[1-9]|[12]\d|3[01])'
                        r'/(19\d\d|20\d\d)$').match

amount_match = re.compile(r'\(?([+-]?)\$?(\d[\d,]*\.\d\d)\)?$').match

def importer(csvfile):
    """Parse a generic CSV containing transaction data."""

    sample = csvfile.read()

    if csv.Sniffer().has_header(sample):
        balances = []
        transactions = _parse_headered_file(sample.splitlines())
        return balances, transactions

    csvfile.seek(0)
    dialect = csv.Sniffer().sniff(sample)
    reader = csv.reader(csvfile, dialect)

    balances = []
    transactions = []

    for row in reader:
        try:
            _parse(row, balances, transactions)
        except ValueError as e:
            print('{0}: ignoring CSV line because luca {1}:\n{2}\n'.format(
                csvfile.name, e, row, file=sys.stderr))

    return balances, transactions

def _parse_headered_file(csvfile):
    reader = csv.DictReader(csvfile)
    names = reader.fieldnames

    account_field = _first(names, ['Card', 'Account'])
    date_field = _first(names, ['Transaction Date', 'Date'])
    description_field = _first(names, ['Description'])
    credit_field = _first(names, ['Amount', 'Credit'])
    debit_field = _first(names, ['Debit'], error=False)

    for row in reader:
        t = Transaction()

        t.account = row[account_field]
        t.date = datetime.strptime(row[date_field], '%m/%d/%Y').date()
        t.description = row[description_field]
        if row[credit_field]:
            t.amount = Decimal(row[credit_field])
        elif debit_field:
            t.amount = - Decimal(row[debit_field])
        else:
            t.amount = Decimal(0)
        yield t

def _first(fieldnames, candidates, error=True):
    for name in candidates:
        if name in fieldnames:
            return name
    if not error:
        return None
    raise ValueError('cannot find any of the names {} in the field names {}'
                     .format(candidates, fieldnames))

def _parse(row, balances, transactions):
    # TODO: better way to detect header line
    # if row[0] == 'Type':
    #     return

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
            if amount is not None:
                # TODO: check whether the second amount is a correct
                # running balance.
                continue
            amount = Decimal(a.group(1) + a.group(2).replace(',', ''))
            if field.startswith('('):
                amount = -amount
            continue
        field = field.strip()
        if field:
            description.append(field)

    if date is None:
        raise ValueError('cannot find date field')
    if amount is None:
        raise ValueError('cannot find amount field')

    t = Transaction()
    t.account = 'Checking'
    t.date = date
    t.description = ' '.join(description)
    t.amount = amount

    transactions.append(t)
