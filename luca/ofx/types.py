"""Classes for representing OFX institutions and applications."""

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
