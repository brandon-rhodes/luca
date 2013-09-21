from decimal import Decimal
from unittest import TestCase
from textwrap import dedent

from luca.kit import cents
from luca.forms.formlib import Form, load_json, dump_json


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
        f._enter_output_mode()
        f.z = 2
        assert f._inputs == ['y', 'x']
        assert f._outputs == ['z']

    def test_attributes_are_only_listed_once(self):
        f = Form()
        f.y = 3
        f.x = 1
        f._enter_output_mode()
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
        f._enter_output_mode()
        f.z = 2
        with self.assertRaises(TypeError):
            f.x = 4

    def test_attribute_assignment_is_ignored_in_default_mode(self):
        f = Form()
        f.x = 1
        f.A = Form()
        f.A.y = 2
        f._enter_default_mode()
        f.x = -1
        f.y = -2
        f.A.x = -3
        f.A.y = -4
        assert f.x == 1
        assert f.y == -2
        assert f.A.x == -3
        assert f.A.y == 2

    def test_default_attributes_disappear_from_output(self):
        f = Form()
        f.x = 1
        f._enter_default_mode()
        f.x = -1
        f.y = -2
        f._enter_output_mode()
        f.z = -3
        assert f._inputs == ['x']
        assert f._outputs == ['z']

    def test_getitem_gets_attributes(self):
        f = Form()
        f.x = 1
        f.y20 = 'Two'
        assert f['x'] == 1
        assert f['y', 20] == 'Two'

    def test_setitem_gets_attributes(self):
        f = Form()
        f['y', 20] = 'Two'
        assert f['y', 20] == 'Two'
        assert f.y20 == 'Two'

    def test_building_from_json_reads_inputs(self):
        for json in json_in, json_empty_output, json_filled_output:
            f = load_json(json)
            assert f._inputs == ['form', 'ssn', 'name', 'Part_I']
            assert f.form == 'rental_income'
            assert f.ssn == '123-45-6789'
            assert f.name == 'Lynn Smith'
            self.assertIsInstance(f.Part_I, Form)
            assert f.Part_I.A.address == '123 Main St, Ohio'
            self.assertIsInstance(f.Part_I.B, Form)

    def test_building_from_json_discards_old_outputs(self):
        for json in json_in, json_empty_output, json_filled_output:
            f = load_json(json)
            assert f._outputs == []
            with self.assertRaises(AttributeError):
                f.A.profit
            with self.assertRaises(AttributeError):
                f.total_rents

    def test_building_from_json_detects_decimals(self):
        for json in json_in, json_empty_output, json_filled_output:
            f = load_json(json)
            self.assertIsInstance(f.Part_I.A.rents, Decimal)
            self.assertIsInstance(f.Part_I.B.expenses, Decimal)
            assert str(f.Part_I.A.rents) == '900.00'
            assert str(f.Part_I.B.expenses) == '230.00'

    def test_building_from_json_detects_decimals_in_lists(self):
        f = load_json(u'{"inputs": {"line1": [["First Bank", "1.23"],'
                      ' ["Second Bank", "4.56"]]}}')
        assert isinstance(f.line1[0][1], Decimal)
        assert isinstance(f.line1[1][1], Decimal)
        assert f.line1 == [["First Bank", Decimal('1.23')],
                           ["Second Bank", Decimal('4.56')]]

    def test_building_from_json_detects_many_digit_decimals(self):
        f = load_json(u'{"inputs": {"line1": [["First Percent", "1.2"],'
                      ' ["Second Percent", "4.56001"]]}}')
        assert isinstance(f.line1[0][1], Decimal)
        assert isinstance(f.line1[1][1], Decimal)
        assert f.line1 == [["First Percent", Decimal('1.2')],
                           ["Second Percent", Decimal('4.56001')]]

    def test_json_output_handles_decimals_in_lists(self):
        f = Form()
        f.line1 = [["First Bank", Decimal('1.23')],
                   ["Second Bank", Decimal('4.56')]]
        assert dump_json(f) == dedent(u'''\
            {
             "inputs": {
              "line1": [
               [
                "First Bank",
                "1.23"
               ],
               [
                "Second Bank",
                "4.56"
               ]
              ]
             },
             "outputs": {}
            }
            ''')

    def test_building_from_json_detects_negative_decimals(self):
        f = load_json(u'{"inputs": {"value": "-100.23"}}')
        self.assertIsInstance(f.value, Decimal)
        assert str(f.value) == '-100.23'

    def test_dumping_form_preserves_inputs(self):
        for json in json_in, json_empty_output, json_filled_output:
            f = load_json(json)
            j = dump_json(f)
            assert j == json_empty_output

    def test_dumping_form_preserves_inputs_and_includes_new_outputs(self):
        for json in json_in, json_empty_output, json_filled_output:
            f = load_json(json)
            f._enter_output_mode()
            process_form(f)
            j = dump_json(f)
            assert j == json_filled_output

    def test_dumping_form_includes_output_subforms(self):
        f = load_json('{"inputs": {"A": {"a": 1}}}')
        f._enter_output_mode()
        f.B = Form()
        f.B._enter_output_mode()
        f.B.b = 2
        j = dump_json(f)
        assert j == dedent(u'''\
            {
             "inputs": {
              "A": {
               "a": 1
              }
             },
             "outputs": {
              "B": {
               "b": 2
              }
             }
            }
            ''')

    def test_loading_list_of_subforms(self):
        f = load_json('{"inputs": {"items": [{"n": 10}, {"m": 11}]}}')
        assert len(f.items) == 2
        assert isinstance(f.items[0], Form)
        assert isinstance(f.items[1], Form)
        assert f.items[0].n == 10
        assert f.items[1].m == 11

    def test_dumping_list_of_subforms(self):
        f = load_json('{"inputs": {"items": [{"n": 10}, {"m": 11}]}}')
        f._enter_output_mode()
        f.items[0].x = 100
        f.items[0].y = 101
        j = dump_json(f)
        assert j == dedent(u'''\
            {
             "inputs": {
              "items": [
               {
                "n": 10
               },
               {
                "m": 11
               }
              ]
             },
             "outputs": {
              "items": [
               {
                "x": 100,
                "y": 101
               },
               {}
              ]
             }
            }
            ''')


json_in = u'''{
 "inputs": {
  "form": "rental_income",
  "ssn": "123-45-6789",
  "name": "Lynn Smith",
  "Part_I": {
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
}
'''

json_empty_output = json_in[:-3] + u''',
 "outputs": {}
}
'''

json_filled_output = json_in[:-3] + u''',
 "outputs": {
  "Part_I": {
   "A": {
    "profit": "800.00",
    "tax": "80.00"
   },
   "B": {
    "profit": "570.00",
    "tax": "57.00"
   }
  },
  "total_rents": "1,700.00",
  "total_expenses": "330.00",
  "total_profit": "1,370.00",
  "total_tax": "137.00"
 }
}
'''

def process_form(f):
    subs = (f.Part_I.A, f.Part_I.B)
    for sub in subs:
        sub.profit = sub.rents - sub.expenses
        sub.tax = cents(sub.profit / 10)
    f.total_rents = sum(sub.rents for sub in subs)
    f.total_expenses = sum(sub.expenses for sub in subs)
    f.total_profit = sum(sub.profit for sub in subs)
    f.total_tax = sum(sub.tax for sub in subs)
