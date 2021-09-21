from flask import Flask
from flask import url_for


app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>helloflask,watchlist project</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/test')
def test_url_for():
    a = url_for('test_url_for', num=2)
    return '<h3>%s</h3>' % a