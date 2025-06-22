import os
from flask import Flask, render_template, request, redirect, url_for
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/search')
def search():
    query = request.args.get('q')
    google_search_results = []

    if query:
        # Perform internal blog search
        internal_posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).all()

        # Perform Google Custom Search
        GOOGLE_API_KEY = 'AIzaSyAMeIeyJqkzrf0Rj2ZNXE9SweOVJgbl07c'
        GOOGLE_CSE_ID = 'c1f7c4818189a4f94'
        search_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}&q={query}&num=1"
        
        try:
            response = requests.get(search_url)
            response.raise_for_status() # Raise an exception for HTTP errors
            search_data = response.json()
            if 'items' in search_data and search_data['items']:
                # Get the first result and add it to google_search_results
                first_result = search_data['items'][0]
                google_search_results.append({
                    'title': first_result.get('title'),
                    'link': first_result.get('link'),
                    'snippet': first_result.get('snippet')
                })
        except requests.exceptions.RequestException as e:
            print(f"Error during Google Custom Search API call: {e}")
            # Handle API error gracefully, e.g., log it and continue without Google results

    else:
        internal_posts = []

    return render_template('search.html', posts=internal_posts, query=query, google_search_results=google_search_results)

@app.route('/admin')
def admin():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin.html', posts=posts)

@app.route('/admin/new', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_post.html')

@app.route('/admin/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_post.html', post=post)

@app.route('/admin/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()