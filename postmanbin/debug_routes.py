import time
import base64
import json

from flask import Response, request, jsonify, g, Blueprint
import utils.helper as helpers

# ----
# Debug Routes
# ----

debug_routes = Blueprint('debug_routes', __name__)

def json_safe(string, content_type='application/octet-stream'):
    """Returns JSON-safe version of `string`.

    If `string` is a Unicode string or a valid UTF-8, it is returned unmodified,
    as it can safely be encoded to JSON string.

    If `string` contains raw/binary data, it is Base64-encoded, formatted and
    returned according to "data" URL scheme (RFC2397). Since JSON is not
    suitable for binary data, some additional encoding was necessary; "data"
    URL scheme was chosen for its simplicity.

    Courtesy: httpbin
    """

    try:
        _encoded = json.dumps(string)
        return string
    except ValueError:
        return ''.join(['data:%s;base64,' % content_type,
                        base64.b64encode(string)])

def get_files():
    files = dict()
    for k, v in request.files.items():
        files[k] = json_safe(v.read(), request.files[k].content_type)
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
    resp['data'] = json_safe(data)
    return jsonify(resp)

@debug_routes.route('/cookies')
def cookies():
    return jsonify(cookies=request.cookies)
