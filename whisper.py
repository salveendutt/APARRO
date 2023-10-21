import argparse
import io
import os
import speech_recognition as sr
import torch
COMPUTE_TYPE = "float16"
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

from faster_whisper import WhisperModel

audio_model = WhisperModel("medium.en", device="cuda", compute_type=COMPUTE_TYPE)

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

# class mevinWhiser:
#   predicted_text = ""
# and predicted_text will be changed to the current recording transcribed after 
# calling the stop_recording method
# 
# def stop_recording:
# pred_text = ....
# self.predicted_text = pred_text
# def GetPredictedText:
# return self.predicted_text

## SOLID PRINCIPLE 
# Every single method should have only one responsobility
##############################################################################################
# USER PERSPECTIVE
# import mevinWhisper

# def main():
#     whisp_instance = mevinWhiper.Initialize(model_name="medium.en", device_type="cuda")
    
#     # This method will be listening to the mic, until 
#     whisp_instance.start_recording(some_parameters...)
    
#     # will save the text in a field inside of the instance
#     whisp_instance.stop_recording()
    
#     text = whisper_instance.GetPredictedText()