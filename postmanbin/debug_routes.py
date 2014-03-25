import time
import base64
import json

from flask import Response, request, jsonify, g, Blueprint, redirect, make_response
import utils.helper as helpers

# ----
# Debug Routes
# ----

debug_routes = Blueprint('debug_routes', __name__)

def get_files():
    files = dict()
    for k, v in request.files.items():
        files[k] = helpers.json_safe(v.read(), request.files[k].content_type)
    return files

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
    resp = { "origin": get_ip() }
    resp["headers"] = get_headers()
    resp['url'] = request.url
    resp['args'] = request.args
    return jsonify(resp)

@debug_routes.route('/post', methods=["POST"])
def post_request():
    resp = { "origin": get_ip() }

    data = request.data
    form = request.form

    try:
        _json = json.loads(data)
    except ValueError:
        _json = None

    resp["headers"] = get_headers()
    resp['url'] = request.url
    resp['args'] = request.args
    resp['files'] = get_files()
    resp['json'] = _json
    resp['form'] = form
    resp['data'] = helpers.json_safe(data)
    return jsonify(resp)

# GET /cookies
@debug_routes.route('/cookies')
def cookies():
    return jsonify(cookies=request.cookies)

# GET /cookies/set?name=value
@debug_routes.route('/cookies/set')
def set_cookie():
    if request.args:
        response = make_response(redirect('/cookies'))
        key, value = request.args.items()[0]
        response.set_cookie(key, value)
        return response
    return jsonify(message="No params found"), 404

# GET /cookies/delete?key=name
@debug_routes.route('/cookies/delete')
def delete_cookie():
    cookies = dict(request.cookies)
    if request.args:
        response = make_response(redirect('/cookies'))
        response.delete_cookie(key=request.args.get('key'))
        return response
    return jsonify(message="No key found"), 404
