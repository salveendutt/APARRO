from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp

# instantiate pipeline with bfloat16 and enable batching
pipeline = FlaxWhisperPipline("openai/whisper-medium.en", dtype=jnp.float16, batch_size=16)

outputs = pipeline("y2mate.com - Martin Luther King Jr I have a dream Audio Clip.mp3",  task="transcribe")

print(outputs)