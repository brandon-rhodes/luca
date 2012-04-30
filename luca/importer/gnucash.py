import gzip
import xml.etree.cElementTree as ET

def parse(path):
    """Open a GnuCash file and return a Book object that manages it."""
    tree = ET.parse(gzip.open(path))
    book = tree.find('.//' + tag('gnc:book'))
    for a in book.findall('.//' + tag('gnc:account')):
        print a
    for t in book.findall('.//' + tag('gnc:transaction')):
        print t

def tag(colontag):
    """Return the fully-qualified XML tag name for a GnuCash tag."""
    prefix, name = colontag.split(':')
    return '{http://www.gnucash.org/XML/%s}%s' % (prefix, name)
