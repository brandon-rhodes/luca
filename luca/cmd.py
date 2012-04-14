"""The `luca` command line."""

import argparse
from . import files
from .ofx import io

def main():
    parser = argparse.ArgumentParser(
        description='Fra Luca double entry bookkeeping.',
        )
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_f = subparsers.add_parser('fetch', help='fetch')
    parser_f.add_argument('nickname', metavar='institution',
                          help='what to fetch')
    parser_f.set_defaults(func=fetch)

    parser_s = subparsers.add_parser('st', help='status')
    parser_s.set_defaults(func=status)

    args = parser.parse_args()
    args.func(args)

def fetch(args):
    nickname = args.nickname
    logins = files.read_logins()
    login = logins[nickname]
    data = io.get_accounts(login.fi, login.username, login.password)
    files.ofx_create(nickname + '-accounts-DATE.xml', data)
    print 'Read', len(data), 'bytes'

def status(args):
    logins = files.read_logins()
    for (nickname, login) in sorted(logins.items()):
        print nickname, '-'
        accounts = files.get_most_recent_account_list(login)
        if accounts is None:
            print 'you have never run "luca fetch {}"'.format(nickname)
        else:
            pass
