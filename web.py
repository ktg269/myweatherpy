# web.py

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/profile/<int:post_id>')
def show_post(post_id):
    return "<h2>Post ID is %s<h2>" % post_id

if __name__ == '__main__':
    app.run(debug=True)