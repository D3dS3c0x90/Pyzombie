class ClockAndTime:
    def __init__(self, hour=0, minutes=0, seconds=0):
        self.hour = hour
        self.minutes = minutes
        self.seconds = seconds
    
class Timer:
    def __init__(self, seconds, fps):
        self.limit = seconds * fps
        self.count = 0
        self.pressed = False
        
    def delay(self):
        self.count += 1
        if self.count >= self.limit:
            self.count = 0
            return True
        return False