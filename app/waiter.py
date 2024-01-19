"""
This module contains the Waiter class which is responsible for processing customer orders.
It uses a language model to interpret the orders and matches them against a menu.
"""
import logging
import textwrap

from ctransformers import AutoConfig, AutoModelForCausalLM
from thefuzz import process
import menu as mn

MODEL_PATH = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
MODEL_FILE = "mistral-7b-instruct-v0.1.Q5_K_M.gguf"
MODEL_TYPE = "mistral"
INITIAL_PROMPT = textwrap.dedent("""
Welcome to our restaurant order processing service! Before proceeding, carefully analyze the customer's order, which may include complex requests and modifications. Accurate interpretation is crucial for customer satisfaction.
Please present the customer's order in a clear and structured manner, following these instructions:
1. Thoroughly analyze the customer's order, paying attention to details and potential modifications. If the customer didn't mention any items, don't return anything.
2. For each item in the order, provide the following information:
- Dish: Name of the dish.
- Quantity: Number of portions or items ordered.
- Comment: If not specified - keep it empty. Here should be specific instructions or comments, including drink sizes (e.g., large, medium, small) and other details (e.g., cold, hot, spicy).
3. Return the order in CSV format, use | as a separator character. After comment always add new line. First line always header, starting from second line return what was ordered in format discussed before.
4. Do not output anything other than CSV output.
""") 
logging.basicConfig(level=logging.INFO)

class Waiter:
    """
    The Waiter class processes customer orders by interpreting them with a large language model
    and matching them against a known menu. It handles both available and unavailable items.
    """
    def __init__(self):
        self._ordered = []
        self._unavailable = []
        self._llm = initialize_model(MODEL_PATH, MODEL_FILE, MODEL_TYPE)

    def predict(self, prompt):
        psv_order = self._llm(prompt, 
                            max_new_tokens=2048, 
                            temperature=0.0,
                            top_k=55, 
                            top_p=0.9, 
                            repetition_penalty=1.2).replace("```", "").replace(".", "")
        psv_order = textwrap.dedent(psv_order)
        return psv_order
    
    def create_order(self, order: str):
        """
        Processes a customer's order and returns a confirmed order and items not on the menu.

        Args:
        order (str): The customer's order as a string.

        Returns:
        tuple: A tuple containing two lists - ordered and ordered_not_in_menu.
        """
        # Stage 1, Creating Prompt for the Model
        prompt = create_prompt(order)
        print(order)
        # Stage 2, Running the model
        logging.info("Predicting...")
        psv_order = self.predict(prompt)
        logging.info("Model output: %s", psv_order)
        # Stage 3, Processing the Order
        self.process_psv_order(psv_order)

    def process_psv_order(self, order: str):
        """
        Processes a pipe-separated values (PSV) order string to identify valid food items.

        This function iterates over each line of the input `order` string, which is expected to be in PSV format (each line contains fields separated by '|'). It splits each line into dish, quantity, and comment. Then, it uses fuzzy matching to find the most similar item from a predefined menu (`mn.mcdonalds_menu`). If the similarity score is 90% or higher, the item is considered a valid menu item and is added to the `_ordered` list with its details. Otherwise, it is added to the `_unavailable` list.

        Args:
            order (str): A string representing the order, with each line in the format of 'dish|quantity|comment'.

        Attributes Modified:
            self._ordered (list): A list of dictionaries where each dictionary contains 'dish', 'comment', and 'quantity' for confirmed menu items.
            self._unavailable (list): A list of dishes that are not found in the menu or have a similarity score below 90.
        """
        for line in order.split('\n'):
            if '|' not in line and 'Dish' not in line and '---' not in line:
                continue
            if not line.strip():
                continue
            food_item = line.split('|')
            dish, quantity, comment = food_item
            # Using fuzziness to find the most similar item on the menu
            best_match, similarity_score = process.extractOne(dish, mn.mcdonalds_menu)
            # Make sure this item does belong in the menu,
            # if similarity is below 90 - it is not in menu
            if similarity_score >= 90:
                confirmed_item = {"dish": best_match, "comment": comment, "quantity": quantity}
                self._ordered.append(confirmed_item)
            else:
                self._unavailable.append(dish)
        
    def read_psv_order(self, order: str):
        """
        Processes a pipe-separated values (PSV) order string to identify valid food items.

        This function iterates over each line of the input `order` string, which is expected to be in PSV format (each line contains fields separated by '|'). It splits each line into dish, quantity, and comment. Then, it uses fuzzy matching to find the most similar item from a predefined menu (`mn.mcdonalds_menu`). If the similarity score is 90% or higher, the item is considered a valid menu item and is added to the `_ordered` list with its details. Otherwise, it is added to the `_unavailable` list.

        Args:
            order (str): A string representing the order, with each line in the format of 'dish|quantity|comment'.

        Attributes Modified:
            self._ordered (list): A list of dictionaries where each dictionary contains 'dish', 'comment', and 'quantity' for confirmed menu items.
            self._unavailable (list): A list of dishes that are not found in the menu or have a similarity score below 90.
        """
        for line in order.split('\n'):
            if '|' not in line and 'Dish' not in line and '---' not in line:
                continue
            if not line.strip():
                continue
            food_item = line.split('|')
            dish, quantity, comment = food_item

                
    def get_order(self):
        """
        Prints the ordered items and unavailable items in a formatted manner.

        Args:
        ordered (list): List of ordered items (as dictionaries 
        with keys "dish", "comment", and "quantity").
        unavailable (list): List of unavailable items.
        """
        ordered_items = []
        unavailable_items = self._unavailable
        for item in self._ordered:
            ordered_item_str = f"{item['quantity']} {item['dish']}"
            if item['comment']:
                ordered_item_str += f" ({item['comment']})"
            ordered_items.append(ordered_item_str)
        ordered_str = ", ".join(ordered_items)
        unavailable_str = ", ".join(self._unavailable)
        result_str = ""
        if ordered_items:
            result_str += f"{ordered_str}\n"
        else:
            result_str += "Sorry, there is nothing in our menu which you ordered\n"
        if unavailable_items:
            result_str += f"Unfortunately we don't have: {unavailable_str}\n"
        return result_str
    

def create_prompt(order: str, initial_prompt=INITIAL_PROMPT):
    """
    Creates a prompt for the model to process a customer's order.

    Args:
    order (str): The customer's order as a string.

    Returns:
    str: The prompt for the model including the order.
    """
    prompt = textwrap.dedent(f"""
    {initial_prompt}
    ```{order}```
    CSV order with | separator:
    """)
    return prompt.strip()

def initialize_model(model_path_or_repo_id, model_file, model_type):
    """
    Initializes an LLM from AutoModelForCausalLM.

    Returns:
    AutoModelForCausalLM: The initialized large language model.
    """
    try:
        config = AutoConfig.from_pretrained("TheBloke/Mistral-7B-v0.1-GGUF")
        config.config.max_new_tokens = 2560
        config.config.context_length = 4096
        return AutoModelForCausalLM.from_pretrained(model_path_or_repo_id,
                                                    model_file=model_file,
                                                    model_type=model_type,
                                                    config=config)
    except Exception as e:
        raise RuntimeError("Error initializing the model: " + str(e)) from e
