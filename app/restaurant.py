import waiter as wt
import transcriber as tr

def print_order(ordered, unavailable):
    ordered_str = ", ".join(ordered)
    unavailable_str = ", ".join(unavailable)

    print(f"Your order is: {ordered_str}")
    print(f"Unfortunately we don't have: {unavailable_str}\n")
    
class Restaurant:
    def __init__(self):
        self.waiter = None
        self.transcriber = None

    @staticmethod
    def Builder():
        return RestaurantBuilder()
    
    def take_order(self):
        pred_order_str = self.transcriber.transcribe()
        ordered, unavailable = self.waiter.create_order(pred_order_str)
        print_order(ordered, unavailable)

class RestaurantBuilder:
    def __init__(self):
        self.restaurant = Restaurant()

    def with_waiter(self):
        self.restaurant.waiter = wt.Waiter()
        return self

    def with_transcriber(self, model_name: str, device_type: str):
        self.restaurant.transcriber = tr.Transcriber(model_name, device_type)
        return self

    def build(self):
        return self.restaurant