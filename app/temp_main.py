import waiter as wt
import transcriber as tr
    
def main_output_demo():
    backup_order = """
    {
        "dish": "MacCrispy",
        "quantity": 1,
        "comment": "without pickle"
    },
    {
        "dish": "French Fries",
        "quantity": 3,
        "comment": ""
    },
    {
        "dish": "Mac Double",
        "quantity": 2,
        "comment": ""
    },
    {
        "dish": "Chicken Biriani",
        "quantity": 1,
        "comment": "Spicy"
    },
    {
        "dish": "Coke",
        "quantity": 1,
        "comment": ""
    }"""
    waiter = wt.Waiter()
    dict_order = waiter.json_to_dict(backup_order)
    waiter.process_order(dict_order)
    waiter.print_order()

def main_transcribe():
    transcriber = tr.Transcriber(model_name="medium.en", device_type="cuda")
    order = transcriber.transcribe()
    print(order)

def main_predict_order():
    order_str = """
    I would like to order McCrispy without pickle and 5 large french fries. Change 2 of french 
    fries to 2 Big Mac and add a Coke. Also add one Chicken Biriani.
    """
    waiter = wt.Waiter()
    waiter.create_order(order_str)
    waiter.print_order()


if __name__ == "__main__":
    main_transcribe()
    # main_predict_order()
    # main_output_demo()