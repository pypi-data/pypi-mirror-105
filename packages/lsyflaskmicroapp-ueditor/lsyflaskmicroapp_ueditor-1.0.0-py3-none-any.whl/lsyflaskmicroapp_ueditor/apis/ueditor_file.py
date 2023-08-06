# -*- coding: utf-8 -*-

"""
UEditor_File
~~~~~~~~~~~~~
文件
"""

import logging
import os
from datetime import datetime

from flask import make_response, current_app, redirect
from flask import request
from flask_login import current_user
from lsyflaskplugin_minio.api import put_dropzone_object, get_presigned_object
from lsyflasksdkcore import RequestQuery, eresponse, sresponse
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.exceptions import DBError
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery
from lsyflasksdkcore.swagger import doc
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_ueditor.entitys.ueditor_file import UEditorFileEdit, UEditorFilePagerQuery
from lsyflaskmicroapp_ueditor.models import create_ueditor_file_model
from lsyflaskmicroapp_ueditor.schemas.ueditor_file import UEditorFileDetailSchema, UEditorFilePagerQuerySchema, \
    UEditorFileEditSchema

logger = logging.getLogger(__name__)

bp = Blueprint('ueditor_file', __name__)

file_classify = {'bmp': 'img', 'jpg': 'img', 'png': 'img', 'tif': 'img', 'gif': 'img', 'pcx': 'img', 'tga': 'img',
                 'exif': 'img', 'fpx': 'img', 'svg': 'img', 'psd': 'img', 'cdr': 'img', 'pcd': 'img', 'dxf': 'img',
                 'ufo': 'img', 'eps': 'img', 'ai': 'img', 'raw': 'img', 'WMF': 'img', 'webp': 'img',
                 'rar': 'zip', 'zip': 'zip', 'cab': 'zip', 'iso': 'zip', 'jar': 'zip', 'ace': 'zip',
                 '7z': 'zip', 'tar': 'zip', 'gz': 'zip', 'arj': 'zip', 'lzh': 'zip', 'uue': 'zip',
                 'bz2': 'zip', 'z': 'zip',
                 'xls': 'excel', 'xlsx': 'excel',
                 'doc': 'word', 'docx': 'word',
                 'wmv': 'video', 'asf': 'video', 'asx': 'video', 'rm': 'video', ' rmvb': 'video', 'mp4': 'video',
                 '3gp': 'video', 'mov': 'video', 'm4v': 'video', 'avi': 'video', 'dat': 'video', 'mkv': 'video',
                 'flv': 'video', 'vob': 'video',
                 'mp3': 'music', 'aac': 'music', 'ogg vorbis': 'music', 'opus,wav': 'music', 'flac': 'music',
                 'ape': 'music', 'alac': 'music', 'wavpack': 'music',
                 'pdf': 'pdf',
                 'txt': 'txt'}


@bp.route('/page', methods=['POST'])
@doc.post("ueditor", UEditorFilePagerQuerySchema.__name__, [UEditorFileDetailSchema.__name__])
@doc.pager()
@bp.auth.grant_view
def page():
    """分页查询"""
    try:
        query = RequestQuery(UEditorFilePagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: UEditorFilePagerQuery = query.data

        model = create_ueditor_file_model()
        dbr, count = model.get_page_query(qd.folder_code, qd.file_name, qd.rows, qd.offset)
        return sresponse(dbr.to_json(), total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@doc.post("ueditor", UEditorFileEditSchema.__name__)
@bp.auth.grant_edit
def modify():
    """修改"""
    try:
        query = RequestQuery(UEditorFileEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: UEditorFileEdit = query.data
        model = create_ueditor_file_model()
        model.modify(entity.id, entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/delete', methods=['POST'])
@doc.post("ueditor", PksQuerySchema.__name__)
@bp.auth.grant_delete
def delete():
    """删除"""
    try:
        query = RequestQuery(PksQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: PksQuery = query.data
        model = create_ueditor_file_model()
        model.tran_delete(qd.ids)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


def upload_record_to_db(file_name, file_alias_name, file_size, folder_code, user_id):
    _name, file_type = os.path.splitext(file_name)
    file_class = file_classify.get(file_type[1:], 'unknown')
    entity = UEditorFileEdit()
    entity.id = get_uuid_str()
    entity.file_name = file_name
    entity.file_format = file_class
    entity.file_alias_name = file_alias_name
    entity.file_size = file_size
    entity.create_time = datetime.now()
    entity.create_user_id = user_id
    entity.folder_code = folder_code
    try:
        model = create_ueditor_file_model()
        model.add(entity)
    except DBError as ex:
        raise ex


@bp.route('/upload', methods=['POST'])
@bp.auth.grant_view
def upload():
    """上传文件"""
    try:
        f = request.files['file']
        folder_code = request.form.get('folder_code', None)

        if folder_code == "image":
            _name, file_type = os.path.splitext(f.filename)
            file_class = file_classify.get(file_type[1:], 'unknown')
            if file_class != "img":
                return make_response(("文件不是图片类型", 500))

        bucket_name = current_app.config['UEDITOR_BUCKET_NAME']
        minio_file = put_dropzone_object(bucket_name, f)
        if minio_file:
            upload_record_to_db(f.filename, minio_file.object_name, minio_file.object_size,
                                folder_code, current_user.get_id())
            return make_response(("上传成功", 200))
        return sresponse(None)
    except Exception as ex:
        logger.error(ex)
        return make_response(("服务器内部错误", 500))


@bp.route('/public_file', methods=['GET'])
def public_file():
    try:
        oid = request.args.get("o", None)
        if oid is None:
            return eresponse("参数错误")
        bucket_name = current_app.config['UEDITOR_BUCKET_NAME']
        presingned_url = get_presigned_object(bucket_name, oid)
        return redirect(presingned_url, code=302)
    except Exception as ex:
        logger.error(ex)
        return make_response(("服务器内部错误", 500))
