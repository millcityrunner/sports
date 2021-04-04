import requests
import logging
from flask import Flask
from configs import Settings


class RequestSession:
    def __init__(self):
        self.s = requests.Session()
        self.setup_requests_session()

    def setup_requests_session(self):
        self.s.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.s.cert = "path/to/certs.cert" if Settings.SECRETS.get("SSL_CERTS_CERT", None) is not None else None
        self.s.verify = "path/to/certfile" if Settings.SECRETS.get("SSL_CERTS_PATH", None) is not None else None


def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)
    app.logger.setLevel(logging.DEBUG)

    return app, app.logger


app, logger = create_app()
requester = RequestSession()
