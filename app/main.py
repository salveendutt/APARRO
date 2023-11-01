import restaurant as rst
# TODO (Depricated if we change to jax_whisper): device_type = "cuda" if torch.cuda.is_available() 
# else "cpu". If we use cpu, then float16 returns error, hence let's fix it.
DEVICE_TYPE = "cuda"
# DEVICE_TYPE = "cpu"
MODEL_NAME = "medium.en"

def main():
    restaurant = (
        rst.Restaurant.Builder()
        .with_transcriber(model_name=MODEL_NAME, device_type=DEVICE_TYPE)
        .with_waiter()
        .build()
    )
    restaurant.take_order()
    
if __name__ == "__main__":
    main()
