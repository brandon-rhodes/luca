'''Tests of the important Form class.'''

from unittest import TestCase
from luca.forms.form import Form


class FormTests(TestCase):

    def test_instantiation(self):
        Form()

    def test_attributes_remember_their_values(self):
        f = Form()
        f.y = 3
        f.x = 1
        f.z = 2
        assert f.y == 3
        assert f.x == 1
        assert f.z == 2

    def test_attributes_remember_their_order(self):
        f = Form()
        f.y = 3
        f.x = 1
        f.switch_from_input_to_output()
        f.z = 2
        assert f._inputs == ['y', 'x']
        assert f._outputs == ['z']


json1 = '''{
 "inputs": {
  "form": "rental_income",
  "ssn": "123-45-6789",
  "name": "Lynn Smith",
  "A": {
   "address": "123 Main St, Ohio",
   "rents": "900.00",
   "expenses": "100.00",
  },
  "B": {
   "address": "456 Elm St, Georgia",
   "rents": "800.00",
   "expenses": "230.00",
  }
 },
 "outputs": {
  "A": {
   "profit": "800.00",
   "tax": "80.00"
  },
  "B": {
   "profit": "570.00"
   "tax": "57.00"
  },
  "total_rents": "1700.00",
  "total_expenses": "330.00",
  "total_tax": "137.00"
 }
}
'''
