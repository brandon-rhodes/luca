from unittest import TestCase
from luca.kit import cents
from luca.forms.form import Form, load_json


class FormTests(TestCase):

    def test_instantiation(self):
        Form()

    def test_attributes_remember_their_values(self):
        f = Form()
        f.y = 3
        f.x = 1
        f.z = 2
        assert f.x == 1
        assert f.y == 3
        assert f.z == 2

    def test_attributes_remember_their_order(self):
        f = Form()
        f.y = 3
        f.x = 1
        f._switch_from_input_to_output()
        f.z = 2
        assert f._inputs == ['y', 'x']
        assert f._outputs == ['z']

    def test_attributes_are_only_listed_once(self):
        f = Form()
        f.y = 3
        f.x = 1
        f._switch_from_input_to_output()
        f.z = 2
        f.w = 4
        f.w = 8
        f.z = 1
        assert f._inputs == ['y', 'x']
        assert f._outputs == ['z', 'w']

    def test_input_attributes_cannot_be_set_twice(self):
        f = Form()
        f.y = 3
        f.x = 1
        with self.assertRaises(TypeError):
            f.y = 5

    def test_input_attributes_cannot_become_outputs(self):
        f = Form()
        f.y = 3
        f.x = 1
        f._switch_from_input_to_output()
        f.z = 2
        with self.assertRaises(TypeError):
            f.x = 4

    def test_input_attribute_list_can_be_cleared(self):
        f = Form()
        f.y = 0
        f.x = 0
        assert f._inputs == ['y', 'x']
        f._clear()
        assert f._inputs == []
        f.x = 5
        f.y = 7
        assert f._inputs == ['x', 'y']
        with self.assertRaises(TypeError):
            f.x = 4

    def test_building_from_json_reads_inputs(self):
        for json in json1, json2:
            f = load_json(json)
            assert f._inputs == ['form', 'ssn', 'name', 'A', 'B']
            assert f.form == 'rental_income'
            assert f.ssn == '123-45-6789'
            assert f.name == 'Lynn Smith'
            self.assertIsInstance(f.A, Form)
            assert f.A.address == '123 Main St, Ohio'
            self.assertIsInstance(f.B, Form)

    def test_building_from_json_discards_old_outputs(self):
        for json in json1, json2:
            f = load_json(json)
            assert f._outputs == []
            with self.assertRaises(AttributeError):
                f.A.profit
            with self.assertRaises(AttributeError):
                f.total_rents


json1 = u'''{
 "inputs": {
  "form": "rental_income",
  "ssn": "123-45-6789",
  "name": "Lynn Smith",
  "A": {
   "address": "123 Main St, Ohio",
   "rents": "900.00",
   "expenses": "100.00"
  },
  "B": {
   "address": "456 Elm St, Georgia",
   "rents": "800.00",
   "expenses": "230.00"
  }
 }
}
'''

json2 = json1[:-3] + u''',
 "outputs": {
  "A": {
   "profit": "800.00",
   "tax": "80.00"
  },
  "B": {
   "profit": "570.00",
   "tax": "57.00"
  },
  "total_rents": "1700.00",
  "total_expenses": "330.00",
  "total_profit": "1370.00",
  "total_tax": "137.00"
 }
}
'''

def process_form(f):
    subs = (f.A, f.B)
    for sub in subs:
        sub.profit = sub.rents - sub.expenses
        sub.tax = cents(sub.profit / 10)
    f.total_rents = sum(sub.rents for sub in subs)
    f.total_expenses = sum(sub.expenses for sub in subs)
    f.total_profit = sum(sub.profit for sub in subs)
    f.total_tax = sum(sub.tax for sub in subs)
