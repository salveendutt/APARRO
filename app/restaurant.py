"""
This module contains the Restaurant and RestaurantBuilder classes.
The Restaurant class is used to take customer orders through a transcriber 
and process them with a waiter.
The RestaurantBuilder class provides a fluent interface to construct a Restaurant instance.
"""

import waiter as wt
import transcriber as tr

class Restaurant:
    """
    The Restaurant class encapsulates the process of taking and processing customer orders.
    """
    def __init__(self):
        self._waiter = None
        self._transcriber = None

    def set_waiter(self, waiter):
        """
        Sets the waiter for the restaurant.
        """
        self._waiter = waiter

    def set_transcriber(self, transcriber):
        """
        Sets the transcriber for the restaurant.
        """
        self._transcriber = transcriber

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
        return self._waiter.print_order()

    def take_order_with_str(self, order: str):
        """
        Takes a customer's order as an input and passing it to the waiter.

        Calls the print_order function to display the order to the customer.
        """
        if self._waiter is None:
            raise ValueError("Waiter must be set before taking orders.")
        self._waiter.create_order(order)
        return self._waiter.print_order()

    @staticmethod
    def builder():
        """
        Static factory method to create a new RestaurantBuilder instance.

        Returns:
        RestaurantBuilder: A new RestaurantBuilder instance.
        """
        return RestaurantBuilder()

class RestaurantBuilder:
    """
    The RestaurantBuilder class provides methods to configure and build a Restaurant instance.
    """
    def __init__(self):
        self._restaurant = Restaurant()

    def with_waiter(self) -> 'RestaurantBuilder':
        """
        Sets the waiter for the restaurant.

        Returns:
        RestaurantBuilder: The current RestaurantBuilder instance with waiter.
        """
        waiter = wt.Waiter()
        self._restaurant.set_waiter(waiter)
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
        transcriber = tr.Transcriber(model_name, device_type)
        self._restaurant.set_transcriber(transcriber)
        return self

    def build(self) -> 'Restaurant':
        """
        Builds and returns the configured Restaurant instance.

        Returns:
        Restaurant: The configured Restaurant instance.
        """
        return self._restaurant
