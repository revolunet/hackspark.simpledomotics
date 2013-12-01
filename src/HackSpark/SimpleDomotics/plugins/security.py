""" Security is an alarm providing bare-bone features for a home security system
Basically providing "arm", "disarm" and events.

Events are in various categories :
- Open (door, window, etc)
- Movement
- Etc.

Events will be thrown by outside modules, based on configuration events.

This plugin supports outbound events.

Launching "alert" mode immediately after event of waiting for a delay has to
be decided.
"""

from pyjon.utils import Singleton
from pyjon.events import EventDispatcher

class SecurityEvents(object):
    __metaclass__ = EventDispatcher

class SecuritySystem(object):
    __metaclass__ = Singleton
    
    def __init__(self):
        self._events = SecurityEvents()
        self._values = dict()
        self._armed = False
        self._alert = False
        self.emit_event = self._events.emit_event
        self.add_listener = self._events.add_listener
    
    def set(self, key, value):
        self._values[key] = value
        
    def get(self, key, value=None):
        return self._values.get(key, value)
        
    def start_alert(self):
        self._alert = True
        self.emit_event("alert_started")
        
    def end_alert(self):
        self._alert = False
        self.emit_event("alert_finished")
        
    def arm(self):
        self._armed = True
        self.emit_event("armed")
        
    def disarm(self):
        self._armed = False
        self.emit_event("disarmed")
        if self._alert:
            self.end_alert()
            
    def is_armed(self):
        return self._armed
        
    
add_listener = SecuritySystem().add_listener
emit_event = SecuritySystem().emit_event
arm = SecuritySystem().arm
disarm = SecuritySystem().disarm
is_armed = SecuritySystem().is_armed
start_alert = SecuritySystem().start_alert
end_alert = SecuritySystem().end_alert

def initialize(config):
    return
    
def switch(switch_config, action="on"):
    if action == "on":
        action = 1
    elif action == "off":
        action = 0
    
    """t = threading.Thread(target=LIB.transmit_switch, args=(
                            str(switch_config["system_code"]),
                            int(switch_config["unit_code"]),
                            int(action),))
    t.start()"""
    
    if action:
        arm()
    else:
        disarm()
        
    switch_config["state"] = int(action)

def get_value(switch_config):
    print is_armed()
    return int(is_armed())
    
def receive():
    """ This dunction is called very often, like a heartbeat.
    """
    pass
