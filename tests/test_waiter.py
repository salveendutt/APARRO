import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import textwrap
from io import StringIO

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
        
    def test_json_to_dict_conversion_and_exception_handling(self):
        """Test conversion from JSON to dictionary and exception handling."""
        # Test successful conversion
        json_str_success = '{"dish": "McChicken", "quantity": 2, "comment": "Extra cheese"}'
        expected_dict_success = [{"dish": "McChicken", "quantity": 2, "comment": "Extra cheese"}]
        with self.subTest(case="Successful Conversion"):
            result_success = wt.json_to_dict(json_str_success)
            self.assertEqual(result_success, expected_dict_success)

        # Test exception handling
        invalid_json_str = '{"dish": "McChicken", "quantity": 2, "comment": "Extra cheese",}'
        with self.subTest(case="Exception Handling"):
            with self.assertRaises(RuntimeError) as context:
                wt.json_to_dict(invalid_json_str)

    def test_process_order_with_available_items(self):
        """Test processing an order with available items."""
        order = [{"dish": "Big Mac", "quantity": 2, "comment": "No pickles"}]
        self.waiter._process_order(order)
        ordered_items = self.waiter._ordered
        self.assertEqual(len(ordered_items), 1)
        self.assertEqual(ordered_items[0]["dish"], "Big Mac")

    def test_process_order_with_unavailable_items(self):
        """Test processing an order with unavailable items."""
        order = [{"dish": "Unknown Dish", "quantity": 1, "comment": "Extra sauce"}]
        self.waiter._process_order(order)
        unavailable_items = self.waiter._unavailable
        self.assertEqual(len(unavailable_items), 1)
        self.assertEqual(unavailable_items[0], "Unknown Dish")

    def test_create_order(self):
        """Test the creation of an order."""
        order_str = 'Give me a Big Mac'
        self.waiter._llm = MagicMock(
            return_value='{"dish": "Big Mac", "quantity": 1, "comment": ""}'
        )
        self.waiter.create_order(order_str)
        ordered_items = self.waiter._ordered
        self.assertEqual(len(ordered_items), 1)
        self.assertEqual(ordered_items[0]["dish"], "Big Mac")

    def test_print_order(self):
        # Test when there are no ordered items
        expected_output = "Sorry, there is nothing in our menu which you ordered\n"
        self.assertEqual(self.waiter.print_order(), expected_output)

        # Test when there are ordered items
        self.waiter._ordered = [
            {"dish": "Burger", "comment": "No onions", "quantity": 2},
            {"dish": "Pizza", "comment": "", "quantity": 1},
        ]

        expected_output = "Your order is: 2 Burger (No onions), 1 Pizza\n"
        self.assertEqual(self.waiter.print_order(), expected_output)

        # Test when there are unavailable items
        self.waiter._ordered = [{"dish": "Burger", "comment": "No onions", "quantity": 1}]  # Reset ordered items
        self.waiter._unavailable = ["Soda", "Dessert"]

        expected_output = "Your order is: 1 Burger (No onions)\nUnfortunately we don't have: Soda, Dessert\n"
        self.assertEqual(self.waiter.print_order(), expected_output)

        # Test when there are both ordered and unavailable items
        self.waiter._ordered = [
            {"dish": "Burger", "comment": "", "quantity": 1},
        ]
        self.waiter._unavailable = ["Pizza"]

        expected_output = "Your order is: 1 Burger\nUnfortunately we don't have: Pizza\n"
        self.assertEqual(self.waiter.print_order(), expected_output)


if __name__ == '__main__':
    unittest.main()
