from bottle import route, run, view, default_app, redirect, auth_basic
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
    

class AuthMiddleware(object):

    def __init__(self, wrap_app):
        self.wrap_app = wrap_app

    def __call__(self, environ, start_response):
        if not self.authorized(environ.get('HTTP_AUTHORIZATION')):
            # Essentially self.auth_required is a WSGI application
            # that only knows how to respond with 401...
            return self.auth_required(environ, start_response)
        # But if everything is okay, then pass everything through
        # to the application we are wrapping...
        return self.wrap_app(environ, start_response)

    def authorized(self, auth_header):
        if not auth_header:
            # If they didn't give a header, they better login...
            return False
        # .split(None, 1) means split in two parts on whitespace:
        auth_type, encoded_info = auth_header.split(None, 1)
        assert auth_type.lower() == 'basic'
        unencoded_info = encoded_info.decode('base64')
        username, password = unencoded_info.split(':', 1)
        return self.check_password(username, password)

    def check_password(self, username, password):
        # Not very high security authentication...
        # return username == password
        
        if 'users' not in app.config:
            return True
            
        if username in app.config['users']:
            if password == app.config['users'][username]:
                return True
        
        return False

    def auth_required(self, environ, start_response):
        start_response('401 Authentication Required',
            [('Content-type', 'text/html'),
             ('WWW-Authenticate', 'Basic realm="this realm"')])
        return ["""
        <html>
         <head><title>Authentication Required</title></head>
         <body>
          <h1>Authentication Required</h1>
          If you can't get in, then stay out.
         </body>
        </html>"""]

if __name__ == "__main__":
    with open('conf.yaml') as fp:
        app.config = yaml.load(fp)
        
    run(app=AuthMiddleware(app), host='0.0.0.0', port=8080, debug=True, server="paste")
