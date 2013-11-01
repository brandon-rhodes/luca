"""Trial of rule-driven accounting."""

import re
import subprocess
from bottle import route, run, template
from decimal import Decimal

transaction_start = re.compile(ur"""
    \s*(\d*)          # "Reference Number"
    \s+(\d\d)/(\d\d)  # "Trans Date"
    \s+(\d\d)/(\d\d)  # "Post Date"
    \s+([^$]*)        # "Description"
    \$(\d+\.\d\d)$    # "Amount"
    """, re.VERBOSE)

class T(object):
    pass

@route('/')
def index(name='World'):
    command = ['pdftotext', '-layout', 'rms-visa-2013-10.pdf', '-']
    content = subprocess.check_output(command).decode('utf-8')

    transactions = []
    lines = iter(content.splitlines())
    i = 0

    for line in lines:
        match = transaction_start.match(line)
        if match:
            t = T()
            t.date = match.group(2)
            description = match.group(6).strip()
            if description.endswith(' **'):
                description = description[:-3].strip()
            t.description = description
            t.amount = Decimal(match.group(7))
            t.comments = []
            transactions.append(t)
            i = match.start(6)
        elif i and line[:i].isspace() and not line[i:i+1].isspace():
            t.comments.append(line.strip())
        elif i:
            i = 0

    foo = ''
    for t in transactions:
        foo += '%s %s %s %s\n' % (t.date, t.amount, repr(t.description), t.comments)

    return template('<pre>{{foo}}</pre><hr><pre>{{name}}</pre>!',
                    foo=foo, name=content)

def main():
    run(host='localhost', port=8080, reloader=True, interval=0.2)

if __name__ == '__main__':
    main()
