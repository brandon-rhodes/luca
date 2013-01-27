"""Yodlee CSV exports.

Open question:

* Does Yodlee ever include check numbers?

"""
import csv
import os
from ConfigParser import RawConfigParser
from cStringIO import StringIO

indent = '   '
standard_heading = (
    'Status,Date,Original Description,Split Type,Category,Currency,'
    'Amount,User Description,Memo,Classification,Account Name'
    )

def matches(content):
    return content.startswith(standard_heading)

def parse(content):
    if os.path.exists('luca.ini'):
        parser = RawConfigParser()
        parser.read(['luca.ini'])
        if parser.has_option('import', 'replace'):
            for line in parser.get('import', 'replace').splitlines():
                line = line.strip()
                if not line:
                    continue
                pattern, replacement = line.split('|')
                content = content.replace(pattern, replacement)

    rows = list(csv.DictReader(StringIO(content)))
    split_dates(rows)
    rows.sort(key=lambda row: row['Date'])
    for row in rows:

        if row['Currency'] != '$':
            raise ValueError('not sure about a non-$ Currency')

        if row['Memo']:
            raise ValueError('not sure about a non-empty Memo')

        if row['Split Type']:
            raise ValueError('not sure about a non-empty Split Type')

        if row['User Description']:
            raise ValueError('not sure about a non-empty User Description')

        if row['Classification'] != 'Personal':
            raise ValueError('not sure about a non-Personal Classification')

        year, month, day = row['Date']
        fields = row['Original Description'].split('%%')
        description = fields[0].strip()
        comments = fields[1:]
        account_name = ' '.join(row['Account Name'].split())

        for comment in comments:
            print ';', comment.strip()
        print '{}/{}/{}'.format(year, month, day),
        if row['Status'] == 'posted':
            print '*',
        else:
            raise ValueError('unrecognized Status %r' % row['Status'])
        print '{}'.format(description)
        print indent, '{:40}  {:>14}'.format(
            row['Category'], '$' + row['Amount'])
        print indent, account_name
        print


def split_dates(rows):
    for row in rows:
        row['Date'] = [ int(field) for field in row['Date'].split('-') ]
