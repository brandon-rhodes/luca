'''The Form class and its supporting materials.'''

import json


class Form(object):
    '''A class whose instances remember the order in which attrs are set.'''

    def __init__(self):
        self._clear()
        self._outputs = []
        self._outputset = set()
        self._mode = 'input'

    def _clear(self):
        self._inputs = []
        self._inputset = set()

    def _switch_from_input_to_output(self):
        self._mode = 'output'

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
    outer = json.loads(text, object_pairs_hook=form_from_pairs)
    return outer.inputs

def form_from_pairs(pairs):
    f = Form()
    for name, value in pairs:
        setattr(f, name, value)
    return f
