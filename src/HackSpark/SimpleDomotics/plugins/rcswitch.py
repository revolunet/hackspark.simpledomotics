from cytpes import cdll

LIB = None

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
        LIB.init_tansmitter(transmit_gpio)
