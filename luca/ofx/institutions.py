"""OFX institution FID codes."""

from .types import FinancialInstitution
from .applications import Quicken2011 as Q, Money2007 as M

db = {}

def add(*args):
    fi = FinancialInstitution(*args)
    db[fi.name] = fi

add('Chase Credit Cards', 'https://ofx.chase.com',
    103, 'B1', 10898, Q)

add('Delta Community Credit Union',
    'https://appweb.deltacommunitycu.com/ofxroot/directtocore.asp',
    103, 'decu.org', 3328, Q)

add('Scottrade', 'https://ofx.scottrade.com',
    103, 'Scottrade', 777, Q)

add('TD Ameritrade', 'https://ofxs.ameritrade.com/cgi-bin/apps/OFX',
    211, 'ameritrade.com', 5024, Q)
