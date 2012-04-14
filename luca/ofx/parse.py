import re
from lxml import etree

def fromstring(data):
    """Parse SGML OFX `data` and return an lxml elementtree."""
    data = re.sub(r'([^>\s])(\s*)<', r'\1</><', data)
    parser = etree.XMLParser(recover=True)
    return etree.fromstring(data, parser=parser)
