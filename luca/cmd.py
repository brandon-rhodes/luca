"""The `luca` command line."""

import argparse
from . import files
from .ofx import io, types

def main():
    parser = argparse.ArgumentParser(
        description='Fra Luca double entry bookkeeping.',
        )
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_f = subparsers.add_parser('fetch', help='fetch')
    parser_f.add_argument('nickname', metavar='institution',
                          help='from which institution to fetch')
    parser_f.add_argument('-a', action='store_true',
                          help='refresh our account list for the institution')
    parser_f.set_defaults(func=fetch)

    parser_s = subparsers.add_parser('st', help='status')
    parser_s.set_defaults(func=status)

    args = parser.parse_args()
    args.func(args)

def fetch(args):
    nickname = args.nickname
    logins = files.read_logins()
    login = logins[nickname]
    if False:
        # If "-a" is specified, or if no account list exists yet, then:
        data = io.fetch_accounts(login.fi, login.username, login.password)
        files.ofx_create(nickname + '-accounts-DATE.xml', data)
        print 'Read', len(data), 'bytes'
    alist = files.get_most_recent_account_list(login)
    data = io.fetch_activity(login.fi, login.username, login.password, alist)
    files.ofx_create(nickname + '-activity-DATE.xml', data)

def status(args):
    logins = files.read_logins()
    for (nickname, login) in sorted(logins.items()):
        print nickname, '-',
        accounts = files.get_most_recent_accounts(login)
        activity = files.get_most_recent_activity(login)
        if accounts is None:
            print 'you have never run "luca fetch -a {}"'.format(nickname)
        elif activity is None:
            print 'you have never run "luca fetch {}"'.format(nickname)
        else:
            print
        if accounts:
            for account in accounts:
                print '  {:20} {:14}'.format(account.id, account.type),
                if activity:
                    if account.id in activity:
                        balance = activity[account.id]
                        print '{:>18}'.format(balance)
                    else:
                        print '(no balance information)'
                else:
                    print
