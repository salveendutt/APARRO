import json
import menu as mn
from ctransformers import AutoModelForCausalLM
from thefuzz import process

MODEL_PATH = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
MODEL_FILE = "mistral-7b-instruct-v0.1.Q5_K_M.gguf"
MODEL_TYPE = "mistral"

class Waiter:
    def __init__(self):
        self.ordered = []
        self.unavailable = []
        
    def create_prompt(self, order: str):
        """
        Creates a prompt for the model to process a customer's order.

        Args:
        order (str): The customer's order as a string.

        Returns:
        str: The prompt for the model including the order.
        """
        prompt = f"""
        Welcome to our restaurant order processing service. Before proceeding, please ensure that you spend some time analyzing the customer's order carefully. Customers may provide complex orders with modifications, and it's important to accurately interpret their preferences.
        Please provide the customer's order in a clear and structured manner. We will assist you in converting it to JSON format for easy processing. Follow the instructions below:
        1. Spend time to thoroughly analyze what the customer has ordered. Customers may provide detailed requests, such as modifying their initial order, which requires your attention to ensure their order is processed accurately.
        2. Provide the following information for each item:
        - Dish: The name of the dish.
        - Quantity: The number of portions or items ordered.
        - Comment: Any specific instructions or comments related to the order.
        3. Format the order as a JSON object with the following keys:
        {{
            "dish": "Dish Name",
            "quantity": 2,  # Adjust the quantity as needed
            "comment": "Add extra cheese"
        }}
        Now please find the order below inside backtics and return order in the proper JSON format
        ```{order}```
        JSON:
        """
        return prompt
    
    def create_old_prompt(self, order: str):
        """
        Creates a prompt for the model to process a customer's order.

        Args:
        order (str): The customer's order as a string.

        Returns:
        str: The prompt for the model including the order.
        """
        prompt = f"""
        Read the restaurant order delimited by triple backticks, step by step analyze what the customer has ordered, and write it down in JSON format with the following keys: dish, quantity, comment.
        ```{order}```
        JSON:
        """
        return prompt
    def initialize_model(self, model_path_or_repo_id, model_file, model_type):
        """
        Initializes an LLM from AutoModelForCausalLM.

        Returns:
        AutoModelForCausalLM: The initialized large language model.
        """
        try:
            return AutoModelForCausalLM.from_pretrained(model_path_or_repo_id,
                                                        model_file=model_file,
                                                        model_type=model_type)
        except Exception as e:
            raise Exception("Error initializing the model: " + str(e))


    def json_to_dict(self, json_str: str):
        """
        Converts a JSON string to a Python dictionary.

        Args:
        json_str (str): The JSON string to convert.

        Returns:
        dict: The Python dictionary representation of the JSON.
        """
        try:
            json_str = json_str.strip()
            json_str = '[' + json_str + ']'
            json_dict = json.loads(json_str)
            return json_dict
        except Exception as e:
            raise Exception("Error converting JSON to dictionary: " + str(e))


    def process_order(self, order: dict):
        """
        Processes a customer's order, confirming items and identifying those not on the menu.

        Args:
        order (dict): The customer's order as a dictionary.

        Updates:
        self.ordered (list of dictionaries): List of dictionaries containing keys as "dish", "quantity", and "comment".
        self.unavailable (list of dishes): List of dishes (names) not found in the menu.
        """
        for food_item in order:
            dish = food_item["dish"]
            quantity = food_item["quantity"]
            comment = food_item["comment"]
            # Using fuzziness to find the most similar item on the menu
            best_match, similarity_score = process.extractOne(dish, mn.mcdonalds_menu)
            # Make sure this item does belong in the menu, if similarity is below 90 - it is not in menu
            if similarity_score >= 90:
                confirmed_item = {"dish": best_match, "comment": comment, "quantity": quantity}
                self.ordered.append(confirmed_item)
            else:
                self.unavailable.append(dish)
        return

    def create_order(self, order: str):
        """
        Processes a customer's order and returns a confirmed order and items not on the menu.

        Args:
        order (str): The customer's order as a string.

        Returns:
        tuple: A tuple containing two lists - ordered and ordered_not_in_menu.
        """
        # Stage 1, Creating Prompt for the Model
        prompt = self.create_prompt(order)
        print(prompt)
        # Stage 2, Preparing model
        llm = self.initialize_model(MODEL_PATH, MODEL_FILE, MODEL_TYPE)
        # Stage 3, Running the model
        print("Predicting...")
        json_order = llm(prompt, max_new_tokens=2048, temperature=0.0, top_k=55, top_p=0.9, repetition_penalty=1.2)
        print(f"Model output: {json_order}")
        # Stage 4, Converting from JSON to dictionary
        dict_order = self.json_to_dict(json_order)
        # Stage 5, Processing the Order
        self.process_order(dict_order)
        
    def print_order(self):
        """
        Prints the ordered items and unavailable items in a formatted manner.

        Args:
        ordered (list): List of ordered items (as dictionaries with keys "dish", "comment", and "quantity").
        unavailable (list): List of unavailable items.
        """
        ordered_items = []
        unavailable_items = self.unavailable
        
        for item in self.ordered:
            ordered_item_str = f"{item['quantity']} {item['dish']}"
            if item['comment']:
                ordered_item_str += f" ({item['comment']})"
            ordered_items.append(ordered_item_str)

        ordered_str = ", ".join(ordered_items)
        unavailable_str = ", ".join(self.unavailable)

        if ordered_items:
            print(f"Your order is: {ordered_str}")
        else:
            print("Sorry, there is nothing in our menu which you ordered")

        if unavailable_items:
            print(f"Unfortunately we don't have: {unavailable_str}\n")

