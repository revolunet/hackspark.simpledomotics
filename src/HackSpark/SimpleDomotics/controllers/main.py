from bottle import view, redirect, static_file
import pkg_resources
from HackSpark.SimpleDomotics import app
from HackSpark.SimpleDomotics.plugins_manager import PLUGIN_MODULES

from importlib import import_module

@app.route('/')
@view('main')
def index():
    plugin_infos = list()
    for plugin_name, info in app.config.get("plugins", dict()).items():
        #pg_mod = __import__("HackSpark.SimpleDomotics.plugins.%s" % plugin_name)
        pg_mod = import_module("HackSpark.SimpleDomotics.plugins.%s" % plugin_name)
        pg = dict(name=plugin_name,
                  title=info.get('title', plugin_name.capitalize()),
                  items=list())
        print repr(pg_mod)
        print dir(pg_mod)
        if "sensors" in info:          
            for item in info["sensors"]:
                pg["items"].append(pg_mod.get_value(plugin_conf=info, **item))
        
        plugin_infos.append(pg)
        
    return dict(switches=app.config.get("switches", None),
                cameras=app.config.get("cameras", None),
                plugin_infos=plugin_infos)
                
@app.route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root=pkg_resources.resource_filename('HackSpark.SimpleDomotics', 'static/'))
