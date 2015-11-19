from flask import Flask, jsonify, Response

from flask_accept import accept, accept_fallback

app = Flask(__name__)
app.debug = True


@app.route('/with-fallback')
@accept_fallback
def index_with_fallback():
    return jsonify(version='v0')


@index_with_fallback.support('application/vnd.vendor.v1+json')
def index_with_fallback_v1():
    return jsonify(version='v1')


@index_with_fallback.support(
    'application/json',
    'application/vnd.vendor+json',
    'application/vnd.vendor.v2+json')
def index_with_fallback_v2():
    return jsonify(version='v2')


@app.route('/without-fallback')
@accept('application/vnd.vendor.v1+json')
def index_without_fallback():
    return jsonify(version='v1')


@index_without_fallback.support(
    'application/json',
    'application/vnd.vendor+json',
    'application/vnd.vendor.v2+json')
def index_with_fallback_v2():
    return jsonify(version='v2')


@app.route('/precedence')
@accept_fallback
def precedence():
    return Response(headers={'Content-Type': 'fallback/fallback'})


for media_type in ['text/plain;format=flowed', 'text/plain', 'text/*', '*/*']:
    precedence.support(media_type)(
        lambda media_type=media_type:
        Response(headers={'Content-Type': media_type})
    )
