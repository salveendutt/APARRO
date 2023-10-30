import waiter as wt
import transcriber as tr

class Restaurant:
    def __init__(self):
        self.waiter = None
        self.transcriber = None
    
    def Initialize(self):
        self.waiter = wt.Waiter()
        self.transcriber = tr.Transcriber()