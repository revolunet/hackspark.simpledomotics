from os import system as call
from bottle import view, redirect

from HackSpark.SimpleDomotics import app, plugin_manager

@app.route('/switch/<switch_num>/<action>')
@app.route('/switch/<switch_num>')
def switch(switch_num, action='toggle'):
    switch_val = app.config["switches"][int(switch_num)]
    if not "state" in switch_val:
        switch_val["state"] = 0
    
    if action == "toggle":
        action = switch_val["state"] and "off" or "on"
    stype = switch_val.get("type")
    
    if stype == "command":
        call(switch_val["commands"][action])
        
        if action == "on":
            switch_val["state"] = 1
        if action == "off":
            switch_val["state"] = 0
            
    elif stype == "plugin":
        plugin = plugin_manager.get_plugin(switch_val["plugin"])
        plugin.switch(switch_val, action=action)
    
    redirect("/")
