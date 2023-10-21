import argparse
import io
import os
import speech_recognition as sr
import torch

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

from faster_whisper import WhisperModel

audio_model = WhisperModel("medium.en", device="cuda", compute_type="float16")

# Create a class for whisper, where you can initialize this class in another file
# and you will be able to do text = my_model.start_recording(smth) and text will
# be what was said after the recording started. No need to implement at this 
# stage anything in live. The voice will be recorded from mic, and the model will
# translate it.
## IN SUMMARY: This module should combine whisper and listening via mic module 
## and be easy to use. 

# Must have a method start_recording (or similar name) which will do everything
# until stop_recording was called (OR MAYBE you can implement other stopping 
# mechanism) 

# Hint, try to use OOD classes and a simplest factory method (or anything else)