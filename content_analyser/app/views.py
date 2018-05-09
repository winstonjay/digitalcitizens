# -*- coding: utf-8 -*-
'''
Here we handle the template veiws.
'''
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Markup
)

from app import app

idx = 0

@app.route('/')
def index():
    "This is returning our home page"
    return render_template("index.html", message="hello")

@app.route('/page/<int:post_id>',  methods=['GET'])
def page(post_id):
    if post_id < 0 or post_id >= len(app.config['content']):
        return "404 page not found 💩. Wrong post id.", 404
    item = app.config['content'][post_id]
    text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] = Markup(text)
    return render_template("page.html", post_id=post_id, data=item, codes=app.config['book'])

def construct_row(r):
    return ", ".join("1" if k in r else "0" for k in keys)

@app.route('/submit_item', methods=['POST'])
def add_item():
    r = request.form
    print(r)
    app.config['db'].set(list(r.keys()))
    print(app.config['db'].data)
    return redirect("/page/%d" % len(app.config['db']))

# handle 404 errors.
@app.errorhandler(404)
def page_not_found(e):
    return "404 page not found 💩", 404