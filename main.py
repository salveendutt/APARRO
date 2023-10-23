import waiter as wt

def main():
    order_str = """
    I would like to order McCrispy without pickle and 5 large french fries. Change 2 of french 
    fries to 2 Big Mac and add a Coke. Also add one Chicken Biriani.
    """.strip()
    waiter = wt.Waiter(order_str)
    order = waiter.take_order()
    # order = """
    #     {
    #         "dish": "McCrispy",
    #         "quantity": 1,
    #         "comment": "without pickle"
    #     },
    #     {
    #         "dish": "French Fries",
    #         "quantity": 3,
    #         "comment": ""
    #     },
    #     {
    #         "dish": "Big Mac",
    #         "quantity": 2,
    #         "comment": ""
    #     },
    #     {
    #         "dish": "Chicken Biriani",
    #         "quantity": 1,
    #         "comment": "Spicy"
    #     },
    #     {
    #         "dish": "Coke",
    #         "quantity": 1,
    #         "comment": ""
    #     }"""
    # food_items = json_to_dict(order)

    
if __name__ == "__main__":
    main()