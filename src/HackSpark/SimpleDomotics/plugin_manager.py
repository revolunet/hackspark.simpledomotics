import threading
from HackSpark.SimpleDomotics import app

from importlib import import_module
from threading import Thread
import time

PLUGINS = dict()
PLUGINS_CONFIGS = dict()

def input_round_robin():
    while True:
        for plugin in PLUGINS.values():
            if hasattr(plugin, "receive"):
                plugin.receive()
        time.sleep(.0005) # fast enough sleep to avoid eating all cpu

def create_plugin_event_listener(code, plugin_name):
    def plugin_event(**kwargs):
        try:
            kwargs.update(dict(PLUGINS=PLUGINS))
            exec code in kwargs
        except Exception, e:
            print "GOT AN EXCEPTION RUNNING '%s'/'%s' EVENT:\n\t%s" % (plugin_name, code, e)
            
    return plugin_event

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
        PLUGINS_CONFIGS[plugin_name] = info
        
        # now, let's prepare events
        if hasattr(pg_mod, "add_listener"):
            for event, listeners in info.get("events", dict()).items():
                if isinstance(listeners, basestring):
                    listeners = [listeners]
                for listener in listeners:
                    pg_mod.add_listener(event, create_plugin_event_listener(listener, plugin_name))
    
    thread = Thread(target = input_round_robin)
    thread.start()
    
def get_plugin(pname):
    return PLUGINS.get(pname)
