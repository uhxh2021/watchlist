import os, sys, click
from flask import Flask
from flask import url_for, render_template
from flask_sqlalchemy import SQLAlchemy

WIN=sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path. \
    join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
    

@app.route('/')
def hello():
    return '<h1>helloflask,watchlist project</h1> \
        <img src="http://helloflask.com/totoro.gif">'

@app.route('/test')
def test_url_for():
    a = url_for('test_url_for', num=2)
    # return '<h3>%s</h3>' % a
    return f"<h3>{a}</h3>"


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/index')
def index():

    movies = Movie.query.all()    
    return render_template('index.html', movies=movies)

@app.route('/base')
def base_page():
   
    return render_template('base.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.cli.command()
def forge():
    ''' Generate fake data'''
    db.create_all()
    name = 'uhxh-db'
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
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

