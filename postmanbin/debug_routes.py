# -*- coding: utf-8 -*-

"""
postmanbin.debug
~~~~~~

This module provides the debug routes for the postmanbin application. Inspired by HTTPBIN.
"""

import time
import base64
import json

from flask import Response, request, jsonify, g, Blueprint, redirect, make_response, render_template
import utils.helper as helpers

# ----
# Debug Routes
# ----

# initialize debug_routes as a blueprint
debug_routes = Blueprint('debug_routes', __name__)

def get_files():
    """ returns files from the request context """
    files = dict()
    for k, v in request.files.items():
        files[k] = helpers.json_safe(v.read(), request.files[k].content_type)
    return files

def get_headers():
    """ returns headers from the request context """
    headers = dict(request.headers.items())
    return headers

def get_ip():
    """ returns the client ip """
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def get_dict(*keys, **extras):
    """ main helper function that generates a dict with subset of keys as requested """
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

@debug_routes.route('/status')
def view_status():
    """ return json showing status and timestamp """
    return jsonify(get_dict("status", "timestamp"))

@debug_routes.route('/delay/<int:seconds>')
def delay(seconds):
    """ show json response after a delay of n (max 10) seconds """
    delay = min(seconds, 10) # max 10 seconds
    time.sleep(delay)
    return jsonify(get_dict('origin', delay=seconds))

@debug_routes.route('/headers')
def headers():
    """ return json showing headers """
    return jsonify(get_dict('headers'))

@debug_routes.route('/get')
def get_request():
    """ same as httpbin """
    return jsonify(get_dict('origin', 'headers', 'url', 'args'))

@debug_routes.route('/post', methods=["POST"])
def post_request():
    """ same as httpbin """
    return jsonify(get_dict('form', 'data', 'json', 'files', 'args',
                            'url', 'headers', 'origin'))

@debug_routes.route('/code/<int:code>')
def get_code(code):
    """ return the HTTP status code """
    response = make_response('')
    response.status_code = code
    return response

@debug_routes.route('/redirect-to')
def redirect_page():
    # GET /redirect-to?url=http://www.example.com
    url = request.args.get('url')
    response = make_response('')
    response.status_code = 302
    response.headers['Location'] = url.encode('utf-8')
    return response

@debug_routes.route('/large')
def large_response():
    """ Returns large dummy response: GET /large?type=html&n=2 """
    response_type = request.args.get('type')

    if request.args.get('n'):
        limit = int(request.args.get('n'))
    else:
        limit = 10

    if response_type not in ["json", "xml", "html", "text"]:
        return jsonify(message="Usage: /large?type=json or xml or html or text")
    if response_type == "html":
        return render_template('large.html', limit=range(limit))
    if response_type == "text":
        return Response(helpers.dummy_text(limit), mimetype="text")
    if response_type == "xml":
        return Response(helpers.dummy_xml(limit), mimetype="text/xml")
    return jsonify(content=helpers.dummy_json(limit))

@debug_routes.route('/method', methods=helpers.POSTMAN_METHODS)
def custom_methods():
    return jsonify(method=request.method)


@debug_routes.route('/cookies')
def cookies():
    """ retrive cookies """
    return jsonify(get_dict('cookies'))

@debug_routes.route('/cookies/set')
def set_cookie():
    """ set the value of cookie  - GET /cookies/set?name=value"""
    if request.args:
        response = make_response(redirect('/cookies'))
        key, value = request.args.items()[0]
        response.set_cookie(key, value)
        return response
    return jsonify(message="No params found"), 404

@debug_routes.route('/cookies/delete')
def delete_cookie():
    """ deletes the value of cookie - GET /cookies/delete?key=name """
    cookies = dict(request.cookies)
    if request.args:
        response = make_response(redirect('/cookies'))
        response.delete_cookie(key=request.args.get('key'))
        return response
    return jsonify(message="No key found"), 404
