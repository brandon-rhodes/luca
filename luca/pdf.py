"""Commands and utilities involving PDF files."""

import subprocess

def extract_text_from_pdf_file(path):
    command = ['pdftotext', '-layout', path, '-']
    text = subprocess.check_output(command).decode('utf-8')
    return text
