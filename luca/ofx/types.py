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
    def __init__(self, name, url, org, fid, version):
        self.name = name
        self.url = url
        self.org = org
        self.fid = fid
        self.version = version

class Account(Mass):
    def __init__(self, attrs):
        super(Account, self).__init__(attrs)
        if self.type == 'bank':
            self.key = (self.bankid, self.acctid, self.accttype)
        elif self.type == 'cc':
            self.key = (self.acctid,)
        elif self.type == 'inv':
            self.key = (self.brokerid, self.acctid)

class Transaction(Mass):
    def __init__(self, attrs):
        super(Transaction, self).__init__(attrs)
        self.trnamt = Decimal(self.trnamt)
