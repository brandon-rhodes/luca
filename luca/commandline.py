"""Fra Luca financial accounting utilities.

Usage:
  luca forms
  luca form <name> [<version>]
  luca complete [-j] <tax-filing.json>...
  luca tally [-bcCt] <rules.yaml> <statement-path>...
  luca (-h | --help)

Options:
  -b    Show a running balance for each account, by date
  -c    Force ANSI color codes even if output is not a tty
  -C    Force off ANSI color codes and output plain text
  -j    Only update JSON files; do not produce new PDF printouts
  -t    Show the transactions that have been sorted into every category

"""
import textwrap

import blessings
from docopt import docopt

import luca.forms.actions
import luca.importer.dccu
import luca.importer.yodlee
from . import files
from .ofx import io


def main():
    args = docopt(__doc__)
    force_styling = None if args['-C'] else True if args['-c'] else False
    terminal=blessings.Terminal(force_styling=force_styling)
    for line in _main(args, terminal):
        print line


def _main(args, terminal):

    t = terminal

    if args['forms']:
        indent = 14

        if t.width:
            fill = textwrap.TextWrapper(
                width=t.width - 2,
                initial_indent=' ' * indent,
                subsequent_indent=' ' * indent,
                ).fill
        else:
            indent_spaces = ' ' * indent
            fill = lambda s: indent_spaces + s

        form_seq = luca.forms.actions.list_forms()
        for module_name, title, versions in sorted(form_seq):
            print t.green('{:<{}}').format(module_name, indent - 1),
            print t.blue(fill(title)[14:])

    elif args['form']:
        luca.forms.actions.print_defaults(args['<name>'], args['<version>'])

    elif args['complete']:
        luca.forms.actions.complete(args['<tax-filing.json>'], not args['-j'])

    elif args['tally']:
        from luca.tally import run_yaml_file
        lines = run_yaml_file(terminal, args['<rules.yaml>'],
                              args['<statement-path>'], args['-b'], args['-t'])
        for line in lines:
            yield line


def old_download_command(args):
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
