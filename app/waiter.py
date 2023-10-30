import json
import menu as mn
from ctransformers import AutoModelForCausalLM
from thefuzz import fuzz, process

class Waiter:
    def __init__(self, order: str):
        self.order = order
        
    def create_prompt(self):
        prompt = f"""
        Read the restaurant order delimited by triple backticks, step by step analyze what the customer has ordered, \
        and write it down in JSON format with the following keys: dish, quantity, comment.
        ```{self.order}```
        JSON:
        """.strip()
        return prompt

    def initialize_model(self):
        return AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.1-GGUF", \
            model_file="mistral-7b-instruct-v0.1.Q5_K_M.gguf", model_type="mistral")

    # TODO, make it ROBUST. { } ALWAYS should open and always should close.
    def json_to_dict(self, json_str: str):
        json_str = json_str.strip()
        json_str = '[' + json_str + ']'
        json_dict = json.loads(json_str)
        return json_dict

    def process_order(self, order: dict):
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
        
    def take_order(self):
        # Stage 1, Creating Prompt for the Model
        prompt = self.create_prompt()
        print(prompt)
        # Stage 2, Preparing model
        llm = self.initialize_model()
        # Stage 3, Running the model
        print("Predicing...")
        json_order = llm(prompt, max_new_tokens=2048, temperature=0.0, top_k=55, top_p=0.9, repetition_penalty=1.2)
        print("model output:" + json_order)
        # Stage 4, Converting from JSON to dictionary
        dict_order = self.json_to_dict(json_order)
        # Stage 5, Processing the Order
        ordered, ordered_not_in_menu = self.process_order(dict_order)
        return (ordered, ordered_not_in_menu) 