
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
   to remind myself of how to use my ``luca`` command,
   which I maintain for my own personal use.
   That is why this documentation is written solely in the first person:
   it is simply my own record of how I use the tool,
   and does not provide any accounting or legal advice
   about how other people ought to be filling out their own tax forms.

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
separate from the idea of a particular instance of that form
that I have submitted to the government.
So in Luca I have used separate terms for these ideas:

*Form*
    An idea like “Form 1040, U.S. Individual Income Tax Return,”
    which exists over very many years in different formats and copies
    and with rules that change year to year.

*Filing*
    A form as filled out and submitted on a particular date,
    like “the Form 1040 for the 2011 tax year
    that I submitted in April of 2012.”
    It has particular values filled in for each line,
    and has been computed using exactly the rules
    for its particular year.

Each JSON tax form file that Luca deals with,
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
  the ``output`` section is entirely rebuild every time
  from calculations done on the ``input`` information.

Note that dollar amounts in the file
are always stored as strings containing decimal numbers like ``"1.23"``
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
and wanting to see the results are:

1. Build an initial blank form listing the default value of each field.
   I can choose whatever filename I would like, and I typically
   start each name with the year and (if applicable) quarter
   so that they sort by date when I list the directory. ::

    luca defaults us.f941 > 2012-Q1-f941.json

2. I then edit the form,
   removing all of the default values that I am happy with —
   since omitting them is another way to get their default value —
   and filling in only the values that I actually need to specify. ::

    emacs 2012-Q1-f941.json    # my editor of choice

3. Once the inputs have been filled in,
   I can ask Luca to compute all of the output fields
   and to render the result as a PDF file.
   Luca creates the ``out/`` directory for me automatically
   if it does not already exist in the current directory. ::

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

Nomenclature
------------


