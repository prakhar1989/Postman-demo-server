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

def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

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
    resp = { "origin": get_ip() , "delay": seconds }
    return jsonify(resp)

@debug_routes.route('/headers')
def headers():
    return jsonify({'headers': get_headers()})

@debug_routes.route('/get')
def get_request():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    resp = { "origin": get_ip() }
    resp["headers"] = get_headers()
    resp['url'] = request.url
    resp['args'] = request.args
    return jsonify(resp)
