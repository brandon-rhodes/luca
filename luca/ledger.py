"""Read and write plain-text files full of Ledger transactions."""

from datetime import date as Date

class Ledger(object):
    """Parse and handle the data from a traditional plain-text-file ledger.

    The file format is documented at: http://ledger-cli.org/

    """
    def __init__(self):
        self.accounts = set()

    def parse(self, source):
        lines = source.splitlines()
        lines.reverse()
        line = lines.pop()
        while lines:
            if not line:
                line = lines.pop()
                continue
            if not line[0].isdigit():
                print('Unrecognized line: {}'.format(line))
                line = lines.pop()
                continue
            date_string, description = line.split(None, 1)
            date = Date(*(int(n) for n in date_string.split('/')))
            while lines:
                line = lines.pop()
                if not line or not line[0].isspace() or not line.strip():
                    break
                words = line.split()
                account_name = words[0]
                if len(words) > 1:
                    dollar_string = words[1]
                self.accounts.add(account_name)
                # do something with dollar_string
