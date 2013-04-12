"""The Form class and its supporting materials."""

import json
import re
from collections import OrderedDict as odict
from decimal import Decimal

class Form(object):
    """A class whose instances remember the order in which attrs are set."""

    def __init__(self):
        self._clear()
        self._outputs = []
        self._outputset = set()
        self._mode = 'input'

    def _clear(self):
        """Forget the names of the inputs that have been set so far.

        This has two consequences.  First, all attributes already set
        may be set one more time without raising an exception.  Second,
        the attributes set so far will not appear when the form is
        rendered as JSON unless they are set a second time.

        This is useful if a tax form wants to set up default values
        (like a zero for each of the input amounts) that can then be
        overwritten by the user's actual form values, but that will not
        clutter up the "input" section when we re-save the form as JSON.

        """
        self._inputs = []
        self._inputset = set()

    def _switch_from_input_to_output(self):
        """Switch this form and all child forms to output mode."""
        self._mode = 'output'
        for value in self.__dict__.values():
            if isinstance(value, Form):
                value._switch_from_input_to_output()

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if name in self._inputset:
                raise TypeError('an input attribute like %s can only be'
                                ' set once' % name)
            if self._mode == 'input':
                self._inputs.append(name)
                self._inputset.add(name)
            else:
                if name not in self._outputset:
                    self._outputs.append(name)
                    self._outputset.add(name)
        super(Form, self).__setattr__(name, value)


def load_json(text):
    """Parse JSON in the unicode string `text` and return a Form."""
    outer = json.loads(text, object_pairs_hook=_form_from_pairs)
    return outer.inputs

_decimal_re = re.compile(ur'^\d+\.\d\d$')

def _form_from_pairs(pairs):
    f = Form()
    for name, value in pairs:
        if isinstance(value, unicode) and _decimal_re.match(value):
            value = Decimal(value)
        setattr(f, name, value)
    return f

def dump_json(form):
    """Render the `form` as attractively formatted JSON."""
    j = json.dumps(form, ensure_ascii=False, indent=1,
                   separators=(',', ': '), default=_encode_form)
    return j + '\n'

def _encode_form(form):
    inputs = _gather_inputs(form)
    outputs = _gather_outputs(form)
    return odict([('inputs', inputs), ('outputs', outputs)])

def _gather_inputs(form):
    d = odict()
    for name in form._inputs:
        value = getattr(form, name)
        if isinstance(value, Form):
            value = _gather_inputs(value)
        elif isinstance(value, Decimal):
            value = str(value)
        d[name] = value
    return d

def _gather_outputs(form):
    d = odict()
    for name in form._inputs:
        value = getattr(form, name)
        if isinstance(value, Form) and value._outputs:
            value = _gather_outputs(value)
            d[name] = value
    for name in form._outputs:
        value = getattr(form, name)
        if isinstance(value, Form):
            value = _gather_inputs(value)
        elif isinstance(value, Decimal):
            value = str(value)
        d[name] = value
    return d
