"""A kit in the British sense: standard-equipment utilities code needs."""

from decimal import Decimal, ROUND_HALF_UP

cent = Decimal('0.01')

def cents(value):
    if not isinstance(value, Decimal):
        value = Decimal(value)
    return value.quantize(cent, rounding=ROUND_HALF_UP)
