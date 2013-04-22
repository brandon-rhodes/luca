"""A kit in the British sense: standard-equipment utilities that code needs."""

from decimal import Decimal, ROUND_HALF_UP

zero = Decimal('0.00')
cent = Decimal('0.01')

def cents(value):
    if not isinstance(value, Decimal):
        value = Decimal(value)
    return value.quantize(cent, rounding=ROUND_HALF_UP)

def zstr(value):
    """Return u'' if `value` is false, else the Unicode string for `value`.

    This is useful on tax forms such as those of the IRS where they
    would rather have you leave a field blank instead of writing an
    explicit zero value like ``0.00``.

    >>> zstr(cent)
    u'0.01'
    >>> zstr(zero)
    u''

    """
    return unicode(value) if value else u''

def zzstr(value):
    """Return Unicode strings ``(dollars, cents)`` for Decimal `value`.

    A zero `value` results in a pair of empty strings ``(u'', u'')``
    instead of ``(u'0', u'00')`` because tax forms typically would
    rather have you leave a field blank if it is zero.

    >>> zzstr(cent)
    [u'0', u'01']
    >>> zzstr(zero)
    [u'', u'']

    This routine is typically used when a form has split up a dollars
    field and a cents field::

        fields['t57'], fields['t58'] = zz(f.line29ag)

    """
    return unicode(value).rsplit('.', 1) if value else [u'', u'']
