# -*- coding: utf-8 -*-
"""Trial of rule-driven accounting."""

from collections import defaultdict
from decimal import Decimal
from itertools import groupby
from textwrap import wrap

import yaml
from blessings import Terminal

from luca.importer.dccu import importers
from luca.pdf import extract_text_from_pdf_file
from luca import rules


def sum_categories(transactions):
    assets = Decimal('0')
    sums = defaultdict(Decimal)
    for tr in transactions:
        assets += tr.amount
        c = tr.category
        sums[c] += tr.amount
        pieces = c.rsplit('.', 1)
        while len(pieces) == 2:
            c = pieces[0]
            sums[c] += tr.amount
            pieces = c.rsplit('.', 1)
    return assets, sums

def group_transactions_by_category(transactions):
    """Return a new list [(category, [transaction, ...], ...]."""
    tlist = sorted(transactions, key=lambda tr: (tr.category, tr.date))
    return {category: list(iterator) for category, iterator
            in groupby(tlist, lambda tr: tr.category)}

def run_yaml_file(path, statement_paths, be_verbose):

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
    for tr in transactions:
        tr.category = rule_tree_function(tr)

    transactions = [tr for tr in transactions if tr.category is not None]
    catdict = group_transactions_by_category(transactions)
    assets, sumdict = sum_categories(transactions)
    categories = set(catdict) | set(sumdict)

    t = Terminal()
    screen_width = t.width or 80

    output_lines = []
    add = output_lines.append

    biggest_amount = max(abs(v) for v in sumdict.values())

    amount_width = len('{:,}'.format(biggest_amount)) + 1
    date_width = 10
    gutter = 2
    category_indent = ' ' * (amount_width + 1)
    description_width = (
        screen_width -  # content from left to right:
        gutter - date_width - gutter - # (description goes here)
        gutter - amount_width - gutter)
    description_indent = ' ' * (gutter + date_width + gutter)

    def f(amount):
        """Format `amount`, putting parentheses around a negative value."""
        if amount < 0:
            return t.red('{:{},}-'.format(-amount, amount_width - 1))
        else:
            return t.green('{:{},} '.format(amount, amount_width - 1))


    add('{} Assets'.format(f(assets)))

    for category in sorted(categories):
        csum = sumdict[category]
        depth = category.count('.')
        add('{}{} {}'.format(category_indent * depth, f(csum), category))
        if not be_verbose:
            continue
        transaction_list = catdict.get(category, None)
        if not transaction_list:
            continue
        add('')
        for tr in transaction_list:
            lines = wrap(tr.description, description_width)
            add('  {}  {:<{}}  {}'.format(
                tr.date, lines[0], description_width, f(tr.amount)))
            for line in lines[1:]:
                add(description_indent + line)
        add('')

    return u'\n'.join(output_lines)
