from steamcheck import app

@app.route('/')
def index():
    return "Hello I am working YAY!"


@app.route('/user/<name>')
def user_map(name=None):
    pass