from flask_init import *


DEV = True


if __name__ == '__main__':
    port = 8080
    host = "0.0.0.0"
    if DEV:
        app.run(host=host, port=port, debug=True)
    else:
        from waitress import serve
        serve(app, host=host, port=port)
