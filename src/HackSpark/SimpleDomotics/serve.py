from bottle import run
import yaml

from HackSpark.SimpleDomotics import app
from HackSpark.SimpleDomotics.controllers.auth import AuthMiddleware
from HackSpark.SimpleDomotics.plugins_manager import initialize_plugins

if __name__ == "__main__":
    with open('conf.yaml') as fp:
        app.config = yaml.load(fp)
        
    initialize_plugins(app.config)
        
    run(app=AuthMiddleware(app), host='0.0.0.0', port=8080, debug=True, server="paste")
