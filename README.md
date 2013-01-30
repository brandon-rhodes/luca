
=================================================
 Luca: accounting for the independent consultant
=================================================

As an independent consultant,
I sustain a very simple business structure:
an S-Corporation of which I am the sole employee.
In this Luca project,
I am slowly collecting commands and scripts
that help me automate the production
of business tax forms and other obligations
that my business must meet each quarter.

Luca is named after Luca Pacioli,
the Italian friend of Leonardo's who invented modern accounting.

You can install Luca by:

    git checkout https://github.com/brandon-rhodes/luca.git
    cd luca
    pip install .

Luca has several bits and pieces,
most of which are still experimental.
But there is one piece that bears mention
as something that might already prove a useful tool for others:
it can compute and print United States tax forms 940 and 941.

I intend the various features of Luca to be independent
and to be mediated by plain-text files
that can be kept in version control.
For example, I plan one day to have a module that can
read in my annual ledger and figure out what numbers
I need to put into forms 940 and 941.
If it is ever written, though, it will produce the same kind of file
that the 940 and 941 routines already take as input today:
simple plain-text JSON files that,
for the moment, I can hand-assemble
from hand-computed numbers to get my tax forms printed.

You will save each particular filing of a form
as a single JSON file,
that has an `inputs` object that you write to,
and an `outputs` object where Luca will write out the fields
that it computes from your inputs.
For example, you might start a 941 form like this:

```
{
 "inputs": {
  "form": "us.irs941",
  "ein": "00-0000000",
  "name": "My Company, Inc.",
  "address": "123 Main Street",
  "city": "Small Town",
  "state": "MA",
  "zip": "01810",
  "quarter": 4,
  "line1": 1,
  "line2": "4500.00",
  "line3": "750.00",
  "line5b1": "0.00",
  "line5e": "",
  "line16a": "X",
  "part4_no": "X",
  "sign_name": "Mister Businessman",
  "sign_title": "President",
  "sign_phone": "867-5309"
 }
}
```

You would then invoke Luca to process and print this form
by running the `luca` command like this:

    luca complete myform.json

This command will modify your JSON file in-place
to add an `outputs` section;
because this in-place modification is still fragile,
I always recommend that you check your raw JSON input file into
version control before running Luca on it!
The new stanza in the file will look something like this,
and lets you check into version control as a permanent record
the exact field values that you will be submitting
when you send in the form:

```
{
 "inputs": {
  ...
 },
 "outputs": {
  "line5a1": "4500.00",
  "line5c1": "4500.00",
  "line5a2": "468.00",
  "line5b2": "0.00",
  "line5c2": "130.50",
  "line5d": "598.50",
  "line6": "1348.50",
  "line10": "1348.50",
  "line14": "1348.50"
 }
}
```

Checking this modified JSON file into version control
is how I keep a permanent record,
without having to archive large PDFs,
of every copy of these forms that I submit to the government.

If you have downloaded the form's PDF from the IRS,
then you can ask Luca to actually fill in the printed form for you.
The following command both recomputes your form's `outputs` section
and also produces a `completed-form.pdf` with your filled-in form:

    luca complete myform.json f941.pdf

Note that the form logic is very fragile at the moment,
as it does the bare minimum needed to fill in a few
form fields correctly for my particular business.
If you try using the command yourself,
you will probably find that you need to implement a few more fields
before the form will be complete and accurate for your own
business; if so, you should find the form logic very straightforward,
and I welcome pull requests that make them more general!
