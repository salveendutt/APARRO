import json
import menu as mn
from ctransformers import AutoModelForCausalLM
from thefuzz import fuzz, process

class Waiter:
    def create_prompt(self, order: str):
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
        """.strip()
        return prompt

    def initialize_model(self):
        """
        Initializes an LLM from AutoModelForCausalLM.

        Returns:
        AutoModelForCausalLM: The initialized large language model.
        """
        try:
            return AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
                                                        model_file="mistral-7b-instruct-v0.1.Q5_K_M.gguf",
                                                        model_type="mistral")
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

        Returns:
        tuple: A tuple containing two lists - confirmed_order and order_not_in_menu.
        """
        confirmed_order = []
        order_not_in_menu = []
        for food_item in order:
            dish = food_item["dish"]
            best_match, similarity_score = process.extractOne(dish, mn.mcdonalds_menu)
            if similarity_score >= 90:
                confirmed_order.append(best_match)
            else:
                order_not_in_menu.append(dish)
        return (confirmed_order, order_not_in_menu)

    def create_order(self, order: str):
        """
        Processes a customer's order and returns a confirmed order and items not on the menu.

        Args:
        order (str): The customer's order as a string.

        Returns:
        tuple: A tuple containing two lists - ordered and ordered_not_in_menu.
        """
        try:
            # Stage 1, Creating Prompt for the Model
            prompt = self.create_prompt(order)
            print(prompt)
            # Stage 2, Preparing model
            llm = self.initialize_model()
            # Stage 3, Running the model
            print("Predicting...")
            json_order = llm(prompt, max_new_tokens=2048, temperature=0.0, top_k=55, top_p=0.9, repetition_penalty=1.2)
            print("model output:" + json_order)
            # Stage 4, Converting from JSON to dictionary
            dict_order = self.json_to_dict(json_order)
            # Stage 5, Processing the Order
            ordered, ordered_not_in_menu = self.process_order(dict_order)  # You need to implement process_order
            return (ordered, ordered_not_in_menu)
        except Exception as e:
            raise Exception("Error processing order: " + str(e))

