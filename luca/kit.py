"""A kit in the British sense: standard-equipment utilities code needs."""

from decimal import Decimal, ROUND_HALF_UP

cent = Decimal('0.01')

def cents(decimal_value):
    return decimal_value.quantize(cent, rounding=ROUND_HALF_UP)
