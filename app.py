import time
import os
from sqlite3 import dbapi2 as sqlite3

from flask import Flask, Response, request, jsonify, g
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'postman_demo.db'),
    DEBUG=True,
    SECRET_KEY="supersecretkey",
    USERNAME="admin",
    PASSWORD="password"
))

# ----
# DB Operations
# ----

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('utils/blogschema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    # set a sqlite_db attribute on the flask global object
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# ----
# Routes
# ----

@app.route('/')
def view_all_endpoints():
    return jsonify({"name": "hello world"})

@app.route('/status')
def view_status():
    resp = { "status": "ok", "timestamp": int(time.time()) }
    return jsonify(resp)

@app.route('/delay/<int:seconds>')
def delay(seconds):
    delay = min(seconds, 10) # max 10 seconds
    time.sleep(delay)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    resp = { "origin": ip , "delay": seconds }
    return jsonify(resp)


# --- 
# Restful API
# ---

class Blog(restful.Resource):
    # get /blog/posts all posts
    def get(self):
        db = get_db()
        cur = db.execute('select id, title, content from posts')
        posts = cur.fetchall()
        return [{'id': p[0], 'title': p[1], 'content': p[2]} for p in posts]

    def post(self):
        db = get_db()
        db.execute('insert into posts (title, content) values (?, ?)',
                  [request.form['title'], request.form['content']])
        db.commit()
        return {'title': request.form['title'],
                'content': request.form['content']}, 201

class BlogPost(restful.Resource):
    def get(self, post_id):
        db = get_db()
        cur = db.execute('select * from posts where id = (?)', [post_id])
        post = cur.fetchone()
        print post
        return {'id': post[0], 'title': post[1], 'content': post[2]}

    def put(self, post_id):
        db = get_db()
        db.execute('update from posts where id = (?)', [post_id])
        db.commit()
        return {'status': 'success'}, 201

    def delete(self, post_id):
        db = get_db()
        db.execute('delete from posts where id = (?)', [post_id])
        db.commit()
        return "", 204

api.add_resource(Blog, '/blog/posts', '/blog/posts/')
api.add_resource(BlogPost, '/blog/posts/<int:post_id>')

if __name__ == "__main__":
    app.run(debug=True)
