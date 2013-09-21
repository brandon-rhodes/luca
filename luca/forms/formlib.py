"""The Form class and its supporting materials."""

import json
import re
from collections import OrderedDict as odict
from decimal import Decimal


class Form(object):
    """A class whose instances remember the order in which attrs are set."""

    def __init__(self):
        self._inputs = []
        self._inputset = set()
        self._outputs = []
        self._outputset = set()
        self._mode = 'input'

    def __repr__(self):
        return u'<Form {}>'.format(' '.join(
                '{}={!r}'.format(name, value) for name, value
                in sorted(self.__dict__.items()) if not name.startswith('_')
                ))

    def __getitem__(self, name):
        """Dynamic attribute lookup, to avoid setattr() and getattr().

        >>> f = Form()
        >>> f.line6 = 100
        >>> f['line6']
        100
        >>> f['line', 6]
        100

        """
        if not isinstance(name, str):
            name = ''.join(str(item) for item in name)
        return getattr(self, name)

    def __setitem__(self, name, value):
        """Dynamic attribute setting."""
        if not isinstance(name, str):
            name = ''.join(str(item) for item in name)
        return setattr(self, name, value)

    def _enter_default_mode(self):
        """Switch this form, and any child forms, to default mode.

        In default mode, an assignment statement only sets an attribute
        if it does not already exist on the form.

        """
        self._mode = 'default'
        for value in self.__dict__.values():
            if isinstance(value, Form):
                value._enter_default_mode()
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Form):
                        item._enter_default_mode()

    def _enter_output_mode(self):
        """Switch this form and all child forms to output mode.

        This never needs to be called from tax form logic, because Luca
        calls this method automatically after a tax form has been read
        in from persistent storage, but before the tax form's compute()
        function is invoked so that computed values become output.

        """
        self._mode = 'output'
        for value in self.__dict__.values():
            if isinstance(value, Form):
                value._enter_output_mode()
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Form):
                        item._enter_output_mode()

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if name in self._inputset:
                if self._mode == 'default':
                    return
                raise TypeError('an input attribute like %s can only be'
                                ' set once' % name)
            if self._mode == 'input':
                self._inputs.append(name)
                self._inputset.add(name)
            elif self._mode == 'output':
                if name not in self._outputset:
                    self._outputs.append(name)
                    self._outputset.add(name)
        super(Form, self).__setattr__(name, value)


def load_json(text):
    """Parse JSON in the unicode string `text` and return a Form."""
    outer = json.loads(text, object_pairs_hook=_form_from_pairs)
    return outer.inputs

_decimal_re = re.compile(ur'^-?[\d,]+\.[\d,]+$')

def _form_from_pairs(pairs):
    f = Form()
    for name, value in pairs:
        setattr(f, name, _convert(value))
    return f

def _convert(value):
    if isinstance(value, unicode) and _decimal_re.match(value):
        return Decimal(value.replace(u',', u''))
    elif isinstance(value, list):
        return [_convert(item) for item in value]
    return value


def dump_json(form):
    """Render the `form` as attractively formatted JSON."""
    j = json.dumps(form, ensure_ascii=False, indent=1,
                   separators=(',', ': '), default=_encode)
    return j + '\n'

def _encode(value):
    if isinstance(value, Decimal):
        return '{:,}'.format(value)
    elif isinstance(value, Form):
        form = value
        inputs = _gather_inputs(form)
        outputs = _gather_outputs(form)
        return odict([('inputs', inputs), ('outputs', outputs)])

def _gather_inputs(form):
    d = odict()
    for name in form._inputs:
        value = getattr(form, name)
        if isinstance(value, Decimal):
            value = '{:,}'.format(value)
        elif isinstance(value, Form):
            value = _gather_inputs(value)
        elif isinstance(value, list) and any(
              isinstance(item, Form) for item in value
              ):
            value = [_gather_inputs(subform) for subform in value]
        d[name] = value
    return d

def _gather_outputs(form):
    d = odict()
    for name in form._inputs:
        value = getattr(form, name)
        if isinstance(value, Form) and _has_outputs(value):
            value = _gather_outputs(value)
            d[name] = value
        elif isinstance(value, list) and any(
              isinstance(item, Form) for item in value
              ):
            value = [_gather_outputs(item) for item in value]
            if any(value):
                d[name] = value
    for name in form._outputs:
        value = getattr(form, name)
        if isinstance(value, Decimal):
            value = '{:,}'.format(value)
        elif isinstance(value, Form):
            value = _gather_outputs(value)
        elif isinstance(value, list):
            value = [_gather_outputs(item) for item in value]
        d[name] = value
    return d

def _has_outputs(form):
    if form._outputs:
        return True
    for value in form.__dict__.values():
        if isinstance(value, Form) and _has_outputs(value):
            return True
    return False
