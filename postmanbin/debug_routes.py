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

def get_dict(*keys, **extras):
    _keys = ('url', 'args', 'form', 'data', 'origin', 'status', 'headers',
             'files', 'json', 'timestamp', 'cookies')

    assert all(map(_keys.__contains__, keys))

    data = request.data
    form = request.form

    try:
        _json = json.loads(data)
    except ValueError:
        _json = None

    d = dict(
        url       = request.url,
        args      = request.args,
        form      = form,
        data      = helpers.json_safe(data),
        origin    = get_ip(),
        headers   = get_headers(),
        files     = get_files(),
        json      = _json,
        timestamp = int(time.time()),
        status    = "ok",
        cookies   = request.cookies
    )

    response_dict = dict()

    for k in keys:
        response_dict[k] = d[k]

    for e in extras:
        response_dict[e] = extras[e]

    return response_dict

@debug_routes.route('/')
def view_all_endpoints():
    return jsonify(hello="world")

@debug_routes.route('/status')
def view_status():
    return jsonify(get_dict("status", "timestamp"))

@debug_routes.route('/delay/<int:seconds>')
def delay(seconds):
    delay = min(seconds, 10) # max 10 seconds
    time.sleep(delay)
    return jsonify(get_dict('origin', delay=seconds))

@debug_routes.route('/headers')
def headers():
    return jsonify(get_dict('headers'))

@debug_routes.route('/get')
def get_request():
    return jsonify(get_dict('origin', 'headers', 'url', 'args'))

@debug_routes.route('/post', methods=["POST"])
def post_request():
    return jsonify(get_dict('form', 'data', 'json', 'files', 'args',
                            'url', 'headers', 'origin'))

# GET /cookies
@debug_routes.route('/cookies')
def cookies():
    return jsonify(get_dict('cookies'))

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
