from app import app
from flask import render_template

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# There is no route for the posts page because when I tried that, I didn't show my posts. It took me to /posts.
# But Grahams code just had "href='/post/list'" and that worked.