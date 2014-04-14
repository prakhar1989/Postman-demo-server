# -*- coding: utf-8 -*-

"""
postmanbin.app
~~~~~~

This module provides the core postmanbin API for blogs and users.
"""

import time
import os
from sqlite3 import dbapi2 as sqlite3
import json

from flask import Flask, Response, request, jsonify, g, Blueprint, render_template
from flask.ext import restful
from werkzeug import check_password_hash, generate_password_hash

import utils.helper as helpers
from postmanbin.debug_routes import debug_routes

app = Flask(__name__)
api = restful.Api(app)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'postman_demo.db'),
    DEBUG=True
))

# register the debug_routes blueprint 
app.register_blueprint(debug_routes)

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

# --- 
# Restful API
# ---

class Blog(restful.Resource):
    # get /blog/posts all posts
    def get(self):
        db = get_db()
        cur = db.execute('select id, created_at, content from posts')
        posts = cur.fetchall()
        return [{'id': p[0], 'created_at': p[1], 'content': p[2]} for p in posts]

    # post /blog/posts
    def post(self):
        post_data = json.loads(request.data)
        access_token = request.args.get('token', '')
        user_id = request.args.get('user_id', '')
        db = get_db()

        if access_token and user_id:
            cur = db.execute('select * from users where token = (?) and id = (?)',
                             [access_token, user_id])
            user = cur.fetchone()
            if user:
                db.execute('insert into posts (content, created_at) values (?, ?)',
                           [post_data.get('post'), int(time.time())])
                db.commit()
                return {'message': "Post added successfully"}
        return {"message": "Invalid credentials"}

class BlogPost(restful.Resource):
    # get /blog/posts/:id - return the blog post
    def get(self, post_id):
        db = get_db()
        cur = db.execute('select id, created_at, content from posts where id = (?)',
                        [post_id])
        post = cur.fetchone()
        if not post:
            restful.abort(404, message="post doesn't exist")
        return {'id': post[0], 'created_at': post[1], 'content': post[2]}

    # put /blog/posts/:id - edit the blog post
    def put(self, post_id):
        db = get_db()
        post_data = json.loads(request.data)
        db.execute('update posts set content = (?) where id = (?)',
                   [post_data.get('post'), post_id])
        db.commit()
        return {'message': 'Post successfully updated'}, 201

    # delete /blog/posts/:id - delete the blog post
    def delete(self, post_id):
        db = get_db()
        db.execute('delete from posts where id = (?)', [post_id])
        db.commit()
        return jsonify({'message': 'Blog post deleted successfully'})

# get /blog/users
# post /blog/users
class UserList(restful.Resource):
    def get(self):
        db = get_db()
        cur = db.execute('select id, username, created_at, token from users')
        users = cur.fetchall()
        return [{'id': u[0], 'username': u[1],
                 'created_at': u[2]} for u in users]

    def post(self):
        db = get_db()
        post_data = json.loads(request.data)
        username, password = post_data.get('username'), post_data.get('password')
        pw_hash = generate_password_hash(password)
        db.execute('insert into users (username, pw_hash, created_at) values (?, ?, ?)',
                  [username, pw_hash, int(time.time())])
        db.commit()
        return {'message': "User created successfully"}

@app.route('/blog/users/<int:user_id>')
def user_detail(user_id):
    """ get /blog/users/:id - info about a user """
    db = get_db()
    cur = db.execute('select id, username, created_at, token from \
                     users where id = (?)', [user_id])
    user = cur.fetchone()
    if not user:
        restful.abort(404, message="user doesn't exist")
    return jsonify({'id': user[0], 'username': user[1],
                    'created_at': user[2], 'token': user[3]})

@app.route('/blog/users/tokens/', methods=["POST"])
def new_token():
    """ post /users/tokens - create a new token """
    db = get_db()
    post_data = json.loads(request.data)
    cur = db.execute('select pw_hash from users where username = (?)',
                    [post_data.get('username')])
    pw_hash = cur.fetchone()
    if pw_hash and check_password_hash(pw_hash[0], post_data.get('password')):
        token = helpers.generate_token()
        db.execute('update users set token = (?) where username = (?)',
                    [token, post_data.get('username')])
        db.commit()
        return jsonify({'token': token})
    else:
        restful.abort(401, message="username / password combination doesn't match")

@app.route('/blog/users/tokens/<token_id>', methods=["DELETE"])
def delete_token(token_id):
    """ delete /users/tokens/id - delete token """
    db = get_db()
    db.execute('update users set token = null where token = (?)', [token_id])
    db.commit()
    return jsonify({'message': 'Token deleted successfully'})


# Adding API resources
api.add_resource(Blog, '/blog/posts')
api.add_resource(BlogPost, '/blog/posts/<int:post_id>')
api.add_resource(UserList, '/blog/users/')


# Display documentation
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
