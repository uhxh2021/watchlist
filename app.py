from flask import Flask
from flask import url_for, render_template


app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>helloflask,watchlist project</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/test')
def test_url_for():
    a = url_for('test_url_for', num=2)
    # return '<h3>%s</h3>' % a
    return f"<h3>{a}</h3>"

@app.route('/index')
def index():
    return render_template('index.html', name=name, movies=movies)


name = 'Grey Li *uhxh*'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]