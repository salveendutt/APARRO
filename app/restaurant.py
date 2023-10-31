import waiter as wt
import transcriber as tr

def print_order(ordered, unavailable):
    """
    Prints the ordered items and unavailable items in a formatted manner.

    Args:
    ordered (list): List of ordered items.
    unavailable (list): List of unavailable items.
    """
    ordered_str = ", ".join(ordered)
    unavailable_str = ", ".join(unavailable)

    if len(ordered) != 0:
        print(f"Your order is: {ordered_str}")
    else: print("Sorry, there is nothing in our menu which you ordered")
    if len(unavailable) != 0:
        print(f"Unfortunately we don't have: {unavailable_str}\n")

class Restaurant:
    def __init__(self):
        self.waiter = None
        self.transcriber = None

    @staticmethod
    def Builder():
        """
        Static factory method to create a new RestaurantBuilder instance.

        Returns:
        RestaurantBuilder: A new RestaurantBuilder instance.
        """
        return RestaurantBuilder()
    
    def take_order(self):
        """
        Takes a customer's order by transcribing their voice and passing it to the waiter.

        Uses the transcriber to convert voice input into text and the waiter to create the order.

        Calls the print_order function to display the order to the customer.
        """
        pred_order_str = self.transcriber.transcribe()
        ordered, unavailable = self.waiter.create_order(pred_order_str)
        print_order(ordered, unavailable)

class RestaurantBuilder:
    def __init__(self):
        self.restaurant = Restaurant()

    def with_waiter(self):
        """
        Sets the waiter for the restaurant.

        Returns:
        RestaurantBuilder: The current RestaurantBuilder instance with waiter.
        """
        self.restaurant.waiter = wt.Waiter()
        return self

    def with_transcriber(self, model_name: str, device_type: str):
        """
        Sets the transcriber for the restaurant.

        Args:
        model_name (str): Name of the transcriber model.
        device_type (str): Type of device to use for transcribing.

        Returns:
        RestaurantBuilder: The current RestaurantBuilder instance with transcriber.
        """
        self.restaurant.transcriber = tr.Transcriber(model_name, device_type)
        return self

    def build(self):
        """
        Builds and returns the configured Restaurant instance.

        Returns:
        Restaurant: The configured Restaurant instance.
        """
        return self.restaurant
