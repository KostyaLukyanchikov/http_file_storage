import logging

import flask
from flask import request, Response
from flask_restful import Api, Resource

from src.auth import auth
from src.storage import Storage

files_blueprint = flask.Blueprint('files', __name__)
files_api = Api(files_blueprint)


@files_api.resource('/files/<string:file_hash>')
class FileResource(Resource):

    @staticmethod
    def get(file_hash: str):
        data = Storage.read(file_hash)
        return Response(data, status=200)

    @staticmethod
    def delete(file_hash: str):
        user = request.authorization['username']
        Storage.delete(user=user, file_hash=file_hash)
        return ''


@files_api.resource('/files')
class FilesResource(Resource):

    @staticmethod
    def get():
        return Storage.get_names()

    @staticmethod
    @auth.verify_password
    def post():
        data = request.data
        user = request.authorization['username']
        file_hash = Storage.save(user=user, data=data)
        return file_hash
