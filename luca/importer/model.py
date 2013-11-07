"""Models that importers can use for representing financial data."""

class Transaction(object):
    __slots__ = [
        'account',
        'category',  # TODO: remove
        'date',
        'posting_date',
        'description',
        'amount',
        ]

    def __init__(self):
        self.category = None
