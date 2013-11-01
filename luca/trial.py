# -*- coding: utf-8 -*-
"""Trial of rule-driven accounting."""

import re
import subprocess
from datetime import date
from decimal import Decimal

import yaml
from StringIO import StringIO
from bottle import route, run, template

sample_yaml = u"""\
- 2013-09:
  - / MA$/: Expenses.Travel.boxborough9
  - / NH$/: Expenses.Travel.boxborough9
"""
print yaml.safe_load(StringIO(sample_yaml))
# import sys
# sys.exit(0)

transaction_start = re.compile(ur"""
    \s*(\d*)          # "Reference Number"
    \s+(\d\d)/(\d\d)  # "Trans Date"
    \s+(\d\d)/(\d\d)  # "Post Date"
    \s+([^$]*)        # "Description"
    \$(\d+\.\d\d)$    # "Amount"
    """, re.VERBOSE)

class T(object):
    pass

def process_transactions(transactions, rule):
    if isinstance(rule, str) or isinstance(rule, unicode):
        category = unicode(rule)
        for t in transactions:
            t.category = category
    elif isinstance(rule, list):
        for item in rule:
            process_transactions(transactions, item)
    elif isinstance(rule, dict):
        for key, value in rule.items():
            if key.startswith('/') and key.endswith('/'):
                r = re.compile(key[1:-1])
                process_transactions(
                    [t for t in transactions
                     if r.search(t.description)
                     or any(r.search(c) for c in t.comments)],
                    value,
                    )
            else: # 'YYYY-MM'
                year = int(key[:4])
                month = int(key[5:7])
                process_transactions(
                    [t for t in transactions
                     if t.date.year == year and t.date.month == month],
                    value,
                    )

@route('/')
def index(name='World'):
    command = ['pdftotext', '-layout', 'rms-visa-2013-10.pdf', '-']
    content = subprocess.check_output(command).decode('utf-8')

    transactions = []
    lines = iter(content.splitlines())
    i = 0

    for line in lines:
        match = transaction_start.match(line)
        if match:
            t = T()
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

    y = yaml.safe_load(StringIO(sample_yaml))
    print y
    process_transactions(transactions, y)

    foo = ''
    for t in transactions:
        foo += '%s %s %s %s : %s\n' % (
            t.date, t.amount, repr(t.description), t.comments, t.category)

    return template('<pre>{{foo}}</pre><hr><pre>{{name}}</pre>!',
                    foo=foo, name=content)

def main():
    run(host='localhost', port=8080, reloader=True, interval=0.2)

if __name__ == '__main__':
    main()
