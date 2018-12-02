"""OFX institution FID codes."""

from .types import FinancialInstitution
from .applications import Quicken2011 as Q, Money2007 as M

db = {}

def add(*args, **kw):
    fi = FinancialInstitution(*args, **kw)
    db[fi.name] = fi

def add2(fi):
    db[fi.name] = fi

add('Chase Credit Cards', 'https://ofx.chase.com',
    103, 'B1', 10898, Q)

add('Delta Community Credit Union',
    'https://appweb.deltacommunitycu.com/ofxroot/directtocore.asp',
    103, 'decu.org', 3328, Q)

add2(FinancialInstitution(
    name='Fidelity',
    url='https://ofx.fidelity.com/ftgw/OFX/clients/download',
    version=211,
    org='fidelity.com',
    fid=3328,
    app=Q,
))

add('First National Bank of Pandora',
    'https://www20.onlinebank.com/OROFX16Listener',
    103, 'orcc', 1824, Q, supports_multiple_requests=False)

add('Scottrade', 'https://ofx.scottrade.com',
    103, 'Scottrade', 777, Q)

add('TD Ameritrade', 'https://ofxs.ameritrade.com/cgi-bin/apps/OFX',
    211, 'ameritrade.com', 5024, Q)

add('US Bank', 'https://www.oasis.cfree.com/1401.ofxgp',
    211, 'US Bank', 1401, M)
