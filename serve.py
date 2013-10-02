from bottle import route, run, view
from bottle import static_file

@route('/hello')
@route('/hello/<name>')
@view('hello')
def hello(name='World'):
    return dict(name=name)
    
@route('/')
@view('main')
def index():
    return dict()

@route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root='static/')

run(host='0.0.0.0', port=8080, debug=True)
