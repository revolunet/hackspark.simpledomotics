import threading
from HackSpark.SimpleDomotics import app

from importlib import import_module
from threading import Thread

PLUGINS = dict()

def input_round_robin():
    while True:
        for plugin in PLUGINS.values():
            plugin.receive()
            

def initialize_plugins(config):
    # warning, this is not thread safe for now.
    for plugin_name, info in app.config.get("plugins", dict()).items():
        #pg_mod = __import__("HackSpark.SimpleDomotics.plugins.%s" % plugin_name)
        try:
            pg_mod = import_module("HackSpark.SimpleDomotics.plugins.%s" % plugin_name)
        except ImportError:
            raise
            #print "Can't import module %s, skipping." % plugin_name
            #continue
        
        pg_mod.initialize(info)
        PLUGINS[plugin_name] = pg_mod
    
    thread = Thread(target = input_round_robin)
    thread.start()
    
def get_plugin(pname):
    return PLUGINS.get(pname)
