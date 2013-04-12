from unittest import TestCase
from luca.kit import Decimal, cents

class TestKit(TestCase):

    def test_cents_round_down(self):
        assert cents('1.234') == Decimal('1.23')

    def test_cents_round_up(self):
        assert cents('1.235') == Decimal('1.24')
