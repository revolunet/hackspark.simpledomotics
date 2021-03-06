from HackSpark.SimpleDomotics import app

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
