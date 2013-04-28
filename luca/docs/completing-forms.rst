
Completing Tax Forms
====================

Thanks to Luca,
I am now able fill out tax forms by building simple JSON files
that I can version-control as a compact yet human-readable
record of exactly what I have written on every form
that I have submitted to the government.
Whenever I need to produce a physical copy of a form,
Luca can read my JSON and produce a PDF suitable for printing.

.. note::

   I have written this Luca documentation
   to remind myself how to use my ``luca`` command,
   which I maintain for my own personal use.
   That is why this documentation is written in the first person:
   it is simply my own record of how I use the tool.
   It is in no way intended as advice —
   whether technical, financial, or legal —
   about how *other* people ought to be filling out their own tax forms.

The Idea of a “Filing”
----------------------

Most tax forms are periodic.
They need to be filled out over and over again,
every quarter or every year,
so that over my career and lifetime
I will wind up submitting many separate copies of each form.
Furthermore, forms evolve over the years
so that the processing logic behind them
needs to adjust to varying line numbers and different rules
depending on the year in which a form was filed.

For these reasons it is important that I keep the general idea of a form
separate from the idea of a particular instance of a form
that I have submitted to the government.
So in Luca I have used separate terms for these ideas:

*Form*
    For example, “Form 1040, U.S. Individual Income Tax Return,”
    which exists over many years in different formats and copies,
    and that has rules that change year to year.

*Filing*
    A form as filled out and submitted on a particular date,
    like “the Form 1040 for the 2011 tax year
    that I submitted in April of 2012.”
    It has particular values filled in for each line,
    and has been computed using exactly the rules
    for its particular year.

Each tax form JSON file that Luca deals with,
therefore, is not really a *form* but more specifically a *filing.*

Inputs and Outputs
------------------

The JSON for a filing looks like this:

.. literalinclude:: ../samples/f941.json
   :language: js

Luca divides a tax filing quite strictly
between input fields and output fields,
which are stored in their own sections of the filing's JSON.
Strictly speaking, a tax filing is a JSON object
that defines only two names, ``input`` and ``output``,
that together contain all of the information from the filing.

* Luca promises to never, ever change
  the content of the ``input`` object
  (though it does get freshly reformatted
  each time the form is processed).
  No matter how many times I run the Luca ``complete`` command
  on a particular filing,
  the input section will remain the same.

* In contrast, the ``output`` section belongs entirely to Luca.
  I cannot assume that any information there
  will survive a re-run of the ``complete`` command;
  the ``output`` section is entirely rebuilt, every time,
  by re-running the form's calculations on the ``input`` information.

Note that dollar amounts in the JSON file are always represented
as strings containing decimal numbers like ``"1.23"``
instead of being stored as bare JSON floating point numbers like ``1.23``
without quotation marks around them.
This avoids the rounding errors and imprecision
that take place when the machine attempts to store
decimal fractions as base-2 floating point.
Luca automatically detects strings that look like numbers
with a decimal point, and converts them to safe Python ``Decimal``
instances.

Workflow
--------

My typical workflow when filling out a tax form
and wanting to see the result is:

1. I ask Luca to build an initial, blank version of the form,
   that lists the default value of each field.
   I can choose whatever filename I want.
   I typically start each filename with the year
   and (if applicable) quarter
   so that they sort by date when I list the directory. ::

    luca defaults us.f941 > 2012-Q1-f941.json

2. I then edit the form,
   removing all of the default values that I am happy with —
   since Luca will assign each omitted field its default value —
   and filling in only the values that I actually need to specify. ::

    emacs 2012-Q1-f941.json    # my editor of choice

3. Once the inputs have been filled in,
   I can ask Luca to compute all of the output fields
   and to render the result as a PDF file.
   Luca creates an ``out/`` directory for me automatically
   if one does not already exist in the current directory,
   and places there a PDF with the same filename as my JSON file. ::

    luca complete 2012-Q1-f941.json
    view out/2012-Q1-f941.pdf

4. Once I have corrected any typos in my inputs
   and am happy with how the form looks,
   I can commit it to version control.
   This is especially important
   so that I have a complete history
   of exactly what I submitted on each form,
   in case I ever need to send in an amended return in the future. ::

    git ci -m 'Filled out 941 for Q1' 2012-Q1-f941.json

When repeated over months and years,
this procedure results in a version controlled history
of all of the tax forms that I have submitted to the government.
Furthermore, it automates the process of doing the additions
and subtractions required on each particular tax form
and makes it less likely that there will be errors.

If I ever discover that Luca has been computing a form incorrectly —
either because of a bug,
or because of an outright misunderstanding about the tax law
that I manage to enshrine in Luca's code —
then I can quickly re-run all of my tax forms
and see immediately which ones are in need of amendment::

    luca complete *.json
    git diff

Field Names
-----------

Luca names form fields by their letter or number when possible,
instead of trying to come up with clever and meaningful names.
This makes it easy for me to visually relate the JSON data
to the actual printed form.

Semantic names were a constant temptation as I implemented
my first few tax forms, but they wind up making programming difficult:
tax form instructions always refer to “line 7”,
not “Wages, salaries, tips, etc”! ::

    # A temptation that Luca avoids:

    ⋮
    "wages_salaries_tips": "46,100.86",
    "taxable_interest": "15.40",
    "tax_exempt_interest": "9.01",
    ⋮

So Luca refers to sections and schedules
by simple names like ``A`` and ``K1``,
since these are valid identifiers in Python already.
But since numbers are not valid identifiers —
a Python program cannot use ``form.7`` in an expression —
tax form lines get the word ``line`` put in front of their names. ::

    # Luca always names fields like this instead:

    ⋮
    "line7": "46,100.86",
    "line8a": "15.40",
    "line8b": "9.01",
    ⋮

Avoiding semantic names also has the great benefit
of discouraging me from trying to proofread the tax form
by staring at the JSON file by itself.
For the line numbers to be meaningful
I generally have to open the tax form itself
in a PDF reader on the other side of my screen,
which is exactly what I should be doing —
I want Luca to be a tool that makes me read the tax forms themselves,
not a tool that pulls my attention away from the actual document
that I am legally required to fill out correctly.
