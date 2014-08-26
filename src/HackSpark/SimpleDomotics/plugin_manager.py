import threading
from HackSpark.SimpleDomotics import app

from importlib import import_module
from threading import Thread
import time
import sys

PLUGINS = dict()
PLUGINS_CONFIGS = dict()

def input_round_robin():
    while True:
        for plugin in PLUGINS.values():
            if hasattr(plugin, "receive"):
                try:
                    plugin.receive()
                except Exception, e:
                    print "GOT AN EXCEPTION RUNNIN RECEIVE FOR %s" % (plugin_name)
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
    plugin_dict = app.config.get("plugins")
    if plugin_dict is None:
        plugin_dict = dict()
        
    if app.config.get("server", dict()).get("PYTHONPATH") is not None:
        for path in app.config["server"]["PYTHONPATH"]:
            sys.path.append(path)
        
    plugin_namespaces = ["HackSpark.SimpleDomotics.plugins",]
    if app.config.get("server", dict()).get("plugin_namespaces") is not None:
        plugin_namespaces.extend(
            app.config["server"]["plugin_namespaces"])        
        
    for plugin_name, info in plugin_dict.items():
        #pg_mod = __import__("HackSpark.SimpleDomotics.plugins.%s" % plugin_name)
        pg_mod = None
        
        p_err = list()
        for namespace in plugin_namespaces:
            try:
                pg_mod = import_module("%s.%s" % (namespace,plugin_name))
            except ImportError, e:
                p_err.append(e)
        if pg_mod is None:
            for err in p_err:
                print repr(err)
            raise ImportError("Can't import plugin %s." % plugin_name)
        
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
