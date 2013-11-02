# -*- coding: utf-8 -*-
"""Trial of rule-driven accounting."""

import re
import sys
from itertools import groupby

import yaml
from StringIO import StringIO
from bottle import route, run, template

from luca.importer.dccu import import_dccu_visa_pdf
from luca.pdf import extract_text_from_pdf_file

class T(object):
    pass

def process_transactions(transactions, rule):
    if isinstance(rule, str) or isinstance(rule, unicode):
        category = unicode(rule)
        for t in transactions:
            if t.category is not None:
                raise ValueError('transaction already has a category')
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

def group_transactions_by_category(transactions):
    """Return a new list [(category, [transaction, ...], ...]."""
    tlist = sorted(transactions, key=lambda t: (t.category or '\177', t.date))
    category_list = []
    for category, group in groupby(tlist, lambda t: t.category):
        tup = (category, list(group))
        category_list.append(tup)
    return category_list

@route('/')
def index(name='World'):

    with open(sys.argv[1]) as f:
        y = yaml.safe_load(f)
    print y

    transactions = []
    for path in sys.argv[2:]:
        text = extract_text_from_pdf_file(path)
        more_transactions = import_dccu_visa_pdf(text, T)
        transactions.extend(more_transactions)

    process_transactions(transactions, y)
    category_list = group_transactions_by_category(transactions)

    lines = ['<pre>']
    for category, transaction_list in category_list:
        lines.append(str(category))
        for t in transaction_list:
            lines.append('%s%s %s %s %s' % (
                ' ' * 12, t.date, t.amount, repr(t.description), t.comments))

    return '\n'.join(lines)

def main():
    run(host='localhost', port=8080, reloader=True, interval=0.2)

if __name__ == '__main__':
    main()
