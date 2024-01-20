"""This module is the entry point for the restaurant application.

It sets up the restaurant with the necessary components and starts taking orders.
"""

import restaurant as rst
# device_type = "cuda" if torch.cuda.is_available() else "cpu".
# If we use cpu, then float16 returns error, hence let's fix it.
# DEVICE_TYPE = "cuda"
DEVICE_TYPE = "cpu"
MODEL_NAME = "medium.en"

def main():
    """Set up the restaurant and start taking orders."""
    restaurant = (
        rst.Restaurant.builder()
        .with_transcriber(model_name=MODEL_NAME, device_type=DEVICE_TYPE)
        .with_waiter()
        .build()
    )
    result = restaurant.take_order()
    print(result)

if __name__ == "__main__":
    main()
