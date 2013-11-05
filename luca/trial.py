# -*- coding: utf-8 -*-
"""Trial of rule-driven accounting."""

import sys
from itertools import groupby

import yaml
from bottle import route, run, template

from luca.importer.dccu import import_dccu_visa_pdf
from luca.pdf import extract_text_from_pdf_file
from luca.rules import apply_rule_tree

class T(object):
    pass

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
        rule_tree = yaml.safe_load(f)

    transactions = []
    for path in sys.argv[2:]:
        text = extract_text_from_pdf_file(path)
        more_transactions = import_dccu_visa_pdf(text, T)
        transactions.extend(more_transactions)

    apply_rule_tree(transactions, None, rule_tree)
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
