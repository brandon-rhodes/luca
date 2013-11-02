# -*- coding: utf-8 -*-
"""Trial of rule-driven accounting."""

import re
import sys

import yaml
from StringIO import StringIO
from bottle import route, run, template

from luca.importer.dccu import import_dccu_visa_pdf
from luca.pdf import extract_text_from_pdf_file

sample_yaml = u"""\
- 2013-09:
  - / MA$/: Expenses.Travel.boxborough9
  - / NH$/: Expenses.Travel.boxborough9
"""

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

@route('/')
def index(name='World'):
    text = extract_text_from_pdf_file(sys.argv[1])
    transactions = import_dccu_visa_pdf(text, T)
    y = yaml.safe_load(StringIO(sample_yaml))
    print y
    process_transactions(transactions, y)

    foo = ''
    for t in transactions:
        foo += '%s %s %s %s : %s\n' % (
            t.date, t.amount, repr(t.description), t.comments, t.category)

    return template('<pre>{{foo}}</pre>', foo=foo)

def main():
    run(host='localhost', port=8080, reloader=True, interval=0.2)

if __name__ == '__main__':
    main()
