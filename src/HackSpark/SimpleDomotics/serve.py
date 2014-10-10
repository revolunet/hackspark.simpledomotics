from bottle import run
import yaml

from HackSpark.SimpleDomotics import app
from HackSpark.SimpleDomotics.controllers.auth import AuthMiddleware
from HackSpark.SimpleDomotics.plugin_manager import initialize_plugins

def serve_app():
    import argparse
    

    parser = argparse.ArgumentParser(description='Start a SimpleDomotics server.')
    parser.add_argument('--config', '-c', dest="config_file", default="conf.yaml",
                        help='specify a config file (default: conf.yaml)')
    parser.add_argument('--port', '-p', default=8080, type=int, dest="port",
                        help='specify the HTTP server port  (default: 8080)')
    parser.add_argument('--host', default="0.0.0.0", type=str, dest="host",
                        help='specify the HTTP server host  (default: 0.0.0.0)')
    parser.add_argument('--debug', default=False, action="store_true", dest="debug",
                        help='start the server in debug mode')
    args = parser.parse_args()         
                        
    with open(args.config_file) as fp:
        app.config = yaml.load(fp)
        
    initialize_plugins(app.config)

    run(app=AuthMiddleware(app), host=args.host, port=args.port, debug=args.debug, server="paste")

if __name__ == "__main__":
    serve_app()
