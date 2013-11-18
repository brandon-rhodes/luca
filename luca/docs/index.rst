.. Luca documentation master file, created by
   sphinx-quickstart on Sat Apr 27 13:45:48 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Luca
===============

*Do accounting with YAML, fill out tax forms with JSON!*

Luca currently supports two exciting use cases:

1. If you download your **bank statements,**
   Luca lets you build a YAML tree of **regular expressions**
   to automatically classify transactions
   and tally your income and expenses.

   (See the chapter on “Tallying” below.)

2. You can version control your **tax forms** as JSON data,
   with Luca performing all of the necessary math
   and then **rendering PDFs**
   that you can print and send the government.

   (See the other chapters listed below.)

Luca is prounounced *Lew-cha* and is named after Luca Pacioli,
the Italian friend of Leonardo da Vinci's
who invented modern accounting.

Luca is easy to install with standard Python tools::

    pip install luca

Project resources:

* `Entry on PyPI <https://pypi.python.org/pypi/luca>`_
* `Source code on GitHub <https://github.com/brandon-rhodes/luca>`_
* `Issue tracker on GitHub <https://github.com/brandon-rhodes/luca/issues>`_

Documentation
-------------

.. toctree::
   :maxdepth: 2

   tally
   completing-forms
   s-corporation
