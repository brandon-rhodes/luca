
Accounting For My S-Corporation
===============================

.. note::

   I have written this Luca documentation
   to remind myself how to use my ``luca`` command,
   which I maintain for my own personal use.
   That is why this documentation is written in the first person:
   it is simply my own record of how I use the tool.
   It is in no way intended as advice —
   whether technical, financial, or legal —
   about how *other* people ought to be filling out their own tax forms.

The Master Diagram
------------------

.. raw:: html

 <style>
  #taxtable td {
   vertical-align: top;
  }
  #taxtable .foo {
   border: 2px solid #d7a14d; background-color: #f9ebd4;
   text-align: center; font-weight: bold;
  }
  #taxtable .dotted {
   border: 2px dashed black;
  }
  #taxtable .tax {
   color: #800;
  }
  #taxtable .comment {
   text-align:center; font-style: italic;
  }
 </style>
 <table id="taxtable">

  <tr>
   <th colspan=4>
    Form 1120S<br>U.S. Income Tax Return for an S-Corporation
   </th>
  </tr>
  <tr>
   <td colspan=4 width="100%" class="foo">
    $100,000<br>Total Income<br>(line 6)
   </td>
  </tr>
  <tr>
   <td colspan=4 width="100%" class="comment">
    — which gets split into two pieces:
   </td>
  </tr>
  <tr>
   <td colspan=1 width="25%" class="foo">
    $25,000<br>Ordinary Business Income<br>(line 21)
   </td>
   <td colspan=3 width="75%" class="foo">
    $75,000<br>Total Deductions<br>(line 20)
   </td>
  </tr>
  <tr>
   <td></td>
   <td colspan=3 width="100%" class="comment">
    — which itself gets split in two:
   </td>
  </tr>
  <tr>
   <td colspan=1 width="25%" class="dotted">
   </td>
   <td colspan=2 width="50%" class="foo">
    $50,000<br>Compensation of Officers<br>(line 7)
   </td>
   <td colspan=1 width="25%" class="foo">
    $25,000<br>Other Deductions<br>(lines 8–19)
   </td>
  </tr>
  <tr>
   <td colspan=4 width="100%">
    <p>
     An S-Corporation receives income through the year
     as customers buy its products or pay invoices for its services.
     Here, I imagine that my annual proceeds totalled $100,000.
     From 1120S invites me to subtract from the total income
     the money that it took to actually operate the corporation.
     My largest such expense is often my own salary,
     since there are often only a few other expenses involved
     in sitting around and programming most of the year —
     like travel, conferences, and taxes.
     The amount of “profit” that remains
     when my salary and other company expenses have been subtracted out
     is called “Ordinary Business Income” on 1120S.
    </p>
    <p>
     I have broken out the salary expense
     from all other 1120S expenses on this particular diagram
     because, in the diagrams that follow, that particular expense
     gets treated very differently
     on the rest of the relevant tax forms.
    </p>
   </td>
  </tr>

  <tr>
   <th colspan=4>
    Form W-2 Wage and Tax Statement
   </th>
  </tr>
  <tr>
   <td colspan=1 width="25%" class="dotted"></td>
   <td colspan=2 width="50%" class="foo">
    $50,000<br>Social Security Wages (box 3)<br>Medicare Wages (box 5)
   </td>
   <td colspan=1 width="25%" class="dotted"></td>
  </tr>
  <tr>
   <td colspan=1 width="25%"></td>
   <td colspan=3 width="75%" class="tax">
    $50,000 × 6.20% = Social security tax withheld (box 4)<br>
    $50,000 × 1.45% = Medicare tax withheld (box 6)
   </td>
  </tr>
  <tr>
   <td colspan=4 width="100%">
    <p>
     Form W-2 explains why my monthly paycheck
     is so significantly less than my actual salary:
     because my income has already turned into taxes
     before I ever see it.
     The Social Security and Medicare taxes are especially stark.
     At least for the first hundred thousand in income
     they offer no deductions, no exceptions, and brook no argument.
    </p>
    <p>
     That is why there is nothing like Form 1040
     for the Social Security tax or for the Medicare tax.
     They are sheerly mechanical and automatic.
     My salary is multiplied by a fixed percentage
     and the resulting amount is earmarked for the government
     instead of being included in my paycheck.
    </p>
    <p>
     But there is more going on in Form W-2 when I consider wages:
    </p>
   </td>
  </tr>
  <tr>
   <td colspan=1 width="25%" class="dotted"></td>
   <td colspan=1 width="35%" class="foo">
    $35,000<br>Wages (Box 1)
   </td>
   <td colspan=1 width="15%" class="foo">
    $15,000<br>401(k) Contribution
   </td>
   <td colspan=1 width="25%" class="dotted"></td>
  </tr>
  <tr>
   <td colspan=1 width="25%"></td>
   <td colspan=3 width="75%" class="tax">
    $35,000 × ? = Federal income tax withheld (box 2)
   </td>
  </tr>
  <tr>
   <td colspan=4 width="100%">
    <p>
     The Federal Income tax is more forgiving:
     it applies only to that portion of my income
     which I am not immediately contributing into a tax-deferred
     retirement investment like a 401(k).
     Another difference is that the personal income tax burden
     can vary considerably from year to year
     thanks to changes in personal circumstances,
     so the W-2 does not use a fixed formula
     to determine how much to withhold.
     Instead, I — as my S-corporation's employee — fill out a W-4,
     a form that lets me set my income tax withholding
     at whichever level I wish.
    </p>
    <p>
     But when tax day finally comes and everything is tallied up,
     then — as we shall see below — 401(k) investment contributions are
     completely hidden from the federal income tax calculations.
     Only the value of W-2 box 1 — my $35,000 wages in this example —
     will be copied to Form 1040 as actual income
     on which federal income taxes are computed.
    </p>
   </td>
  </tr>

  <tr>
   <th colspan=4>
    Form 941 Employer’s QUARTERLY Federal Tax Return<br>
   </th>
  </tr>
  <tr>
   <td colspan=4 width="100%">
    <p>
     This form starts off with deceptive simplicity:
     lines 2, 5a column 1, and 5c column 1
     are respectively the sums of all employee W-2 boxes 1, 3, and 5.
     But when I first reached column 2 of lines 5a and 5c,
     I stopped short: while I had been told that there was an
     “employee half” and “employer half”
     to both the Social Security and Medicare taxes,
     here on Form 941 the two halves of each tax are lumped together
     into a single sum with no indication that the monies due
     are pulled from two very different places
     in my S-Corporation's accounting.
    </p>
    <p>
     The solution to the puzzle is that the “other half”
     of the Social Security and Medicare taxes —
     the half that I do <i>not</i> take directly
     from my own paycheck per W-2 —
     become one of the “Other deductions” shown above for Form 1120S.
     More specifically, they are part of the total
     on line 12, “Taxes and licenses”, of that form.
     So the burden of paying the totals on 941 falls like this:
    </p>
   </td>
  </tr>
  <tr>
   <td colspan=1 width="25%" class="dotted"></td>
   <td colspan=1 width="35%" class="foo">
    $35,000<br>Wages (Box 1)
   </td>
   <td colspan=1 width="15%" class="dotted"></td>
   <td colspan=1 width="25%" class="foo">
    $25,000<br>Other Deductions<br>(lines 8–19)
   </td>
  </tr>
  <tr>
   <td colspan=1 width="25%"></td>
   <td colspan=1 width="35%" class="tax">
    Pays:<br>
    $50,000 × 6.20%<br>
    $50,000 × 1.45%<br>
    Estimated income taxes
   </td>
   <td colspan=1 width="15%"></td>
   <td colspan=1 width="25%" class="tax">
    Pays:<br>
    $50,000 × 6.20%<br>
    $50,000 × 1.45%
   </td>
  </tr>
  <tr>
   <td colspan=4 width="100%">
    <p>
     But on Form 941 the entire amounts that my business is depositing
     into the Social Security and Medicare funds
     are shown in single boxes,
     and so the percentages shown are 12.4% and 2.9%.
    </p>
   </td>
  </tr>

  <tr>
   <th colspan=4>
    Form 1040<br>U.S. Individual Income Tax Return
   </th>
  </tr>
  <tr>
   <td colspan=1 width="25%" class="foo">
    $25,000<br>Ordinary Business Income<br>(line 17 and Schedule E)
   </td>
   <td colspan=1 width="35%" class="foo">
    $35,000<br>Salary<br>(line 7)
   </td>
   <td colspan=1 width="15%" class="dotted">
   </td>
   <td colspan=1 width="25%" class="dotted">
   </td>
  </tr>
  <tr>
   <td colspan=4 width="100%">
    <p>
     Finally we reach Form 1040.
     Appropriately enough for an income tax form,
     neither pre-tax contributions to my 401(k)
     nor the costs of running my business show up on this form:
     instead, all I see is income!
     Included are both the wages that I have received as an employee,
     and the income that my S-corporation has earned
     over and above my salary.
    </p>
    <p>
     I must always be careful to remember that the <i>entirety</i>
     of my S-corporation's “ordinary business income” income
     appears immediately on that year's 1040 line 17,
     regardless of how much of that income
     I keep in my S-corporation's bank account as assets
     and how much I remove to my personal bank account
     as a distribution.
    </p>
   </td>
  </tr>

 </table>

