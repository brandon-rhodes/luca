"""Compile YAML rules into a Python function.

The `compile_tree()` routine is the main function in this module; the
other functions exist to support it.  See the documentation for more
information about writing YAML rules.

"""
import re
from ast import (AST, If, Name, Return, Str, Param, FunctionDef, Interactive,
                 arguments, fix_missing_locations, parse)
from datetime import date

_month_day_re = re.compile('\d\d/\d\d$')
_month_day_to_month_day_re = re.compile('\d\d/\d\d-\d\d/\d\d$')


def compile_tree(tree):
    tree_node = analyze_tree(tree, None)

    node = Interactive(body=[
        FunctionDef(
            name='run_rules',
            args=arguments(args=[Name(id='t', ctx=Param())],
                           vararg=None, kwarg=None, defaults=[]),
            body=[tree_node],
            decorator_list=[]),
        ])
    fixed = fix_missing_locations(node)
    code = compile(fixed, '<luca rule compiler>', 'single')

    globals_dict = {'date': date, 'search': re.search}
    eval(code, globals_dict)
    run_rules = globals_dict['run_rules']
    return run_rules


def eparse(source):
    """Parse the expression in `source` and return its AST.

    This function is careful to remove the ast.Expression object which
    ast.parse() wraps around its return value in eval mode.

    """
    expression_node = parse(source, mode='eval')
    return expression_node.body


def analyze_tree(tree, category):

    if isinstance(tree, list):
        subtrees = [analyze_tree(subtree, category) for subtree in tree]
        return If(eparse('True'), subtrees, [])

    elif isinstance(tree, dict):
        if len(tree) != 1:
            raise ValueError('len(dict) != 1')
        rule, subtree = tree.items()[0]
        r = analyze_rule(rule)
        if isinstance(r, AST):
            test = r
            return If(test, [analyze_tree(subtree, category)], [])
        else:
            category = r
            return analyze_tree(subtree, category)

    else:
        rule = tree
        r = analyze_rule(rule)
        if isinstance(r, AST):
            test = r
            if category is None:
                raise ValueError('bottomed out without category')
            return If(test, [Return(Str(category))], [])
        else:
            category = r
            return Return(Str(category))


def analyze_rule(rule):
    """Return (new_category, None) or (None, test)."""

    if isinstance(rule, str):
        if rule.startswith('/') and rule.endswith('/'):
            return eparse('search(%r, t.description)' % rule[1:-1])
        elif rule.startswith('~/') and rule.endswith('/'):
            return eparse('not search(%r, t.description)' % rule[2:-1])
        else:
            match = _month_day_re.match(rule)
            if match:
                month = int(rule[:2])
                day = int(rule[3:])
                return eparse('t.date.month == %r and t.date.day == %r'
                             % (month, day))
            else:
                match = _month_day_to_month_day_re.match(rule)
                if match:
                    month1 = int(rule[:2])
                    day1 = int(rule[3:5])
                    month2 = int(rule[6:8])
                    day2 = int(rule[9:11])
                    return eparse('date(t.date.year, %r, %r) <= t.date and '
                                 't.date <= date(t.date.year, %r, %r)'
                                 % (month1, day1, month2, day2))

    if isinstance(rule, str):
        n = int(rule) if rule.isdigit() else None
    else:
        n = rule if isinstance(rule, int) else None

    if (n is not None) and 1900 <= n <= 2100:
        return eparse('t.date.year == %r' % n)
    elif (n is not None) and 1 <= n <= 12:
        return eparse('t.date.month == %r' % n)

    category = rule
    return category
