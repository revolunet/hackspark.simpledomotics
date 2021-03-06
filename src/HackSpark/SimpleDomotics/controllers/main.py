from bottle import view, redirect, static_file
import pkg_resources
from HackSpark.SimpleDomotics import app, plugin_manager
from HackSpark.SimpleDomotics.plugin_manager import PLUGINS_CONFIGS, get_plugin

from importlib import import_module

@app.route('/')
@view('main')
def index():
    plugin_infos = list()
        
    for plugin_name, info in PLUGINS_CONFIGS.items():
        pg_mod = get_plugin(plugin_name)
        pg = dict(name=plugin_name,
                  title=info.get('title', plugin_name.capitalize()),
                  items=list())
                  
        if "sensors" in info:
            for item in info["sensors"]:
                pg["items"].append(pg_mod.get_value(plugin_conf=info, **item))
        
        plugin_infos.append(pg)
    
    switches = app.config.get("switches", None)
    # let's update switch states
    if switches is not None:
        for switch_val in switches:
            stype = switch_val.get("type")
            if stype == 'plugin':
                plugin = plugin_manager.get_plugin(switch_val["plugin"])
                print plugin
                if hasattr(plugin, "get_value"):
                    switch_val["state"] = plugin.get_value(switch_val)
        
    return dict(switches=switches,
                cameras=app.config.get("cameras", None),
                plugin_infos=plugin_infos)
                
@app.route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root=pkg_resources.resource_filename('HackSpark.SimpleDomotics', 'static/'))
