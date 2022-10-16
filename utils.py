import os
from flask import Response


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


def send_html(name):
    content = get_file(os.path.join('frontend', name))
    return Response(content, mimetype='text/html')
