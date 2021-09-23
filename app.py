import os, sys, click, time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, url_for, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

WIN=sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path. \
    join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
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

@app.route('/testurl')
def test_url():
    flash('三秒后跳转到首页')
    time.sleep(3)
    return redirect(url_for('index'))


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/index', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('输入错误')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item 创建成功！')
        return redirect(url_for('index'))
    
    movies = Movie.query.all()    
    return render_template('index.html', movies=movies)

@app.route('/base')
def base_page():
   
    return render_template('base.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    login_manager.login_view = 'login'
    login_manager.login_message = '请先登录再操作！'
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('输入错误')
            return redirect(url_for('edit', movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
@login_required

def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    login_manager.login_view = 'login'
    login_manager.login_message = '请先登录再操作！'
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('输入错误！')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功！')
            return redirect(url_for('index'))
        flash('错误的用户名或密码！')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出！')
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('输入错误！')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')



@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    '''Initialize the database.'''
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized db.')

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

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    '''Create user.'''
    db.create_all()
    
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Create Done.')
    
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

