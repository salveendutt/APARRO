from ctransformers import AutoModelForCausalLM


def create_prompt(input_order):
    prompt = f"""
    Read the restaurant order delimited by triple backticks and answer what customer has ordered 
    in a JSON format with the following keys: food_id, quantity, comment. 
    ```{input_order}```
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
    print(json_order)


def main():
    order = """
    I would like to order Mac Crispy without pickle and 5 large french fries. Change 2 of french 
    fries to 2 big macs and add a coke.
    """.strip()
    take_order(order)

if __name__ == "__main__":
    main()