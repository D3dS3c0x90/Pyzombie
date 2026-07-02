class ClockAndTime:
    def __init__(self, hour=0, minutes=0, seconds=0):
        self.hour = hour
        self.minutes = minutes
        self.seconds = seconds
    
class Timer:
    def __init__(self, seconds, fps):
        self.limit = int(seconds * float(fps))
        self.count = 0
        self.pressed = False
        self.hold = False
        
        """
        # How to use...
        
        1- uses for make a delay AFTER BUTTON CLICKED
        2- before the button clicked, start the delay for holding
        3- check from the pressed case, if pressed means that the hold knows that action happend
                so, it will start holding
        4- after the time passes based on the counter, the pressed and hold will be reseted
        5- that's it 

        """
    def delay(self):
        if self.pressed:
            self.hold = True
            self.count += 1
            if self.count >= self.limit:
                self.count = 0
                self.hold = False
                self.pressed = False