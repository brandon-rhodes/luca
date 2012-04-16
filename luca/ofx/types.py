"""Classes representing OFX data."""

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
        self.key = (self.BANKID, self.ACCTID, self.ACCTTYPE)

class Transaction(object):
    def __init__(self, trntype, dtposted, trnamt, fitid, checknum, name):
        self.trntype = trntype
        self.dtposted = dtposted
        self.trnamt = trnamt
        self.fitid = fitid
        self.checknum = checknum
        self.name = name
