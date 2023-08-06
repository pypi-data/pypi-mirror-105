# -*- coding: utf-8 -*-

from lsyflaskmicroapp_ueditor.apis import file_upload
from lsyflaskmicroapp_ueditor.apis import ueditor_file
from lsyflaskmicroapp_ueditor.config import UEDITOR_CONFIG
from lsyflaskmicroapp_ueditor.orm import init_db


def init_app(app):
    if not app.config.get("UEDITOR_CONFIG", None):
        app.config.setdefault("UEDITOR_CONFIG", UEDITOR_CONFIG)

    if not app.config.get("UEDITOR_BUCKET_NAME", None):
        raise Exception("lsyflaskmicroapp_ueditor not find UEDITOR_BUCKET_NAME in config")

    init_db(app)

    app.register_blueprint(file_upload.bp, url_prefix='/api/ueditor')
    app.register_blueprint(ueditor_file.bp, url_prefix='/api/ueditor_file')


__all__ = ['init_app']
