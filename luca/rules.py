"""Apply YAML rules to transactions."""

import re


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


def apply_rule(transactions, category, rule):
    """Return (transactions, category)."""

    print repr(rule)

    if isinstance(rule, str):
        s = rule
        n = int(rule) if rule.isdigit() else None
    elif isinstance(rule, int):
        s = str(rule)
        n = rule
    else:
        raise ValueError('no rule looks like this! %r' % rule)

    f = None

    if (n is not None) and 1900 <= n <= 2100:
        f = lambda t: t.date.year == n
    elif (n is not None) and 1 <= n <= 12:
        f = lambda t: t.date.month == n
    elif (s is not None) and s.startswith('/') and s.endswith('/'):
        r = re.compile(s[1:-1])
        f = lambda t: r.search(t.description)

    if f is None:
        category = rule
    else:
        transactions = [t for t in transactions if f(t)]

    return transactions, category
