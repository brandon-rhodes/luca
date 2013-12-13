"""Models that importers can use for representing financial data."""

class _Balance(object):
    """An assertion of an account's balance at a point in time."""

    __slots__ = [
        'account',
        'date',
        'amount',
        ]

    event_type = 'balance'

    def __repr__(self):
        return '<%s %r %s %s>' % (type(self).__name__, self.account,
                                  self.date, self.amount)

class StartOfDayBalance(_Balance):
    """An assertion of an account's balance at the end of ``date``."""

    event_type = 'balance'
    sort_key = -1               # before today's transactions

class EndOfDayBalance(_Balance):
    """An assertion of an account's balance at the end of ``date``."""

    event_type = 'balance'
    sort_key = 1                # after today's transactions


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
    sort_key = 0  # between start-of-day balances and end-of-day balances

    def __init__(self):
        self.category = None


def can_import_texts_containing(*substrings):
    def annotate(importer):
        def does_this_match(text):
            return all((substring in text) for substring in substrings)
        importer.does_this_match = does_this_match
        return importer
    return annotate
