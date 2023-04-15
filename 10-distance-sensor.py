import time
from time import ticks_ms, ticks_us, sleep
from machine import Pin
    
class DistanceSensor:
    """
    Represents a HC-SR04 ultrasonic distance sensor.
    :param int echo:
        The pin that the ECHO pin is connected to.
    :param int trigger:
        The pin that the TRIG pin is connected to. 
    :param float max_distance:
        The :attr:`value` attribute reports a normalized value between 0 (too
        close to measure) and 1 (maximum distance). This parameter specifies
        the maximum distance expected in meters. This defaults to 1.
    """
    def __init__(self, echo, trigger, max_distance=1):
        self._pin_nums = (echo, trigger)
        self._max_distance = max_distance
        self._echo = Pin(echo, mode=Pin.IN, pull=Pin.PULL_DOWN)
        self._trigger = Pin(trigger, mode=Pin.OUT, value=0)
        self._last_distance = 0
        
    def _read(self):
        echo_on = None
        echo_off = None
        timed_out = False
        
        self._trigger.off()
        sleep(0.000005)
        self._trigger.on()
        sleep(0.00001)
        self._trigger.off()

        # If an echo isn't measured in 100 milliseconds, it should
        # be considered out of range. The maximum length of the
        # echo is 38 milliseconds but it's not known how long the
        # transmission takes after the trigger
        stop = ticks_ms() + 1000
        while echo_off is None and not timed_out:
            if self._echo.value() == 1 and echo_on is None:
                echo_on = ticks_us()
            if echo_on is not None and self._echo.value() == 0:
                echo_off = ticks_us()
            if ticks_ms() > stop:
                timed_out = True
            
        if echo_off is None or timed_out:
           # return self._last_distance
            return None
        else:
            distance = ((echo_off - echo_on) * 0.000343) / 2
            distance = min(distance, self._max_distance)
#              self._last_distance = distance
            return distance
    
    @property
    def value(self):
        """
        Returns a value between 0, indicating the reflector is either touching 
        the sensor or is sufficiently near that the sensor can’t tell the 
        difference, and 1, indicating the reflector is at or beyond the 
        specified max_distance. A return value of None indicates that the
        echo was not received before the timeout.
        """
        distance = self.distance
        return distance / self._max_distance if distance is not None else None
    
    @property
    def distance(self):
        """
        Returns the current distance measured by the sensor in meters. Note 
        that this property will have a value between 0 and max_distance.
        """
        return self._read()

    @property
    def max_distance(self):
        """
        Returns the maximum distance that the sensor will measure in metres.
        """
        return self._max_distance
    
# GLOBAL_VARIABLES
led = Pin(10, Pin.OUT)
ds = DistanceSensor(echo=5, trigger=4, max_distance=1)


while True:
    print(ds.value)
    time.sleep_ms(500)
      