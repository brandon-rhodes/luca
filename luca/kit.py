"""A kit in the British sense: standard-equipment utilities that code needs."""

import re
from decimal import Decimal, ROUND_HALF_UP

# Currency conveniences.

zero = Decimal('0.00')
cent = Decimal('0.01')

def cents(value):
    if not isinstance(value, Decimal):
        value = Decimal(value)
    return value.quantize(cent, rounding=ROUND_HALF_UP)

def zstr(value):
    """Return u'' for a false `value`, else format it with thousands commas.

    This is useful on tax forms such as those of the IRS where they
    would rather have you leave a field blank instead of writing an
    explicit zero value like ``0.00``.  Includes thousands commas.

    >>> zstr(Decimal('1234567.89'))
    u'1,234,567.89'
    >>> zstr(zero)
    u''

    """
    return u'{:,}'.format(value) if value else u''

def zzstr(value):
    """Return Unicode strings ``(dollars, cents)`` for Decimal `value`.

    A zero `value` results in a pair of empty strings ``(u'', u'')``
    instead of ``(u'0', u'00')`` because tax forms typically would
    rather have you leave a field blank if it is zero.  A non-zero
    value, if large enough, will include thousands commas.

    >>> zzstr(Decimal('1234567.89'))
    [u'1,234,567', u'89']
    >>> zzstr(zero)
    [u'', u'']

    This routine is typically used when a form has split up a dollars
    field and a cents field::

        fields['t57'], fields['t58'] = zz(f.line29ag)

    """
    return u'{:,}'.format(value).rsplit('.', 1) if value else [u'', u'']

# Time periods.

class validate(object):

    @staticmethod
    def year(y):
        if not isinstance(y, int) or y < 1000 or y > 9999:
            raise ValueError('please specify the year as a four-digit '
                             'integer, not a value like {!r}'.format(y))

    @staticmethod
    def quarter(q):
        if not isinstance(q, int) or q < 1 or q > 4:
            raise ValueError('please specify the quarter as an integer '
                             '1-4, not a value like {!r}'.format(q))
