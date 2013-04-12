'''The Form class and its supporting materials.'''

class Form(object):
    '''A class whose instances remember the order in which attrs are set.'''

    def __init__(self):
        self._inputs = []
        self._outputs = []
        self._names = self._inputs

    def _clear(self):
        del self._inputs[:]

    def _switch_from_input_to_output(self):
        self._names = self._outputs

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if name in self._inputs:
                raise TypeError('an input attribute like %s can only be'
                                ' set once' % name)
            if name not in self._names:
                self._names.append(name)
        super(Form, self).__setattr__(name, value)
