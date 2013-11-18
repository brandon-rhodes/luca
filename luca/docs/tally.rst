
Tallying
========

If Luca knows how to parse your bank statements,
then all you have to do is write a quick YAML tree of rules,
and Luca will categorize your transactions
and tally all of your income and expenses!
The currently supported statement formats are:

* Delta Community Credit Union checking
* Delta Community Credit Union Visa Business

If your bank statements are **not yet supported,**
please **let us know** the format
so that we can add a module to the ``luca.importer`` sub-package.

Quick reference to rules
------------------------

| ``2013`` — Match a particular year.
| ``9/16`` — Match a month and day.
| ``9/16-10/5`` — Inclusive range of dates.
| ``/regex/`` — Description contains a regular expression.
| ``~/regex/`` — Description does not contain a regular expression.

Any other string is considered a category.
You might start out writing rules by putting categories
at the bottom of your YAML hierarchy:

.. highlight:: yaml

::

    - /AERLING/:
      - Travel.Airfare
    - /DELTA AIR/:
      - Travel.Airfare
    - /DJANGOCON/:
      - Travel.Conferences
    - /PYCON/:
      - Travel.Conferences

But feel free to pivot category names
up into the middle of the hierarchy instead.
When a transaction matches a leaf node successfully,
it receives the nearest ancestor category:

::

    - Travel.Airfare:
      - /AERLING/
      - /DELTA AIR/
    - Travel.Conferences:
      - /DJANGOCON/
      - /PYCON/

Be sure to include a colon ``:`` after a rule or category
that is followed by further rules or categories.
If you forget, then YAML will not be kind to you:

::

    # Whoops! The terminal colon is missing.

    - Travel.Airfare
      - /DELTA AIR/

    # YAML parses this as simply a category named:

    - "Travel.Airfare - /DELTA AIR/"

A transaction is tested against the rules in the YAML file
starting at the top and proceeding downward.
Only by matching a parent rule can a transaction
proceed to be tested against its children.
Once a transaction survives all the way out to a leaf node —
a node that the transaction matches, that has no further children —
then a match has been made,
a category is assigned,
and no further rules are processed for that transaction.

Invoking tally
--------------

If you supply PDF files to Luca,
be sure that you have the ``pdftotext`` command installed on your system
(Ubuntu keeps it in the ``poppler-utils`` package)
so that Luca can turn them into plain text itself:

