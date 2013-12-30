"""General routines for working with taxes.

This module is experimental and cannot yet be exercised though the Luca
command-line tool.

>>> schedule = federal_monthly_withholding['MJ']
>>> schedule.build_instructions()
       over but_not_over       pay   plus of_excess_over
0    692.00      2179.00      0.00   0.10         692.00
1   2179.00      6733.00    148.70   0.15        2179.00
2   6733.00     12892.00    831.80   0.25        6733.00
3  12892.00     19279.00   2371.55   0.28       12892.00
4  19279.00     33888.00   4159.91   0.33       19279.00
5  33888.00     38192.00   8980.88   0.35       33888.00
6  38192.00     Infinity  10487.28  0.396       38192.00
>>> schedule.compute_tax_on(cents(25000))
Decimal('6047.84')

"""
import pandas as pd
from luca.kit import Decimal, cents, infinity, percent, zero

class TaxSchedule(object):

    def __init__(self, brackets, one_allowance=zero):
        """Return a Pandas tax schedule DataFrame.

        Each element of `brackets` should be a two-element tuple
        ``(over, rate)`` like ``(8926, 15)`` giving the base of the tax
        bracket in dollars ("if the amount is *over*...") and its tax
        rate as a percent.  Each value in the tuple should either be a
        Decimal, or an integer or string that will be automatically
        converted to a Decimal.

        The value `one_allowance` should be the amount of any deduction
        that gets subtracted from income before the tax is computed.

        """
        overs, rates = zip(*brackets)
        df = pd.DataFrame({'over': [cents(value) for value in overs]})
        df['rate'] = [Decimal(rate) * percent for rate in rates]
        df['but_not_over'] = df['over'].shift(-1).fillna(infinity)
        self.brackets = df
        self.one_allowance = cents(one_allowance)

    def build_instructions(self):
        """Return a conventional table of instructions for computing tax.

        The resulting table can be compared to official printed tax
        instructions to verify that this bracket will produce values
        that agree with those of your tax authority.

        """
        df = self.brackets.copy()
        bracket_size = df['but_not_over'] - df['over']
        bracket_cost = (bracket_size * df['rate']).map(cents)
        df['pay'] = bracket_cost.cumsum().shift(1).fillna(zero)
        df['plus'] = df.pop('rate')
        df['of_excess_over'] = df['over']
        return df

    def compute_tax_on(self, wages, allowances=0):
        """Return the tax due on `wages` according to this schedule."""
        df = self.brackets
        wages = wages - allowances * self.one_allowance
        wages_in_bracket = df['but_not_over'].clip_upper(wages) - df['over']
        tax = wages_in_bracket.clip_lower(zero) * df['rate']
        return tax.map(cents).sum()


federal_monthly_withholding = {
    'MJ': TaxSchedule(one_allowance=325, brackets = [
            (692, 10),
            (2179, 15),
            (6733, 25),
            (12892, 28),
            (19279, 33),
            (33888, 35),
            (38192, '39.6'),
            ]),
    }
