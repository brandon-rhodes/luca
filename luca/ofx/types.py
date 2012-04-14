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
    def __init__(self, type, id, bankacctfrom):
        self.type = type
        self.id = id
        self.bankacctfrom = bankacctfrom
