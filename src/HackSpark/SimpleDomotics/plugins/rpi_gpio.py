try:
    import RPi.GPIO as rGPIO
except ImportError:
    print "Unable to import RPi.GPIO, please check its installation."
    print "Please try to run 'easy_install -UZ RPi.GPIO' or running with sudo."
    raise

GPIOS = dict()

class GPIO(object):
    def __init__(self, pin, direction='out', pullup=False, pulldown=False,
                 frequency=200):
        self._export = int(pin)
        self._direction = direction
        self._pullup = pullup
        self._pulldown = pulldown
        self._frequency = frequency
        self._initialize_pin()
        self._value = 0
        self._status = False
        self._pwm = None
        
    def set_pwm(self, value):
        assert 0.0 <= value <= 100.0, "PWM value should be between 0 and 100"
        
        if self._pwm is None:
            self._pwm = rGPIO.PWM(self._export, self._frequency)
            self._pwm.start(value)
        else:
            self._pwm.ChangeDutyCycle(value)
    
    def stop_pwm(self):
        if self._pwm is not None:
            self._pwm.stop()
            self._pwm = None
    
    def _initialize_pin(self):
        pupd = rGPIO.PUD_OFF
        if self._pullup:
            pupd = rGPIO.PUD_UP
        if self._pulldown:
            pupd = rGPIO.PUD_DOWN
        
        if self._direction == 'in':
            direction = rGPIO.IN
        if self._direction == 'out':
            direction = rGPIO.OUT
            
        rGPIO.setup(self._export, direction, pull_up_down=pupd)
    
    def on(self):
        """
        Sets the gpio pin high.
        """
        if self._direction == 'out':
            self._value = 1
            rGPIO.output(self._export, 1)
            self._status = True
            

    def off(self):
        """
        Sets the gpio pin low.
        """
        if self._direction == 'out':
            self._value = 0
            rGPIO.output(self._export, 0)
            self._status = False

    def value(self):
        """
        Get the value of the gpio pin.
        """
        if self._direction == 'out':
            value = self._value
        else:
            value = rGPIO.input(self._export)
        return value
        

def initialize(config):
    rGPIO.setmode(rGPIO.BCM)
    if "pins" in config:
        for pin, pin_conf in config["pins"].items():
            if isinstance(pin_conf, basestring):
                direction = pin_conf
                default = 'off'
            else:
                direction = pin_conf.get('direction', 'out')
                default = pin_conf.get('default', 'off')

            GPIOS[pin] = GPIO(pin, direction=direction)
            if default == 'on':
                GPIOS[pin].on()

def get_value(switch_config):
    return GPIOS[int(switch_config["pin"])].value()

def switch(switch_config, action="on"):
    if action == "on":
        action = 1
        GPIOS[int(switch_config["pin"])].on()
    elif action == "off":
        action = 0
        GPIOS[int(switch_config["pin"])].off()

    switch_config["state"] = int(action)
