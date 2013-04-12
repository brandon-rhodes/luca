'''The Form class and its supporting materials.'''

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
