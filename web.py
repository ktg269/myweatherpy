# web.py

from flask import Flask, render_template

app = Flask(__name__)

#
# GET /
#

@app.route('/')
def index():
    print("VISITING THE START PAGE")
    return 


@app.route('/profile/<int:post_id>')
def show_post(post_id):
    return "<h2>Post ID is %s<h2>" % post_id

if __name__ == '__main__':
    app.run(debug=True)