# -*- coding: utf-8 -*-
"""Tally expenses by category, driven by bank statements and YAML rules."""

from collections import defaultdict
from decimal import Decimal
from itertools import groupby
from operator import attrgetter
from textwrap import wrap

import yaml
from blessings import Terminal

from luca.importer.dccu import importers
from luca.pdf import extract_text_from_pdf_file
from luca import rules

def sum_categories(transactions):
    sums = defaultdict(Decimal)
    for tr in transactions:
        for a in category_and_ancestors('Accounts.' + tr.account):
            sums[a] += tr.amount
        for c in category_and_ancestors(tr.category):
            sums[c] -= tr.amount
    return sums

def category_and_ancestors(category):
    """Generate a list of strings: a category and all its ancestors.

    >>> for c in category_and_ancestors('Expenses.Travel.PyCon'):
    ...     c
    ...
    'Expenses.Travel.PyCon'
    'Expenses.Travel'
    'Expenses'

    """
    i = category.rfind('.')
    while i != -1:
        yield category
        category = category[:i]
        i = category.rfind('.')
    yield category

def group_transactions_by_category(transactions):
    """Return a new list [(category, [transaction, ...], ...]."""
    tlist = sorted(transactions, key=lambda tr: (tr.category, tr.date))
    return {category: list(iterator) for category, iterator
            in groupby(tlist, lambda tr: tr.category)}

def run_yaml_file(terminal, path, statement_paths, show_balances, be_verbose):

    t = terminal
    screen_width = t.width or 80

    with open(path) as f:
        rule_tree = yaml.safe_load(f)

    rule_tree_function = rules.compile_tree(rule_tree)

    balances = []
    transactions = []

    for path in statement_paths:
        if path.lower().endswith('.pdf'):
            text = extract_text_from_pdf_file(path)
        elif path.lower().endswith('.txt'):
            with open(path) as f:
                text = f.read().decode('utf-8')
        else:
            raise ValueError('no idea what to do with file {!r}'.format(path))

        matching_importers = [importer for importer in importers
                              if importer.does_this_match(text)]

        if len(matching_importers) == 0:
            raise RuntimeError('cannot find an importer for file: {}'
                               .format(path))
        elif len(matching_importers) > 1:
            raise RuntimeError('found too many importers for file: {}'
                               .format(path))

        importer = matching_importers[0]
        new_balances, new_transactions = importer(text)
        balances.extend(new_balances)
        transactions.extend(new_transactions)

    verify_balances(balances, transactions, show_balances, t)

    for tr in transactions:
        tr.category = rule_tree_function(tr)

    transactions = [tr for tr in transactions if tr.category is not None]
    catdict = group_transactions_by_category(transactions)
    sumdict = sum_categories(transactions)
    categories = set(catdict) | set(sumdict)

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


    for category in sorted(categories):
        csum = sumdict[category]
        depth = category.count('.')
        if not be_verbose and depth:
            name = category[category.rfind('.')+1:]
        else:
            name = category
        add('{}{} {}'.format(category_indent * depth, f(csum), name))
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

def verify_balances(balances, transactions, show_balances, t):
    """Raise an exception if the transactions do not match the balances."""

    # We are careful to balances before transactions in the original
    # list so that the stable sort leaves all balances for a particular
    # date in front of any transactions for that same date.

    events = list(balances)
    events.extend(transactions)
    events.sort(key=attrgetter('date'))
    if show_balances:
        events.sort(key=attrgetter('account'))

    amounts = {}

    for e in events:

        if e.event_type == 'balance':
            if e.account not in amounts:
                if show_balances:
                    print
                    print e.account
                    print
                amounts[e.account] = e.amount
                continue

            equal = (amounts[e.account] == e.amount)

            if not equal:
                print e.date, amounts[e.account], '!=', e.amount
            elif show_balances:
                print e.date, '==', e.amount

            #assert equal

        elif e.event_type == 'transaction':
            if e.account not in amounts:
                continue

            amounts[e.account] += e.amount

            if show_balances:
                print e.date, amounts[e.account]

    if show_balances:
        print
