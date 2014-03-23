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

if __name__ == "__main__":
    app.run(debug=True)
