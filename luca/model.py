"""Data model."""


from decimal import Decimal
from luca.utils import moneyfmt


class BlankLine(object):
    def format_for_ledger(self):
        print


class Comment(object):
    def __init__(self, line):
        self.line = line.strip()

    def format_for_ledger(self):
        print ';', self.line


class Transaction(object):

    def __init__(self, account_name, posted_date, effective_date,
                 description, amount, comments, is_posted=True):
        self.account_name = account_name
        self.posted_date = posted_date
        self.effective_date = effective_date
        self.description = description
        self.amount = Decimal(amount.strip('$').replace(',', ''))
        self.comments = comments
        self.category = 'Undecided'
        self.is_posted = is_posted

    def format_for_ledger(self):
        account_name = self.account_name
        category = self.category

        amount = self.amount
        if amount < 0:
            amount = -amount
            account_name, category = category, account_name

        pdate = self.posted_date
        datestr = '{}/{}/{}'.format(pdate.year, pdate.month, pdate.day)
        edate = self.effective_date
        if edate is not None:
            datestr += '={}/{}/{}'.format(edate.year, edate.month, edate.day)
        print datestr,
        if self.is_posted:
            print '*',
        print '{}'.format(self.description)
        print '    {:40}  {:>14}'.format(
            account_name, moneyfmt(amount, curr='$'))
        print '    {}'.format(category)
        for comment in self.comments:
            comment = comment.strip()
            if comment:
                print ';', comment
        print

    def key(self):
        return self.posted_date
