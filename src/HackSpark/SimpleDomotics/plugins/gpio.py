import os
from pyjon.events import EventDispatcher

class Manager(object):
    __metaclass__ = EventDispatcher

MANAGER = Manager()

emit_event = MANAGER.emit_event
add_listener = MANAGER.add_listener

class GPIO(object):
    """ Class based on Gadgets GPIO class.
    """
    _path = '/sys/class/gpio'
    _export_path = '/sys/class/gpio/export'
    _gpio_path = '/sys/class/gpio/gpio{0}'
    _base_path = '/sys/class/gpio/gpio{0}/{1}'

    def __init__(self, pin, direction='in', pullup=False):
        self._export = pin
        self._direction = direction
        self._pullup = pullup
        self._file_cache = None
        self._initialize_pin()
        self._value = 0
        self._status = False
        

    @property
    def status(self):
        return self._status

    @property
    def _file(self):
        """
        Returns the sysfs file object that is the
        Linux interface to the gpio pin.
        """
        if self._file_cache is None:
            self._file_cache = self._open_file()
        return self._file_cache

    def on(self):
        """
        Sets the gpio pin high.
        """
        if self._direction == 'out':
            self._value = 1
            self._file.write('1')
            self._file.flush()
            self._status = True

    def off(self):
        """
        Sets the gpio pin low.
        """
        if self._direction == 'out':
            self._value = 0
            self._file.write('0')
            self._file.flush()
            self._status = False

    def value(self):
        """
        Get the value of the gpio pin.
        """
        if self._direction == 'out':
            value = self._value
        else:
            value = int(self._file.read())
            self._file.seek(0)
        return value

    def close(self):
        """
        Closes the file that GPIO uses to set/read the
        value of the pin.
        """
        self._file.close()

    def _open_file(self):
        """
        Opens the sysfs gpio interface file that sets
        the pin high or low.
        """
        value_path = self._base_path.format(self._export, 'value')
        if self._direction == 'out':
            buf = open(value_path, 'w')
            buf.write('0')
            buf.flush()
        else:
            buf = open(value_path, 'r')
        return buf

    def _write_to_file(self, path, value):
        """
        writes the given value to a sysfs
        path
        """
        print repr(path), repr(value)
        with open(path, 'w') as buf:
            buf.write(value)

    @property
    def home_dir(self):
        """
        After a gpio pin is enabled the sysfs interface for the
        pin is created as a directory.  This property creates
        the path to that directory.
        """
        return self._gpio_path.format(self._export)
        
    def _initialize_pin(self):
        """
        determine whether to use the old sysfs
        to set the pin mode or to use the new
        device tree overlay
        """
        if not os.path.exists(self.home_dir):
            self._write_to_file(self._export_path, str(self._export))
        if not os.path.exists(self.home_dir):
            raise IOError(
                'failed gpio export: {0}'.format(
                    self.home_dir))
        path = self._base_path.format(self._export, 'direction')
        self._write_to_file(path, self._direction)


    def _device_tree_init(self):
        """
        """
        pass

GPIOS = dict()

def initialize(config):
    if "pins" in config:
        for pin, pin_conf in config["pins"].items():
            #print pin, direction
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
