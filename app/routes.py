from app import app
from flask import render_template, request, url_for, redirect

from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    contacts = [
        {
            'name': 'GitHub',
            'url': 'https://github.com/KIST-CFL'
        }
    ]
    
    posts = [
        {
            'author': {'username': 'airman416'},
            'date': '2020',
            'title': 'First Post',
            'body': 'First post on the new CFL Newsletter website! <br> This is some sample <code>code</code>',
            'topic': 'Python'
        }
    ]
    
    topics = []
    for post in posts:
        print(post)
        if post['topic'] in topics:
            continue
        else:
            topics.append(post['topic'])
        
    return render_template('index.html', title='Home', posts=posts, contacts=contacts, topics=topics)


# @app.route('/admin', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash("Login requested for user {}, remember_me={}".format(
#             form.username.data, form.remember_me.data
#         ))
#         return redirect(url_for('index'))
#     return render_template('login.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
