# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate, post_dump

from lsyflaskmicroapp_ueditor.entitys.ueditor_file import UEditorFileBase, UEditorFileEdit, UEditorFileDetail, \
    UEditorFilePagerQuery


class UEditorFileSchema(Schema):
    """ 文件 Schema """
    # 文件id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36), description="文件id")
    # 所属目录
    folder_code = fields.Str(required=True, validate=validate.OneOf(('file', 'image', 'video',)), description="目录编码")
    # 文件名称
    file_name = fields.Str(required=True, validate=validate.Length(max=100), description="文件名称")
    # 文件格式
    file_format = fields.Str(required=True, validate=validate.Length(max=50), description="文件格式")
    # 文件大小
    file_size = fields.Int(required=True, validate=validate.Range(min=0, max=99999999), description="文件大小")
    # 文件别名
    file_alias_name = fields.Str(required=True, description="文件别名")
    # 创建时间
    create_time = fields.DateTime(required=True, description="创建时间")
    # 创建人
    create_user_id = fields.Str(required=True, validate=validate.Length(max=36), description="创建人")
    # 备注
    remark = fields.Str(required=False, allow_none=True, description="备注")

    @post_load
    def make(self, data, **kwargs):
        return UEditorFileBase().__fill__(**data)


class UEditorFileEditSchema(UEditorFileSchema):

    @post_load
    def make(self, data, **kwargs):
        return UEditorFileEdit().__fill__(**data)


class UEditorFileDetailSchema(UEditorFileSchema):
    # 创建人
    create_user_id_name = fields.Str(required=False, allow_none=True, description="创建人名字")
    file_url = fields.Str(description="文件url")

    @post_dump
    def make_file_url(self, data, **kwargs):
        data["file_url"] = f"/api/ueditor_file/public_file?o={data['file_alias_name']}"
        return data

    @post_load
    def make(self, data, **kwargs):
        return UEditorFileDetail().__fill__(**data)


class UEditorFilePagerQuerySchema(PagerQuerySchema):
    folder_code = fields.Str(required=True, validate=validate.OneOf(('file', 'image', 'video', '*',)),
                             description="目录编码")
    # 文件名称
    file_name = fields.Str(required=False, validate=validate.Length(max=20), description="文件名称")

    @post_load
    def make(self, data, **kwargs):
        return UEditorFilePagerQuery().__fill__(**data)