The Mechanics of my Ledger
--------------------------

Three techniques help me manage the ``ledger.dat`` file
where my business checking account and credit card transactions
get assigned to income and expense categories through the magic
of double-entry bookkeeping.
Again, see the `Ledger documentation <http://www.ledger-cli.org/>`_
for background in how such files work
and are used to generate reports.

First, I do “tax-driven accounting” in the same spirit
as a computer programmer might do “test-driven development”:
the structure of my ``ledger.dat`` is designed from the ground up
to make it easy to fill out my tax forms.
I switched to this approach when, at tax time one year,
I found that it took hours to parcel out all of my business expenses
into the official expense categories listed on Form 1120S.
My expense categories looked like this::

    # Before: categories with no obvious relationship
    # to the tax forms that they will be driving.

    Expenses:Consultant:Jen Smith
    Expenses:Payroll
    Expenses:State corporation fees
    Expenses:Travel:Airport parking

So I re-worked them so that every expense
includes in its name the line number on which it should be tallied
when I sit down at year's end to fill out my 1120S::

    # Much better: expenses have been pre-labelled
    # with the categories that the 1120S needs.

    Expenses: 7:Payroll
    Expenses:12:State corporation fees
    Expenses:19:Consultant:Jen Smith
    Expenses:19:Travel:Airport parking

