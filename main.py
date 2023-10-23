from ctransformers import AutoModelForCausalLM
import json
from thefuzz import fuzz, process

def create_prompt(input_order):
    prompt = f"""
    Read the restaurant order delimited by triple backticks and return a JSON file depending on \
    what customer ordered with the following keys: food_id, quantity, comment. 
    
    Order: ```{input_order}```
    JSON:
    """.strip()
    return prompt

def initialize_model():
    return AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.1-GGUF", \
        model_file="mistral-7b-instruct-v0.1.Q5_K_M.gguf", model_type="mistral")

def take_order(order):
    prompt = create_prompt(order)
    print(prompt)
    llm = initialize_model()
    print("Predicing...")
    json_order = llm(prompt, max_new_tokens=2048, temperature=0.0, top_k=55, top_p=0.9, repetition_penalty=1.2)
    print("#" + json_order + "#")
    return json_order

def main():
    order = """
    I would like to order Mac Crispy without pickle and 5 large french fries. Change 2 of french 
    fries to 2 big macs and add a coke.
    """.strip()
    order = take_order(order)
    # MAYBE FUZZY JSON BY MYSELF??
    json_order = '[' + order + ']'
    data = json.loads(json_order.strip())
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    main()