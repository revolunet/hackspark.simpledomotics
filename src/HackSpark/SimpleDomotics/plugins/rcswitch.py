from ctypes import cdll
import threading

LIB = None

def receive():
    val = LIB.get_received_value()
    if val != -1:
        print val

def initialize(config):
    global LIB
    stdc = cdll.LoadLibrary("libc.so.6")
    stdcpp = cdll.LoadLibrary("libstdc++.so.6")
    LIB = cdll.LoadLibrary("librcswitch.so")
    
    receive_gpio = None
    transmit_gpio = None
    if "gpios" in config:
        receive_gpio = config["gpios"].get("receive")
        transmit_gpio = config["gpios"].get("transmit")
    
    LIB.initialize_rcswitch()
    
    if receive_gpio is not None:
        LIB.init_receiver(receive_gpio)
    
    if transmit_gpio is not None:
        LIB.init_transmitter(transmit_gpio)
        
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
    
    LIB.transmit_switch(str(switch_config["system_code"]),
                        int(switch_config["unit_code"]),
                        int(action))
    switch_config["state"] = int(action)
    
