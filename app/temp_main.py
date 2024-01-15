"""
This module demonstrates different functionalities of the restaurant order processing system.
It includes demonstrations of order transcription, order prediction, and direct order processing.
"""

import waiter as wt
import transcriber as tr

def main_transcribe():
    """
    Demonstrates the transcription of an order using the transcriber.
    """
    transcriber = tr.Transcriber(model_name="medium.en", device_type="cuda")
    order = transcriber.transcribe()
    print(order)

def main_predict_order():
    """
    Demonstrates the prediction and processing of an order string using the waiter.
    """
    order_str = """
    I would like to order a McCrispy without pickle and 5 large french fries. Change 2 of the 
    french fries to 2 Big Macs and add a Coke. Also add one Chicken Biriani.
    """
    waiter = wt.Waiter()
    waiter.create_order(order_str)
    print(waiter.get_order())

def main_predict_order2():
    """
    Demonstrates the prediction and processing of an order string using the waiter.
    """
    order_str = """
McCrispy||1||no pickle, dry
5 large french fries||3||
2 Big Macs||2||
Coke||1||
Chicken Biriani||1||
    """
    waiter = wt.Waiter()
    waiter._process_psv_order(order_str)
    waiter.print_order()

if __name__ == "__main__":
    # Uncomment the function you wish to demonstrate
    main_transcribe()
    # main_predict_order()
    # main_predict_order2()
    # main_output_demo()
