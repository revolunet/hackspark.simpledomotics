from bottle import view, redirect, static_file
import pkg_resources
from HackSpark.SimpleDomotics import app

@app.route('/')
@view('main')
def index():
    switches = None
    if "switches" in app.config:
        switches = app.config["switches"]
        
    return dict(switches=app.config.get("switches", None),
                cameras=app.config.get("cameras", None))
                
@app.route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root=pkg_resources.resource_filename('HackSpark.SimpleDomotics', 'static/'))
