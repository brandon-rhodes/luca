
Accounting For My S-Corporation
===============================

The Luca tool does not actually compute my taxes.
I discovered that an already existing tool,
the `Ledger command-line accounting system <http://www.ledger-cli.org/>`,
works great for tallying up the tax consequences of my business.
It works so well that it has completely defeated my usual instinct
to re-implement everything in Python!

So this documentation chapter really has nothing to do with Luca,
which only becomes involved when I am ready to submit tax forms.
Instead, these are my notes about setting up an annual ``ledger.dat``
file for my S-corporation so that I can easily determine my taxes.

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
  #taxtable .foo {
   border: 2px solid #d7a14d; background-color: #f9ebd4;
   vertical-align: top; text-align: center; font-weight: bold;
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
     as customers buy its products or pay its invoices for services.
     Here, I imagine a consultancy whose proceeds totalled $100,000.
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
   <th colspan=4>
    Form 1040<br>U.S. Individual Income Tax Return
   </th>
  </tr>
  <tr>
   <td colspan=1 width="25%" class="foo">
    $25,000<br>Supplemental Income<br>(line 17)
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
     Your business receives payments and fees from your customers
     over the calendar year,
     which when added together make up your Total Income.
    </p>
   </td>
  </tr>

 </table>

