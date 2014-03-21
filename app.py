import time

from flask import Flask, Response, request, jsonify

app = Flask(__name__)


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
