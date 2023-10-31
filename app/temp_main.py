import restaurant as rst

def main():
    restaurant = (
        rst.Restaurant.Builder()
        .with_transcriber(model_name="medium.en", device_type="cuda")
        .with_waiter()
        .build()
    )
    restaurant.take_order()
    
if __name__ == "__main__":
    main()