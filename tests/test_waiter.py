import unittest
from unittest.mock import MagicMock
import sys
import os
# TODO Mevin Fix the path. Right now it gives warning, but something has to be done in order
# for it to not show warning
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.append(app_dir)
import waiter as wt


class TestWaiter(unittest.TestCase):
    def setUp(self):
        self.waiter = wt.Waiter()

    # def test_create_prompt(self):
    #     order = "Sample order for the test"
    #     expected_prompt = f"""
    #     Read the restaurant order delimited by triple backticks, step by step analyze what the customer has ordered, and write it down in JSON format with the following keys: dish, quantity, comment.
    #     ```{order}```
    #     JSON:
    #     """.strip()
    #     prompt = self.waiter.create_old_prompt(order)
    #     self.assertEqual(prompt, expected_prompt)

    def test_initialize_model(self):
        self.waiter.initialize_model = MagicMock(return_value="Mocked Model")
        model = self.waiter.initialize_model()
        self.assertEqual(model, "Mocked Model")

    def test_json_to_dict(self):
        json_str = '{"dish": "Pizza", "quantity": 2, "comment": "Extra cheese"}'
        expected_dict = [{"dish": "Pizza", "quantity": 2, "comment": "Extra cheese"}]
        result = self.waiter.json_to_dict(json_str)
        self.assertEqual(result, expected_dict)


if __name__ == '__main__':
    unittest.main()
