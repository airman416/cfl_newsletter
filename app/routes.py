from app import app, db
from flask import render_template, request, url_for, redirect, flash, session

from app.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

query = Post.query.distinct(Post.topic).group_by(Post.topic).all()
topics = []
    
for post in query:
    print(post)
    if post.topic in topics:
        continue
    else:
        topics.append(post.topic)

@app.route('/')
@app.route('/index')
def index():
    contacts = [
        {
            'name': 'GitHub',
            'url': 'https://github.com/KIST-CFL'
        }
    ]
    
    posts = Post.query.order_by(Post.timestamp.desc()).limit(8).all()
        
    return render_template('index.html', posts=posts, contacts=contacts, topics=topics)


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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, summary=form.summary.data, body=form.post.data, user_id=current_user.username, topic=form.topic.data)
        db.session.add(post)
        db.session.commit()
        flash("Live post!")
        return redirect(url_for('index'))
    else:
        print("INVALID")
        print(form.title.data, form.summary.data, form.post.data, current_user.username, form.topic.data)
        print(form.post.errors)
    return render_template('add.html', form=form)


@app.route('/<topic>')
def topic(topic):
    contacts = [
        {
            'name': 'GitHub',
            'url': 'https://github.com/KIST-CFL'
        }
    ]
    
    posts = Post.query.order_by(Post.timestamp.desc()).filter_by(topic=topic).all()
    
    return render_template('topic.html', posts=posts, contacts=contacts, topics=topics, topic=topic)


@app.route('/post/<id>')
def id(id):
    post = Post.query.filter_by(id=id).first_or_404()
    
    return render_template('post.html', post=post)


@app.route('/delete/<id>')
@login_required
def delete(id):
    post = Post.query.filter_by(id=id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))
    
    