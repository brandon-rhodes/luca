"""Classes representing OFX data."""

class Application(object):
    def __init__(self, name, appid, appver):
        self.name = name
        self.appid = appid
        self.appver = appver

class FinancialInstitution(object):
    def __init__(self, name, url, org, fid):
        self.name = name
        self.url = url
        self.org = org
        self.fid = fid

class Account(object):
    def __init__(self, bankid, acctid, accttype):
        self.bankid = bankid
        self.acctid = acctid
        self.accttype = accttype
        self.key = (bankid, acctid, accttype)

class Transaction(object):
    def __init__(self, trntype, dtposted, trnamt, fitid, name):
        self.trntype = trntype
        self.dtposted = dtposted
        self.trnamt = trnamt
        self.fitid = fitid
        self.name = name
