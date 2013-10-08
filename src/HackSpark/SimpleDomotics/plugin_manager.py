
PLUGINS = dict()

def initialize_plugins(config):
    # warning, this is not thread safe for now.
    for plugin_name, info in app.config.get("plugins", dict()).items():
        #pg_mod = __import__("HackSpark.SimpleDomotics.plugins.%s" % plugin_name)
        try:
            pg_mod = import_module("HackSpark.SimpleDomotics.plugins.%s" % plugin_name)
        except ImportError:
            print "Can't import module %s, skipping." % plugin_name
            continue
        
        pg_mod.initialize(info)
        PLUGINS[plugin_name] = pg_mod
