import waiter as wt

def mainB():
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
    waiter = wt.Waiter("")
    dict_order = waiter.json_to_dict(backup_order)
    ordered, unavailable = waiter.process_order(dict_order)
    print("Your order is: ", end="")
    for item in ordered:
            print(item, end=", ")
    print()
    print("Unfortunately we don't have: ", end="")
    for item in unavailable:
        print(item, end=", ")
    print("\n")

def main():
    order_str = """
    I would like to order McCrispy without pickle and 5 large french fries. Change 2 of french 
    fries to 2 Big Mac and add a Coke. Also add one Chicken Biriani.
    """.strip()
    waiter = wt.Waiter(order_str)
    ordered, unavailable = waiter.take_order()
    print("Your order is: ", end="")
    for item in ordered:
            print(item, end=", ")
    print()
    print("Unfortunately we don't have: ", end="")
    for item in unavailable:
        print(item, end=", ")
    print("\n")


if __name__ == "__main__":
    main()
    # mainB()