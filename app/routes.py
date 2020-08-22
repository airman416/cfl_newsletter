from app import app
from flask import render_template

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
            'body': 'First post on the new CFL Newsletter website!',
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