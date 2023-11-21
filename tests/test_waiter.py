import os
import sys
import unittest
from unittest.mock import MagicMock
import textwrap

# Add the 'app' directory to the system path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.append(app_dir)

# Import the module under test
import waiter as wt


class TestWaiter(unittest.TestCase):
    """Test cases for the Waiter class."""

    def setUp(self):
        """Set up the test environment."""
        self.waiter = wt.Waiter()

    def test_create_prompt(self):
        """Test the creation of a prompt."""
        order = "Sample order for the test"
        expected_prompt = textwrap.dedent(f"""
        random message
        ```{order}```
        JSON:
        """).strip()
        prompt = wt.create_prompt(order, initial_prompt="random message")
        self.assertEqual(prompt, expected_prompt)

    def test_initialize_model(self):
        """Test the initialization of the model."""
        self.waiter.initialize_model = MagicMock(return_value="Mocked Model")
        model = self.waiter.initialize_model()
        self.assertEqual(model, "Mocked Model")

    def test_json_to_dict(self):
        """Test conversion from JSON to dictionary."""
        json_str = '{"dish": "McChicken", "quantity": 2, "comment": "Extra cheese"}'
        expected_dict = [{"dish": "McChicken", "quantity": 2, "comment": "Extra cheese"}]
        result = wt.json_to_dict(json_str)
        self.assertEqual(result, expected_dict)

    def test_process_order_with_available_items(self):
        """Test processing an order with available items."""
        order = [{"dish": "Big Mac", "quantity": 2, "comment": "No pickles"}]
        self.waiter._Waiter__process_order(order)
        ordered_items = self.waiter._Waiter__ordered
        self.assertEqual(len(ordered_items), 1)
        self.assertEqual(ordered_items[0]["dish"], "Big Mac")

    def test_process_order_with_unavailable_items(self):
        """Test processing an order with unavailable items."""
        order = [{"dish": "Unknown Dish", "quantity": 1, "comment": "Extra sauce"}]
        self.waiter._Waiter__process_order(order)
        unavailable_items = self.waiter._Waiter__unavailable
        self.assertEqual(len(unavailable_items), 1)
        self.assertEqual(unavailable_items[0], "Unknown Dish")

    def test_create_order(self):
        """Test the creation of an order."""
        order_str = 'Give me a Big Mac'
        self.waiter._Waiter__llm = MagicMock(
            return_value='{"dish": "Big Mac", "quantity": 1, "comment": ""}'
        )
        self.waiter.create_order(order_str)
        ordered_items = self.waiter._Waiter__ordered
        self.assertEqual(len(ordered_items), 1)
        self.assertEqual(ordered_items[0]["dish"], "Big Mac")


if __name__ == '__main__':
    unittest.main()
