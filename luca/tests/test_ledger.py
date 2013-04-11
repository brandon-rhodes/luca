import unittest
from luca.ledger import Ledger

class LedgerTests(unittest.TestCase):

    def test_parse(self):
        ledger = Ledger()
        ledger.parse(sample_data)
        self.assertEqual(ledger.accounts,
                         set(['Expenses:Books', 'Liabilities:Visa']))

sample_data = """

2004/05/27 Amazon.com
      Expenses:Books                $187.19
      Liabilities:Visa

"""
