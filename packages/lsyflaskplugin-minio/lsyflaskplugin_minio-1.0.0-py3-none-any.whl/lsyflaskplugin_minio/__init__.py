# coding: utf-8

import os

import minio
from flask import current_app, _app_ctx_stack

from .api import put_chunk_object, put_file, put_object
from .error import MinioError

basedir = os.path.abspath(os.path.dirname(__file__))


class Minio(object):
    """This class is used to control the Minio integration to one or more Flask
    applications.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not self.app:
            self.app = app

        app.minio_manager = self

        if not app.config.get("MINIO_ENDPOINT", None):
            raise MinioError("not find MINIO_ENDPOINT config")
        if not app.config.get("MINIO_ACCESS_KEY", None):
            raise MinioError("not find MINIO_ACCESS_KEY config")
        if not app.config.get("MINIO_SECRET_KEY", None):
            raise MinioError("not find MINIO_SECRET_KEY config")

        app.config.setdefault('MINIO_SECURE', True)
        app.config.setdefault('MINIO_REGION', None)
        app.config.setdefault('MINIO_HTTP_CLIENT', None)
        app.config.setdefault('MINIO_TEMP_SPACE', os.path.join(basedir, 'minio_temp_space'))
        app.teardown_appcontext(self.teardown)

    @staticmethod
    def connect():
        return minio.Minio(
            current_app.config['MINIO_ENDPOINT'],
            access_key=current_app.config['MINIO_ACCESS_KEY'],
            secret_key=current_app.config['MINIO_SECRET_KEY'],
            secure=current_app.config['MINIO_SECURE'],
            region=current_app.config['MINIO_REGION'],
            http_client=current_app.config['MINIO_HTTP_CLIENT']
        )

    @staticmethod
    def teardown(exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'minio'):
            ctx.minio._http.clear()

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'minio'):
                ctx.minio = self.connect()
            return ctx.minio


def init_minio(app):
    client = Minio()
    client.init_app(app)


__all__ = ['init_minio', 'put_object', 'put_chunk_object', 'put_file']

__version__ = "1.0.0"
