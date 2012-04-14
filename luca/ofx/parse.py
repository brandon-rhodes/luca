import re
from lxml import etree
from . import types

def fromstring(data):
    """Parse SGML OFX `data` and return an lxml elementtree."""
    data = re.sub(r'([^>\s])(\s*)<', r'\1</><', data)
    parser = etree.XMLParser(recover=True)
    return etree.fromstring(data, parser=parser)

def accounts(ofx):
    """Return the list of accounts in the XML tree `ofx`."""
    return [ types.Account(x.find('.//ACCTTYPE').text,
                           x.find('.//ACCTID').text,
                           x.find('.//BANKACCTFROM'))
             for x in ofx.findall('.//BANKACCTINFO') ]
