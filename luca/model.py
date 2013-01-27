"""Data model."""


from decimal import Decimal
from luca.utils import moneyfmt


class Transaction(object):

    def __init__(self, account_name, date, description, amount, comments,
                 is_posted=True):
        self.account_name = account_name
        self.date = date
        self.description = description
        self.amount = Decimal(amount)
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

        date = self.date
        print '{}/{}'.format(date.month, date.day),
        if self.is_posted == 'posted':
            print '*',
        print '{}'.format(self.description)
        print '    {:40}  {:>14}'.format(
            account_name, moneyfmt(amount, curr='$'))
        print '    {}'.format(category)
        for comment in self.comments:
            print ';', comment.strip()
        print
