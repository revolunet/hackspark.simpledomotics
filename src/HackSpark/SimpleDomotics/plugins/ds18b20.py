

def initialize(config):
    return


def get_value(plugin_conf, chip_id=None, name=None):
    w1  ="/sys/bus/w1/devices/%s/w1_slave" % chip_id
    if name is None:
        name = chip_id
        
    raw = open(w1, "r").read()
    
    value = float(raw.split("t=")[-1])/1000
    if "format" in plugin_conf:
        value = eval(plugin_conf["format"])
    
    return dict(name = name,
                value = value)
