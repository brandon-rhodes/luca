"""Apply YAML rules to transactions."""

import re
from datetime import date

def apply_rule_tree(transactions, category, rule_tree):
    """Um."""

    if isinstance(rule_tree, int) or isinstance(rule_tree, str):
        rule = rule_tree
        transactions2, category2 = apply_rule(transactions, category, rule)
        for t in transactions2:
            if t.category is not None:
                t.category = '!CONFLICT: {} or {}'.format(t.category, category)
            else:
                t.category = category2

    elif isinstance(rule_tree, list):
        for subtree in rule_tree:
            apply_rule_tree(transactions, category, subtree)

    elif isinstance(rule_tree, dict):
        for rule, subtree in rule_tree.items():
            transactions2, category2 = apply_rule(transactions, category, rule)
            apply_rule_tree(transactions2, category2, subtree)

_month_day_re = re.compile('\d\d/\d\d$')
_month_day_to_month_day_re = re.compile('\d\d/\d\d-\d\d/\d\d$')

def apply_rule(transactions, category, rule):
    """Return (transactions, category)."""

    f = None

    if isinstance(rule, str):
        if rule.startswith('/') and rule.endswith('/'):
            r = re.compile(rule[1:-1])
            f = lambda t: r.search(t.description)
        elif rule.startswith('~/') and rule.endswith('/'):
            r = re.compile(rule[2:-1])
            f = lambda t: not r.search(t.description)
        else:
            match = _month_day_re.match(rule)
            if match:
                month = int(rule[:2])
                day = int(rule[3:])
                f = lambda t: t.date.month == month and t.date.day == day
            else:
                match = _month_day_to_month_day_re.match(rule)
                if match:
                    month1 = int(rule[:2])
                    day1 = int(rule[3:5])
                    month2 = int(rule[6:8])
                    day2 = int(rule[9:11])
                    f = lambda t: (
                        date(t.date.year, month1, day1) <= t.date and
                        t.date <= date(t.date.year, month2, day2)
                        )

    if isinstance(rule, str):
        s = rule
        n = int(rule) if rule.isdigit() else None
    elif isinstance(rule, int):
        s = str(rule)
        n = rule

    if (n is not None) and 1900 <= n <= 2100:
        f = lambda t: t.date.year == n
    elif (n is not None) and 1 <= n <= 12:
        f = lambda t: t.date.month == n

    if f is None:
        category = rule
    else:
        transactions = [t for t in transactions if f(t)]

    return transactions, category
