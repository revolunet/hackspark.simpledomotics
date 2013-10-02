from bottle import route, run, view, default_app, redirect
from bottle import static_file
import yaml

from os import system as call

app = default_app()

@app.route('/hello')
@app.route('/hello/<name>')
@view('hello')
def hello(name='World'):
    return dict(name=name)
    
@app.route('/')
@view('main')
def index():
    switches = None
    if "switches" in app.config:
        switches = app.config["switches"]
        
    return dict(switches=app.config.get("switches", None),
                cameras=app.config.get("cameras", None))
    
@app.route('/switch/<switch_num>/<action>')
@app.route('/switch/<switch_num>')
def switch(switch_num, action='toggle'):
    switch_val = app.config["switches"][int(switch_num)]
    if not "state" in switch_val:
        switch_val["state"] = 0
    
    if action == "toggle":
        action = switch_val["state"] and "off" or "on"
    
    if switch_val.get("type", "command"):
        print switch_val["commands"]
        call(switch_val["commands"][action])
        
        if action == "on":
            switch_val["state"] = 1
        if action == "off":
            switch_val["state"] = 0
        
        print switch_val["state"]
    
    redirect("/")

@app.route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root='static/')

if __name__ == "__main__":
    with open('conf.yaml') as fp:
        app.config = yaml.load(fp)
    run(host='0.0.0.0', port=8080, debug=True)
