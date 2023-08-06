# -*- coding: utf-8 -*-


from typing import List, Tuple

from lsyflasksdkcore.exceptions import DBError
from lsyflasksdkcore.model import DBResult
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from lsyflaskmicroapp_ueditor.entitys.ueditor_file import UEditorFileEdit, UEditorFileBase, UEditorFileDetail
from lsyflaskmicroapp_ueditor.orm import db, model, UEditorFile, AuthUser
from lsyflaskmicroapp_ueditor.schemas.ueditor_file import UEditorFileSchema, UEditorFileDetailSchema


class UEditorFileModel(object):
    """ 文件 Model
    """

    columns = [UEditorFile.id, UEditorFile.folder_code, UEditorFile.file_name, UEditorFile.file_format,
               UEditorFile.file_size, UEditorFile.file_alias_name, UEditorFile.create_time,
               UEditorFile.create_user_id, UEditorFile.remark]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(UEditorFile, sort), order)()
        return None

    @model.entity(UEditorFileSchema)
    def get_one(self, _id: str) -> DBResult[UEditorFileBase]:
        try:
            return self.session.query(UEditorFile).filter(UEditorFile.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(UEditorFileSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[UEditorFileBase]:
        try:
            q = self.session.query(UEditorFile)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.pager(UEditorFileDetailSchema)
    def get_page_query(self, folder_code: str, file_name: str,
                       limit: int, offset: int) -> Tuple[DBResult[UEditorFileDetail], int]:
        try:
            columns = self.columns
            q = self.session.query(*columns, AuthUser.user_name.label("create_user_id_name")) \
                .select_from(UEditorFile) \
                .outerjoin(AuthUser, AuthUser.id == UEditorFile.create_user_id)

            if folder_code != "*":
                q = q.filter(UEditorFile.folder_code == folder_code)
            if file_name:
                q = q.filter(UEditorFile.file_name.contains(file_name))

            rows = None
            count = q.count()
            if count > 0:
                q = q.order_by(UEditorFile.file_name.asc())
                rows = q.limit(limit).offset(offset).all()
            return rows, count
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_search error,error:{ex}")

    def add(self, entity: UEditorFileEdit):
        try:
            schema = UEditorFileSchema()
            d = schema.dump(entity)
            row = UEditorFile(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: UEditorFileEdit):
        try:
            schema = UEditorFileSchema()
            d = schema.dump(entity)
            self.session.query(UEditorFile).filter(UEditorFile.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        try:
            self.session.query(UEditorFile).filter(UEditorFile.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def tran_delete(self, pks: List[str]):
        try:
            self.session.query(UEditorFile).filter(
                UEditorFile.id.in_(pks)).delete(synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")
