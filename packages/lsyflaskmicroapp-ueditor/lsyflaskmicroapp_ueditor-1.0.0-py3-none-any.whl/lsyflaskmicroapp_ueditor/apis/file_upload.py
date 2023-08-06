import json
import logging

from flask import make_response, jsonify, current_app
from flask import request
from lsyflaskplugin_minio.api import put_dropzone_object
from lsyflasksdkcore import sresponse
from lsyflasksdkcore.blueprints import Blueprint

from lsyflaskmicroapp_ueditor.models import create_ueditor_file_model

logger = logging.getLogger(__name__)

bp = Blueprint('file_upload', __name__)

"""
http://fex.baidu.com/ueditor/#dev-request_specification
http://fex.baidu.com
"""


@bp.route('/config', methods=['GET'])
@bp.auth.grant_view
def config():
    try:
        callback_func_name = request.args["callback"]
        config_args = json.dumps(current_app.config['UEDITOR_CONFIG'])
        response = make_response(f"{callback_func_name}({config_args})")
        response.headers['Content-Type'] = 'application/javascript; charset=utf-8'
        return response
    except Exception as ex:
        logger.error(ex)
        return make_response(("服务器内部错误", 500))


@bp.route('/upload', methods=['POST', 'GET'])
@bp.auth.grant_view
def upload():
    try:
        action = request.args["action"]
        if action == "uploadimage" and request.method == "POST":
            f = request.files['upfile']
            bucket_name = current_app.config['MINIO_FSTORE_BUCKET_NAME']
            minio_file = put_dropzone_object(bucket_name, f)
            if minio_file:
                url = "/api/fstore/store_file/public_file?o=%s" % minio_file.object_name
                return jsonify({"state": "SUCCESS", "url": url, "title": "", "original": "", "error": None})
            return sresponse(None)
        if (action == "uploadfile" or action == "uploadvideo") and request.method == "POST":
            f = request.files['upfile']
            bucket_name = current_app.config['MINIO_FSTORE_BUCKET_NAME']
            minio_file = put_dropzone_object(bucket_name, f)
            if minio_file:
                url = "/api/fstore/store_file/public_file?o=%s" % minio_file.object_name
                return jsonify({"state": "SUCCESS", "url": url, "title": "", "original": "", "error": None})
            return sresponse(None)
        if action == "uploadscrawl" and request.method == "POST":
            base64 = request.form["upfile"]
            return jsonify(
                {"state": "SUCCESS", "url": "https://www.baidu.com/img/flexible/logo/pc/result.png", "title": "",
                 "original": "", "error": None})

        # http://192.168.102.229:9600/api/ueditor/upload?start=0&size=20&action=listimage&callback=bd__editor__45p7to
        if action == "listimage":
            callback_func_name = request.args["callback"]
            start = request.args["start"]
            size = request.args["size"]

            model = create_ueditor_file_model()
            dbr, count = model.get_page_query("image", "", start, size)
            lst = dbr.to_list()
            images = []
            data = {
                "start": "0",
                "state": "SUCCESS",
                "total": 2,
                "list": [
                    {"url": "https://www.baidu.com/img/flexible/logo/pc/result.png", "mtime": 1},
                    {"url": "https://w1.hoopchina.com.cn/channel/website/static/images/basketball-nba-logo.png",
                     "mtime": 2}
                ]
            }
            config_args = json.dumps(data)
            response = make_response(f"{callback_func_name}({config_args})")
            response.headers['Content-Type'] = 'application/javascript; charset=utf-8'
            return response

        # http://192.168.102.229:9600/api/ueditor/upload?action=listfile&start=0&size=20&noCache=1614926228694
        if action == "listfile":
            start = request.args["start"]
            size = request.args["size"]
            model = create_ueditor_file_model()
            model.get_page_query("file", "", start, size)

            data = {
                "start": "0",
                "state": "SUCCESS",
                "total": 2,
                "list": [
                    {"url": "https://www.baidu.com/img/flexible/logo/pc/result.png", "mtime": 1},
                    {"url": "https://w1.hoopchina.com.cn/channel/website/static/images/basketball-nba-logo.png",
                     "mtime": 2}
                ]
            }
            return jsonify(data)
        if action == "config" and request.method == "GET":
            callback_func_name = request.args["callback"]
            config_args = json.dumps(current_app.config['UEDITOR_CONFIG'])
            response = make_response(f"{callback_func_name}({config_args})")
            response.headers['Content-Type'] = 'application/javascript; charset=utf-8'
            return response
    except Exception as ex:
        logger.error(ex)
        return make_response(("服务器内部错误", 500))