This added only three characters to the name of most categories,
yet completely transformed the process of filling out the 1120S —
cutting the time to only a few minutes!
It feels like the Agile technique
of writing documentation and deployment scripts
as a system is written,
instead of leaving everything for the project's end.

Note that I only added the line *number* to each expense name,
not the line *title,*
because it would look rather silly to have expenses like::

    # But including line *titles* is silly!

    Expenses: 9 Repairs and maintenance:Repairs
    Expenses: 9 Repairs and maintenance:Maintenance

The second technique was to automate the halving
of meals and entertainment expenses,
which — cruelly — only count half against business expenses
when I travel or pay for a customer's meal.
This would normally lead to verbose ledger entries like::

    # Verbose, repetitive

    2012/10/6 The Gourmet Goat
        Expenses:19:Meals and entertainment       $27.05
        Nondeductable:19:Meals and entertainment  $27.05
        Liabilities:Credit card

Not only would such entries be repetitive,
but I could easily forget to halve a particular meal.
So I have automated the process with the following rule::

    # Cut meals and entertainment in half automatically

    = "Meals and entertainment"
        $account                              -0.5
        Nondeductable:Meals and entertainment  0.5

The total of the year's resulting “Nondeductable” category
winds up on Form 1120S line 16c and on subsequent lines that include
that line, like line 5 of Schedule M-2.

Third and finally,
I use a series of virtual accounts
beneath a top-level ``Form`` account
to determine what obligations come into being
when I promise myself a month's salary,
and then to make sure that I discharge those obligations.
I keep the Ledger file here:

:download:`forms.dat <forms.dat>`

I can use it with my main ledger
by putting it first on the command line when asking for a balance::

    ledger -f forms.dat -f obligations.dat -f ledger.dat -p 2012 balance

Its actual documentation is in its comments,
but the main idea is that each month I create a new “obligation”
entry in the ``obligations.dat`` file specifying my monthly salary
next to the “free variables” on Form W-2,
such as how much I am withholding for federal and state taxes.
In return, :download:`forms.dat <forms.dat>` computes the fixed
quantities that also appear on the W-2 —
namely, the Social Security and Medicare taxes —
and creates virtual ``Forms:…`` accounts
giving both the totals to be filled in
to each line of Form 941 and Form W-2,
and also my obligation to pay the remaining balance
as my end-of-month paycheck.

As I then send myself a paycheck and submit my 941 form,
these obligations are then dispelled
until finally each form shows a zero balance
and all is right with the world.

Choosing a Salary Level
-----------------------

It takes me only a quick re-reading of the above diagram
to remember why the structure of an S-corporation
dis-incentivizes large salaries.
The only fixed quantities in the whole diagram
are the corporation's “Total Income” —
the size of the whole pie, so to speak —
and the block of 1120S “Other deductions” expenses
that were necessary to operate the business.
But the difference between those two quantities
can be split among my 401(k), my salary, and my distributions
with rather impressive latitude.
There are regulatory limits on 401(k) contributions, of course,
as well as the practical limit
that the remaining income must support my lifestyle.

The prevailing theory as to how much salary one should draw
seems to be “as little as possible” to minimize the Social Security
and Medicare burden on both the personal and business taxes.
This leads business owners to accumulate cherry-picked job listings
that justify a small salary for their particular skills and niche.

To temper this typical approach,
I like to start at first principles:
why are investments taxed at a different rate than wages
in the first place, instead of being taxed the same?
Because of a desire to incentivize investment.
An investment is a risk, and to make those risks attractive
policymakers set lower tax rates
on earnings like long-term capital gains.

In the case of my S-corporation,
the freedom that it gives me to divide my schedule shrewdly
between the customers that most need my expertise this month
also introduces considerable risk —
that, after a few busy months, there might come a moment
when *no* customers need me and no immediate income is available
to pay my salary at month's end.

And so, when setting my salary,
I look at my business income to date
and try to determine how much of that income is really at risk —
how much income could really evaporate from the next few months
if things went badly for my most important customers.
The level of income that seems secure even through a lean quarter
— not a single lean month that stands as an outlier,
but several lean months in a row —
should be my salary:
because it is that portion of my income
which does not stand at considerable risk,
and should not enjoy special tax treatment.

But the income above and beyond that of a usual quarter
is exceptional, cannot be counted upon,
and is exactly the sort of boon for which
I have taken the risk of running my own business.
And because it is the reward for risks taken,
I am happy to leave it as S-corporation income
instead of taking it as salary.