.. code-block:: bash

    $ luca tally rules.yaml statements/*.pdf

Otherwise, you can render the PDFs to plain text manually
before passing the text files to Luca:

.. code-block:: bash

    $ pdftotext -layout new.pdf > statements/2013-03-checking.txt
    $ luca tally rules.yaml statements/*.txt

If you are going to version control your bank statements
alongside your rules files,
then you might find the text versions more convenient anyway.
In the last section of this document
you will find an example ``Makefile``
if you want to automate this process.

Two sample statements
---------------------

The following sections walk you through building a sample rules file.
To try out the examples yourself,
simply download these two sample bank statements:

* :download:`statement-bank.txt <statement-bank.txt>`
* :download:`statement-visa.txt <statement-visa.txt>`

These examples have been pared down to the minimum necessary text
for Luca to recognize and parse
this particular bank’s checking and Visa statements.

Starting your rules file
------------------------

You will generally begin a rules file
with a root selector, to narrow Luca’s attention
to the specific transactions for which that file is designed.
To keep things simple I maintain a separate rules file for each year;
it would be difficult to keep a single rules file
working against all previous years
while writing new rules for the current year.
We might start a 2013 rules file by typing this:

.. literalinclude:: rules0t.yaml
   :language: yaml

This selects all transactions for the calendar year 2013
and gives them the category ``Unknown``
so that we can take a look at them
and start making decisions about how to divide them up.
Running a rules file against a set of bank statements is easy:

.. code-block:: bash

    $ luca tally -t rules.yaml statements/*.txt

Always use the ``-t`` option while working on your rules:
it asks Luca to display, beneath each category,
its full list of matching transactions
so that you can see whether your transactions
are winding up in the right categories.
Its output when run with these initial rules is quite simple:

.. highlight:: none

.. raw:: html
   :file: output0t.html

Success — we can now see the transactions that need categorization!
It is time to start creating specific rules.

Designing rules
---------------

The first step is usually to isolate transactions
that do not represent real income or expenses,
but that instead just represent money moving between our own accounts.
I create a category named ``Zero`` for such transactions
since transactions that move money should sum to exactly zero.

In this case, a single $300 payment on 10/1
is showing up twice:
as both a deduction from our checking account
and also a payment toward our Visa credit card account.
To remove these from the ``Unknown`` category,
we simply need to craft a pair of regular expressions to match:

.. literalinclude:: rules1t.yaml
   :language: yaml

.. raw:: html
   :file: output1t.html

Since accounts are alphabetized in the output,
our new ``Zero`` account appears at the bottom.
It successfully balances to zero!
We have taken what was really a single transaction
reported from two different points of view,
and correctly tallied
that moving the money from one account to the other
made us neither richer nor poorer.

What should we tackle next?
The sources of income stand out rather obviously in green,
since they are the only remaining positive amounts.

The income is of two very different kinds —
one is a client check that has resulted from a sale,
while the other two are interest payments from the credit union —
so we will create an ``Income`` account
with two separate sub-accounts named ``Interest`` and ``Sales``.
Luca understands the idea of a hierarchy of accounts,
if we separate parent from child accounts with a period:

.. literalinclude:: rules2t.yaml
   :language: yaml

.. raw:: html
   :file: output2t.html

Note that Luca has computed a sub-total
both for the child accounts ``Interest`` and ``Sales``,
while also including those sub-totals
in the final tally for ``Income`` itself.

At this point we face our expenses.
I start by addressing expenses
that need only one or two regular expressions,
and then tackle expenses that are more complicated.

When accounting for my S-Corporation,
I go ahead and name the sub-categories right beneath ``Expenses``
by whichever line of Form 1120S a particular expense belongs on.
This makes it easy to transfer the totals to Form 1120S later.

.. literalinclude:: rules3t.yaml
   :language: yaml

.. raw:: html
   :file: output3t.html

Finally, we reach a point
where all remaining expenses belong to a single category —
in this case, all ``Unknown`` transactions
are restaurant visits during conferences or business travel.

Instead of trying to write a regular expression for every single one,
you can simply rewrite your final rule
so that it puts all remaining transactions
in the ``Meals`` category instead of calling them ``Unknown``.
So our rules file winds up looking like:

.. literalinclude:: rules4.yaml
   :language: yaml

You might worry that this will mis-categorize future transactions
as they arrive with new statements from my credit union.
But since I always version control my ``tally`` ``-t`` output
in addition to the rules files themselves,
a quick ``diff`` in my version control system
will make it easy what new transactions have arrived each month
so that I can make sure that they land in the right places.

Running a final report
----------------------

When you are happy with where your transactions are landing,
you can take a deep breath, remove ``-t`` from your command line,
and receive your reward:
succinct income and expense tallies
driven directly by your bank statements!

.. raw:: html
   :file: output4.html

Remember that the total for each top-level account
will include both the sub-totals from the sub-accounts
indented below it,
as well as for any transactions that you assigned directly to it.

Automation and version control
------------------------------

A simple ``make`` will be enough to run your balances
if you build a ``Makefile`` that contains rules like:

.. code-block:: make

    tally-2013.txt: rules-2013.yaml statements/*.txt
            luca tally -t $+ > $@

So that you can see exactly which transactions are new
when you add new bank statements and re-run luca,
put everything under version control —
both your input rules, and the resulting output file.

.. code-block:: bash

    git add Makefile
    git add statements/*.txt
    git add rules-2013.yaml
    git add tally-2013.txt
    git commit

Given these files under version control,
here is my rough algorithm each month
for getting new information into Luca
and making sure that I like how my rules have classified
the new transactions:

.. code-block:: bash

    # As each new statement arrives, I always
    # convert it to *.txt manually to avoid
    # putting huge PDFs under version control:

    pdftotext -layout ~/Downloads/stmt.pdf > statements/2013-11-checking.txt

    # Prepare to enroll it in version control:

    git add statements/*.txt

    # To check whether your rules classify the
    # new transactions appropriately:

    make
    git diff

    # Edit your rules until you like where
    # each transaction is landing, then:

    git commit .

Of course,
if you simply wait until the end of the year
to write your ``rules.yaml`` and do all of your accounting
then you will not need these precautions.
No new bank statements will be showing up later
to scatter fresh transactions across your categories!
Instead, you will write the rules once,
already knowing every transactions
that they have to successfully classify.
