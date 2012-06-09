"""Classes representing OFX data."""

from decimal import Decimal

class Mass(object):
    """Objects whose attributes are mass-assigned during initialization."""

    def __init__(self, attrs):
        self.__dict__.update(attrs)

class Application(object):
    def __init__(self, name, appid, appver):
        self.name = name
        self.appid = appid
        self.appver = appver

class FinancialInstitution(object):
    def __init__(self, name, url, version, org, fid, app,
                 supports_multiple_requests=True):
        self.name = name
        self.url = url
        self.org = org
        self.fid = fid
        self.app = app
        self.version = version
        self.supports_multiple_requests = supports_multiple_requests

class Account(Mass):
    def __init__(self, attrs):
        super(Account, self).__init__({
                tag.lower(): text for tag, text in attrs.iteritems()
                })
        self.key = account_key(attrs)

def account_key(attrs):
    if 'BANKID' in attrs:
        return (attrs['BANKID'], attrs['ACCTID'], attrs['ACCTTYPE'])
    elif 'BROKERID' in attrs:
        return (attrs['BROKERID'], attrs['ACCTID'])
    else:
        return (attrs['ACCTID'],)

class Transaction(Mass):
    def __init__(self, attrs):
        super(Transaction, self).__init__(attrs)
        self.trnamt = Decimal(self.trnamt)
