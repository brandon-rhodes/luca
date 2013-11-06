# -*- coding: utf-8 -*-
"""Trial of rule-driven accounting."""

import sys
from collections import defaultdict
from decimal import Decimal
from itertools import groupby

import yaml
from bottle import route, run, template

from luca.importer.dccu import importers
from luca.pdf import extract_text_from_pdf_file
from luca.rules import apply_rule_tree

class T(object):
    def __init__(self):
        self.category = '(uncategorized)'
        self.earlier_categories = []

def sum_categories(transactions):
    sums = defaultdict(Decimal)
    for t in transactions:
        c = t.category
        sums[c] += t.amount
        pieces = c.rsplit('.', 1)
        while len(pieces) == 2:
            c = pieces[0]
            sums[c] += t.amount
            pieces = c.rsplit('.', 1)
    return sums

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
        transaction_lists = [importer(text, T) for importer in importers]
        keepers = [tlist for tlist in transaction_lists if tlist is not None]
        if len(keepers) == 0:
            raise RuntimeError('cannot find an importer for file: {}'
                               .format(path))
        elif len(keepers) > 1:
            raise RuntimeError('found too many importers for file: {}'
                               .format(path))
        transactions.extend(keepers[0])

    apply_rule_tree(transactions, None, rule_tree)
    sums = sum_categories(transactions)
    category_list = group_transactions_by_category(transactions)

    lines = ['<pre>']
    for category, transaction_list in category_list:
        lines.append('{:10,}  {}'.format(sums[category], category))
        for t in transaction_list:
            lines.append('{}{} {:10,} {} {}'.format(
                u' ' * 12, t.date, t.amount, t.description, t.comments))

    return u'\n'.join(lines)

def main():
    run(host='localhost', port=8080, reloader=True, interval=0.2)

if __name__ == '__main__':
    main()
