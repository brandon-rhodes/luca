"""The `luca` command line."""

import argparse
from operator import attrgetter
from . import files
from .ofx import io

def main():
    parser = argparse.ArgumentParser(
        description='Fra Luca double entry bookkeeping.',
        )
    subparsers = parser.add_subparsers(help='sub-command help')

    p = subparsers.add_parser('fetch', help='fetch')
    p.add_argument('nickname', metavar='institution',
                          help='from which institution to fetch')
    p.add_argument('-a', action='store_true',
                          help='refresh our account list for the institution')
    p.set_defaults(func=fetch)

    p = subparsers.add_parser('merge', help='merge')
    p.set_defaults(func=merge)

    p = subparsers.add_parser('st', help='status')
    p.set_defaults(func=status)

    args = parser.parse_args()
    args.func(args)

def fetch(args):
    nickname = args.nickname
    logins = files.read_logins()
    login = logins[nickname]
    if args.a:  # or if no account list exists yet, then:
        data = io.fetch_accounts(login.fi, login.username, login.password)
        files.ofx_create(nickname + '-accounts-DATE.xml', data)
        print 'Read', len(data), 'bytes'
        if args.a:
            return
    alist = files.get_most_recent_accounts(login)
    data = io.fetch_activity(login.fi, login.username, login.password, alist)
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
        print t.fitid, t.dtposted, t.trntype, t.trnamt, t.checknum, t.name
        date = '-'.join((t.dtposted[0:4], t.dtposted[4:6], t.dtposted[6:8]))
        p0, p1 = '()' if t.trnamt < 0 else '  '
        print '   {}  {:>12}  {} {!r}'.format(
            date, p0 + str(abs(t.trnamt)) + p1, t.trntype.lower(), t.name,
            )

def status(args):
    logins = files.read_logins()
    emptylist = []
    for (nickname, login) in sorted(logins.items()):
        print nickname, '-',
        accounts = files.get_most_recent_accounts(login)
        balances, transactions = files.get_most_recent_activity(login)
        if accounts is None:
            print 'you have never run "luca fetch -a {}"'.format(nickname)
        elif balances is None:
            print 'you have never run "luca fetch {}"'.format(nickname)
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
                if tlist:
                    print '{:>5} new transactions'.format(len(tlist))
                else:
                    print '      up-to-date'

def negparen(amount):
    if amount < 0:
        return '({:.2f})'.format(-amount)
    return '{:.2f} '.format(amount)
