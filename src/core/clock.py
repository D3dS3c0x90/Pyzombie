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
        Cooldown timer that prevents rapid button toggling.

        1. Set pressed = True when the action triggers.
        2. The timer starts counting (hold = True).
        3. Once count >= limit, both pressed and hold reset to False.
        4. Check hold before allowing the next action.
        """
    def delay(self):
        if self.pressed:
            self.hold = True
            self.count += 1
            if self.count >= self.limit:
                self.count = 0
                self.hold = False
                self.pressed = False