"""Models that importers can use for representing financial data."""

class Balance(object):
    """An assertion of an account's balance at the *beginning* of ``date``."""

    __slots__ = [
        'account',
        'date',
        'amount',
        ]

    event_type = 'balance'

    def __repr__(self):
        return '<Balance %r %s %s>' % (self.account, self.date, self.amount)

class Transaction(object):
    """A record stating that that money moved in or out of an account."""

    __slots__ = [
        'account',
        'category',  # TODO: remove
        'date',
        'posting_date',
        'description',
        'amount',
        ]

    event_type = 'transaction'

    def __init__(self):
        self.category = None


def can_import_texts_containing(*substrings):
    def annotate(importer):
        def does_this_match(text):
            return all((substring in text) for substring in substrings)
        importer.does_this_match = does_this_match
        return importer
    return annotate
