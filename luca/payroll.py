"""Routines for computing a payroll.

This module is experimental and cannot yet be exercised though the Luca
command-line tool.

"""
import pandas
from luca.kit import Decimal, cents, zero
from luca.taxes import TaxSchedule, federal_monthly_withholding

# "ss" - Social Security
# "mc" - Medicare

D = lambda s: Decimal(s.replace(',', ''))
ss_limit = D('113700.00')
ss_rate = D('0.062')
mc_rate = D('0.0145')
bluffton_school_rate = D('0.005')      # From SDIT_Instructions.pdf
monthly_school_exemption = D('54.17')  # From SDIT_Instructions.pdf

def compute_payroll(wage_schedule, state_withholding, exemptions):
    """Return a 2013 payroll schedule as a Pandas DataFrame."""

    month_integers = range(1, len(wage_schedule) + 1)

    pd = pandas.DataFrame(index=month_integers)
    pd['wages'] = wage_schedule

    compute = federal_monthly_withholding['MJ'].compute_tax_on
    pd['fedwh'] = [compute(amount, exemptions) for amount in wage_schedule]

    ss_excess = (pd['wages'].cumsum() - ss_limit).clip(zero)
    pd['ss_wages'] = (pd['wages'] - ss_excess).clip(zero)
    pd['ss'] = [cents(n) for n in ss_rate * pd['ss_wages']]
    pd['mc'] = [cents(n) for n in mc_rate * pd['wages']]
    pd['ss2'] = [cents(n) for n in ss_rate * 2 * pd['ss_wages']]
    pd['mc2'] = [cents(n) for n in mc_rate * 2 * pd['wages']]

    pd['statewh'] = [state_withholding(wage)
                     for month, wage in pd['wages'].iteritems()]
    pd['localwh'] = [cents((wage - monthly_school_exemption * exemptions)
                           * bluffton_school_rate) for wage in pd['wages']]

    pd['paycheck'] = (pd['wages'] - pd['fedwh'] - pd['ss'] - pd['mc']
                      - pd['statewh'] - pd['localwh'])

    return pd

def print_report(pd):
    """Display pay stub and tax form totals for the year."""

    # Compute the totals.

    pd['f941'] = pd['fedwh'] + pd['ss2'] + pd['mc2']

    # Display the totals.

    quarter = lambda month: 'Q{}'.format((month + 2) // 3)
    year = lambda month: 2013

    print
    print 'Paystubs'
    columns = ['wages', 'fedwh', 'ss', 'mc', 'statewh', 'localwh', 'paycheck']
    print pd[columns]

    print
    print 'Form W-2'
    w2 = pd[columns].groupby(year).sum()
    print w2

    print
    print 'Form 941 monthly tax deposits'
    columns = ['fedwh', 'ss2', 'mc2', 'f941']
    print pd[columns]
    print 'Form 941'
    columns = ['wages', 'fedwh', 'ss_wages', 'ss2', 'mc2', 'f941']
    print pd[columns].groupby(quarter).sum()

    print
    columns = ['statewh', 'localwh']
    print pd[columns].groupby(quarter).sum()
    print pd[columns].groupby(year).sum()

    print

def main():
    ohio_withholding = TaxSchedule(
        [(0, '0.5'), (5000, 1), (10000, 2), (15000, '2.5'), (20000, 3),
         (40000, '3.5'), (80000, 4), (100000, 5)],
        Decimal('650')/Decimal('12'))
    wage_schedule = (
        [D('2,500.00')] * 6
        )
    exemptions = 2

    pd = compute_payroll(wage_schedule, ohio_withholding.compute_tax_on,
                         exemptions)
    print_report(pd)

if __name__ == '__main__':
    main()
