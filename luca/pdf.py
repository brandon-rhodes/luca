"""Commands and utilities involving PDF files."""

import subprocess
import sys

def extract_text_from_pdf_file(path):
    command = ['pdftotext', '-layout', path, '-']
    try:
        text = subprocess.check_output(command).decode('utf-8')
    except OSError:
        print >> sys.stderr, error_message.format(path)
        sys.exit(1)
    return text

error_message = """\

Luca cannot find the "pdftotext" command that it needs to load PDF files.
On Ubuntu, you can provide it by installing the "poppler-utils" package.
You can also convert the PDF to text yourself with:

        pdftotext -layout statement.pdf > statement.txt

and provide the text file's path to Luca instead.

Error: cannot process PDF {0}"""
