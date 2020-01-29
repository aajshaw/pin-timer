from gpiozero import LED as Pin
from datetime import time
from datetime import datetime as dt
from time import sleep

# Set a GPIO to 'On' or 'Off' on a schedule defined in a dictionary
#
# What is actually being controlled does not have to be an LED, it can be
# anything as the GPIO is just being set to on (high) or off (low). The
# program was developed to control a relay that operated a set of lights
# for a fish tank

class Pin_Timer:
    def __init__(self, pin, times):
        # Get a local copy of the on/off times and sort the times into ascending
        # order so that they can checked by interval
        self.times = times
        self.times_keys = sorted(times.keys())
        self.times_length = len(self.times_keys)

        # Initialise the pin to off/low
        self.pin = Pin(pin)
        self.pin.off()

    def run(self):
        # Loop forever checking the current system time against the sorted list
        # of on/off periods
        while True:
            now = dt.now().time()
            for ndx, when in enumerate(self.times_keys):
                next_when = self.times_keys[(ndx + 1) % self.times_length]
                # When the correct period is found set the pin to on or off
                # depending on the state required by the start of the period
                if (next_when < when and now >= when) or (next_when >= when and now >= when and now < next_when):
                    if self.times[self.times_keys[ndx]] == 'On':
                        self.pin.on()
                    else:
                        self.pin.off()
                    break
            sleep(10)

# Times represented as hours, minutes, seconds
times = { time( 9, 0, 0) : 'On',  # Turn on at 9am
          time(11, 0, 0) : 'Off', # Turn off at 11am
          time(12, 29, 0) : 'On',  # Turn on at 12:29pm
          time(12, 31, 0) : 'Off',  # Turn off at 12:31pm
          time(12, 32, 0) : 'On',  # Turn on at 12:32pm
          time(12, 33, 0) : 'Off'  # Turn off at 12:33pm and stay off until 9am next day
        }

# Get an instance of a Pin_Timer for pin 0 (zero) and then run it
# Change the zero to another GPIO pin number to use that instead
pin = Pin_Timer(0, times)
pin.run()
