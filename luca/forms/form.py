'''The Form class and its supporting materials.'''

class Form(object):

    def __init__(self):
        self._inputs = []
        self._outputs = []
        self._names = self._inputs

    def switch_from_input_to_output(self):
        self._names = self._outputs

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            if name not in self.__dict__:
                self._names.append(name)
            elif name in self._inputs:
                raise TypeError('an input attribute like %s can only be'
                                ' set once' % name)
        super(Form, self).__setattr__(name, value)
