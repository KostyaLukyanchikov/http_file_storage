import logging

from flask import Flask, request
from flask.typing import ResponseReturnValue

from src import db
from src import exceptions
from src.api import files_blueprint


def set_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


class MyFlask(Flask):

    def dispatch_request(self) -> ResponseReturnValue:
        try:
            if request.method in ['POST', 'DELETE']:
                self.auth()
            return super().dispatch_request()
        except exceptions.ServerError as e:
            return e.msg, e.error_code

    @staticmethod
    def auth():
        auth = request.authorization
        if not auth:
            raise exceptions.AuthRequired
        if db.get_user_pwd(auth['username']) != auth['password']:
            raise exceptions.AuthFailed


def create_app():
    set_logging()
    app_ = MyFlask(__name__)
    app_.register_blueprint(files_blueprint)
    init_db(app_)
    return app_


def init_db(app_: MyFlask):
    app_.teardown_appcontext(db.close_connection)


app = create_app()
