from bottle import route, run, view, default_app, redirect, auth_basic
from bottle import static_file
import yaml
    

if __name__ == "__main__":
    with open('conf.yaml') as fp:
        app.config = yaml.load(fp)
        
    run(app=AuthMiddleware(app), host='0.0.0.0', port=8080, debug=True, server="paste")
