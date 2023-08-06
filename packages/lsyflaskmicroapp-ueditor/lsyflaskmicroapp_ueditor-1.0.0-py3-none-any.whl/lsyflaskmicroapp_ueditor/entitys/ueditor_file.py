# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass, PagerQuery


class UEditorFileBase(AutoClass):
    """文件"""

    def __init__(self):
        # 文件id
        self.id = ""
        # 所属目录
        self.folder_code = ""
        # 文件名称
        self.file_name = ""
        # 文件格式
        self.file_format = ""
        # 文件大小
        self.file_size = None
        # 文件别名
        self.file_alias_name = ""
        # 创建时间
        self.create_time = None
        # 创建人
        self.create_user_id = ""
        # 备注
        self.remark = ""


class UEditorFileEdit(UEditorFileBase):
    pass


class UEditorFileDetail(UEditorFileBase):
    def __init__(self):
        super().__init__()
        self.create_user_id_name = ""
        self.file_url = ""


class UEditorFilePagerQuery(PagerQuery):
    def __init__(self):
        super().__init__()
        # 所属目录
        self.folder_code = ""
        # 文件名称
        self.file_name = ""
