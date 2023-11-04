import waiter as wt
import transcriber as tr

class Restaurant:
    def __init__(self):
        self._waiter = None
        self._transcriber = None

    def take_order(self):
        """
        Takes a customer's order by transcribing their voice and passing it to the waiter.

        Uses the transcriber to convert voice input into text and the waiter to create the order.

        Calls the print_order function to display the order to the customer.
        """
        if self._waiter is None or self._transcriber is None:
            raise ValueError("Waiter and transcriber must be set before taking orders.")
        
        pred_order_str = self._transcriber.transcribe()
        self._waiter.create_order(pred_order_str)
        self._waiter.print_order()

    @staticmethod
    def Builder():
        """
        Static factory method to create a new RestaurantBuilder instance.

        Returns:
        RestaurantBuilder: A new RestaurantBuilder instance.
        """
        return RestaurantBuilder()

class RestaurantBuilder:
    def __init__(self):
        self._restaurant = Restaurant()

    def with_waiter(self) -> 'RestaurantBuilder':
        """
        Sets the waiter for the restaurant.

        Returns:
        RestaurantBuilder: The current RestaurantBuilder instance with waiter.
        """
        self._restaurant._waiter = wt.Waiter()
        return self

    def with_transcriber(self, model_name: str, device_type: str) -> 'RestaurantBuilder':
        """
        Sets the transcriber for the restaurant.

        Args:
        model_name (str): Name of the transcriber model.
        device_type (str): Type of device to use for transcribing.

        Returns:
        RestaurantBuilder: The current RestaurantBuilder instance with transcriber.
        """
        self._restaurant._transcriber = tr.Transcriber(model_name, device_type)
        return self

    def build(self) -> 'Restaurant':
        """
        Builds and returns the configured Restaurant instance.

        Returns:
        Restaurant: The configured Restaurant instance.
        """
        return self._restaurant
