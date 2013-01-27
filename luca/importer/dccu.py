"""Delta Community Credit Union PDF statements."""

import re
import subprocess
import luca.files
from datetime import date
from luca.model import Transaction


date_re = re.compile(r'\d\d/\d\d$')
amount_re = re.compile(r'[\d,]+\.\d\d-?$')

def matches(content):
    return True  # TODO: put real check here


def parse(filename):

    command = ['pdftotext', '-layout', filename, '-']
    content = subprocess.check_output(command)

    config = luca.files.parse_ini()

    if config.has_option('import', 'replace'):
        for line in config.get('import', 'replace').splitlines():
            line = line.strip()
            if not line:
                continue
            pattern, replacement = line.split('|')
            content = content.replace(pattern, replacement)

    words = content.split()
    starts = [ i for i in range(len(words) - 1)
               if words[i] == 'Balance' and words[i+1] == 'Forward' ]

    for start in starts:
        section = words[start:]

        n = start
        while words[n] != 'ID':
            n -= 1
        account_name = ' '.join(words[n+1:start])

        end = section.index('Ending') + 3
        del section[end:]

        # The `section` word list is now established.

        year = 2012

        dates = [ i for i in range(len(section))
                  if date_re.match(section[i]) ]

        for m in range(len(dates) - 1):
            i, j = dates[m], dates[m+1]
            trans = section[i:j]
            for k in range(len(trans)):
                if amount_re.match(trans[k]) and amount_re.match(trans[k+1]):
                    break
            month, day = [ int(s) for s in trans[0].split('/') ]
            t = Transaction(
                account_name=account_name,
                date=date(year, month, day),
                description=' '.join(trans[1:k-1]),
                amount=trans[k],
                # at k+1 is the new balance
                comments=[' '.join(trans[k+2:])],
                )
            t.format_for_ledger()

        i = dates[-1]
        assert section[i+1] == 'Ending'
        assert section[i+2] == 'Balance'

        # print 'end', section[i], section[i+3]
