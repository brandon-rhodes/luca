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
from luca import rules


def sum_categories(transactions):
    assets = Decimal('0')
    sums = defaultdict(Decimal)
    for t in transactions:
        assets += t.amount
        c = t.category
        sums[c] += t.amount
        pieces = c.rsplit('.', 1)
        while len(pieces) == 2:
            c = pieces[0]
            sums[c] += t.amount
            pieces = c.rsplit('.', 1)
    return assets, sums

def group_transactions_by_category(transactions):
    """Return a new list [(category, [transaction, ...], ...]."""
    tlist = sorted(transactions, key=lambda t: (t.category, t.date))
    return {category: list(iterator) for category, iterator
            in groupby(tlist, lambda t: t.category)}

@route('/')
def index(name='World'):
    pass

def run_yaml_file(path, statement_paths):

    with open(path) as f:
        rule_tree = yaml.safe_load(f)

    #from pprint import pprint
    #pprint(rule_tree)

    transactions = []
    for path in statement_paths:
        if path.lower().endswith('.pdf'):
            text = extract_text_from_pdf_file(path)
        elif path.lower().endswith('.txt'):
            with open(path) as f:
                text = f.read().decode('utf-8')
        else:
            raise ValueError('no idea what to do with file {!r}'.format(path))

        transaction_lists = [importer(text) for importer in importers]
        keepers = [tlist for tlist in transaction_lists if tlist is not None]
        if len(keepers) == 0:
            raise RuntimeError('cannot find an importer for file: {}'
                               .format(path))
        elif len(keepers) > 1:
            raise RuntimeError('found too many importers for file: {}'
                               .format(path))
        transactions.extend(keepers[0])

    rule_tree_function = rules.compile_tree(rule_tree)
    for tt in transactions:
        tt.category = rule_tree_function(tt)

    transactions = [t for t in transactions if t.category is not None]
    catdict = group_transactions_by_category(transactions)
    assets, sumdict = sum_categories(transactions)
    categories = set(catdict) | set(sumdict)

    lines = ['<style>'
             'body {background-color: #ffffff; color: #073642}'
             'pre {font-family: Inconsolata}'
             'strong {color: #002b36}'
             'pos {color: #859900; font-weight: bold}'
             'neg {color: #dc322f; font-weight: bold}'
             '</style><pre>']

    tag = 'pos' if assets >= 0 else 'neg'
    lines.append('<{}>{:>12}</{}>  <strong>Assets</strong>'.format(
        tag, qformat(assets), tag))

    for category in sorted(categories):
        csum = sumdict[category]
        tag = 'pos' if csum >= 0 else 'neg'
        lines.append('<{}>{:>12}</{}>  <strong>{}</strong>'.format(
            tag, qformat(csum), tag, category))
        transaction_list = catdict.get(category, None)
        if not transaction_list:
            continue
        for t in transaction_list:
            tag = 'pos' if t.amount >= 0 else 'neg'
            lines.append('{}{} <{}>{:>12}</{}> {}'.format(
                u' ' * 14, t.date, tag, qformat(t.amount), tag, t.description))

    return u'\n'.join(lines)

def qformat(quantity):
    """Stringify `quantity`, putting parentheses around a negative value."""
    if quantity < 0:
        return '{:,}-'.format(-quantity)
    else:
        return '{:,} '.format(quantity)

def main():
    run(host='localhost', port=8080, reloader=True, interval=0.2)

if __name__ == '__main__':
    main()
