import time

from flask import Response, request, jsonify, g, Blueprint
import utils.helper as helpers

# ----
# Debug Routes
# ----

debug_routes = Blueprint('debug_routes', __name__)


def get_headers():
    headers = dict(request.headers.items())
    return headers

@debug_routes.route('/')
def view_all_endpoints():
    return jsonify({"name": "hello world"})

@debug_routes.route('/status')
def view_status():
    resp = { "status": "ok", "timestamp": int(time.time()) }
    return jsonify(resp)

@debug_routes.route('/delay/<int:seconds>')
def delay(seconds):
    delay = min(seconds, 10) # max 10 seconds
    time.sleep(delay)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    resp = { "origin": ip , "delay": seconds }
    return jsonify(resp)

@debug_routes.route('/headers')
def headers():
    headers = get_headers()
    return jsonify({'headers': headers})
