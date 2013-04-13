"""The `luca` command line."""

import argparse
import os
import sys

import luca.forms.actions
import luca.importer.dccu
import luca.importer.yodlee
from operator import attrgetter
from . import files
from .model import Transaction
from .ofx import io

def main():
    parser = argparse.ArgumentParser(
        description='Fra Luca double entry bookkeeping.',
        )
    subparsers = parser.add_subparsers(help='sub-command help')

    p = subparsers.add_parser('complete', help='complete a tax form')
    p.add_argument('json_path', metavar='json-path',
                   help='Path to the JSON file containing the form')
    p.add_argument('pdf_path', metavar='pdf-path', nargs='?',
                   help='Path to the blank PDF form to fill in')
    p.set_defaults(func=complete)

    p = subparsers.add_parser('defaults', help='print the default JSON'
                              ' data for a tax form')
    p.add_argument('form_name', metavar='form-name',
                   help='Name of the form, like us.irs1040sa')
    p.set_defaults(func=defaults)

    p = subparsers.add_parser('download', help='download')
    p.add_argument('nickname', metavar='institution',
                          help='from which institution to download')
    p.add_argument('-a', action='store_true',
                          help='refresh our account list for the institution')
    p.set_defaults(func=download)

    p = subparsers.add_parser('import', help='import')
    p.set_defaults(func=import_subcommand)
    p.add_argument('path', help='file from which to import transactions',
                   nargs='*')

    p = subparsers.add_parser('merge', help='merge')
    p.set_defaults(func=merge)

    for name in 'st', 'status':
        p = subparsers.add_parser(name, help='status')
        p.set_defaults(func=status)

    args = parser.parse_args()
    args.func(args)

def complete(args):
    luca.forms.actions.complete(args.json_path, args.pdf_path)

def defaults(args):
    luca.forms.actions.print_defaults(args.form_name)

def download(args):
    nickname = args.nickname
    logins = files.read_logins()
    login = logins[nickname]
    if args.a:  # or if no account list exists yet, then:
        data = io.download_accounts(login.fi, login.username, login.password)
        files.ofx_create(nickname + '-accounts-DATE.xml', data)
        print 'Read', len(data), 'bytes'
        if args.a:
            return
    account_list = files.get_most_recent_accounts(login)
    if login.fi.supports_multiple_requests:
        operations = [account_list]  # single request listing every account
    else:
        operations = [[account] for account in account_list]
    for op in operations:
        data = io.download_activity(login.fi, login.username, login.password, op)
        files.ofx_create(nickname + '-activity-DATE.xml', data)

def merge(args):
    logins = files.read_logins()
    transactions = []
    for (nickname, login) in sorted(logins.items()):
        #accounts = files.get_most_recent_accounts(login)
        balances, more_transactions = files.get_most_recent_activity(login)
        for tranlist in more_transactions.values():
            transactions.extend(tranlist)
    transactions.sort(key=attrgetter('dtposted'))
    for t in transactions:
        # print t.fitid
        date = '/'.join((t.dtposted[0:4], t.dtposted[4:6], t.dtposted[6:8]))
        p0, p1 = '()' if t.trnamt < 0 else '  '

        print 'a', t.trntype, t.trnamt
        print 'b', '   {} {!r}'.format(
            p0 + str(abs(t.trnamt)) + p1, t.name,
            )

        print date,
        if hasattr(t, 'checknum'):
            print '({})'.format(t.checknum.strip('0'))
        print
        print


def import_subcommand(args):
    transactions = []
    for path in args.path:
        more = import_action(path)
        transactions.extend(more)

    transactions.sort(key=Transaction.key)
    for t in transactions:
        t.format_for_ledger()

def import_action(path):
    if not os.path.exists(path):
        print >>sys.stderr, 'No such path:', path
        exit(1)

    return luca.importer.dccu.parse(path)

    with open(path) as f:
        content = f.read()
    assert luca.importer.yodlee.matches(content)
    luca.importer.yodlee.parse(content)


def status(args):
    logins = files.read_logins()
    emptylist = []
    for (nickname, login) in sorted(logins.items()):
        print nickname, '-',
        accounts = files.get_most_recent_accounts(login)
        balances, transactions = files.get_most_recent_activity(login)
        if accounts is None:
            print
            print '  you have never run "luca download -a {}"'.format(nickname)
        elif balances is None:
            print
            print '  you have never run "luca download {}"'.format(nickname)
        else:
            print
        if accounts:
            for account in accounts:
                print '  {:20} {:14}'.format(
                    account.acctid,
                    getattr(account, 'accttype', ''),
                    ),
                if balances:
                    if account.key in balances:
                        balance = balances[account.key]
                        print '{:>12}'.format(negparen(balance)),
                    else:
                        print '(no balance information)',
                tlist = transactions.get(account.key, emptylist)
                print
                if tlist:
                    for t in tlist:
                        print '{}-{}-{}'.format(t.dtposted[0:4],
                                                t.dtposted[4:6],
                                                t.dtposted[6:8]),
                        print repr(t.name),
                        print t.trnamt
                if tlist:
                    print '{:>5} new transactions'.format(len(tlist))
                else:
                    print '      up-to-date'

def negparen(amount):
    if amount < 0:
        return '({:.2f})'.format(-amount)
    return '{:.2f} '.format(amount)
