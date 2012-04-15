import re
from lxml import etree
from . import types

def fromstring(data):
    """Parse SGML OFX `data` and return an lxml elementtree."""
    data = re.sub(
        r'<([^>]+)>'    # if we see a tag, named \1
        r'([^<]+)'      # that holds non-empty text, stored in \2
        r'(?!</)',      # which is not followed by a closing tag,
        r'<\1>\2</\1>', # then add a closing tag ourselves
        data)
    parser = etree.XMLParser()
    return etree.fromstring(data, parser=parser)

def accounts(ofx):
    """Return the list of accounts in the XML tree `ofx`."""
    return [ types.Account(x.find('.//ACCTTYPE').text,
                           x.find('.//ACCTID').text,
                           x.find('.//BANKACCTFROM'))
             for x in ofx.findall('.//BANKACCTINFO') ]

def activity(ofx):
    """Return activity."""
    return {
        x.find('.//ACCTID').text: x.find('.//BALAMT').text
        for x in ofx.findall('.//STMTRS')
        }
