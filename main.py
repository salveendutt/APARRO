import order as od

def main():
    order = """
    I would like to order McCrispy without pickle and 5 large french fries. Change 2 of french 
    fries to 2 Big Mac and add a Coke. Also add one Chicken Biriani.
    """.strip()
    
    order = od.take_order(order)
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