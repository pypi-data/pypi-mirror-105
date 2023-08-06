# -*- coding: utf-8 -*-


from typing import List

from lsyflasksdkcore.exceptions import DBError
from lsyflasksdkcore.model import DBResult
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from lsyflaskmicroapp_fstore.entitys.store_file import StoreFileBase, StoreFileEdit, StoreFileDetail
from lsyflaskmicroapp_fstore.orm import db, model, StoreFile, AuthUser, StoreFolder
from lsyflaskmicroapp_fstore.schemas.store_file import StoreFileSchema, StoreFileDetailSchema


class StoreFileModel(object):
    """ 文件 Model
    """

    columns = [StoreFile.id, StoreFile.folder_id, StoreFile.file_name, StoreFile.file_format, StoreFile.file_size,
               StoreFile.file_alias_name, StoreFile.create_time, StoreFile.create_user_id, StoreFile.remark]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(StoreFile, sort), order)()
        return None

    @model.entity(StoreFileSchema)
    def get_one(self, _id: str) -> DBResult[StoreFileBase]:
        try:
            return self.session.query(StoreFile).filter(StoreFile.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(StoreFileSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[StoreFileBase]:
        try:
            q = self.session.query(StoreFile)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.list(StoreFileDetailSchema)
    def get_list_search(self, folder_id: str, file_name: str, sort: str, order: str) -> DBResult[StoreFileDetail]:
        try:
            columns = self.columns
            q = self.session.query(*columns, AuthUser.user_name.label("create_user_id_name"),
                                   StoreFolder.folder_name.label("folder_id_name")) \
                .select_from(StoreFile) \
                .outerjoin(AuthUser, AuthUser.id == StoreFile.create_user_id) \
                .outerjoin(StoreFolder, StoreFolder.id == StoreFile.folder_id)

            if folder_id:
                q = q.filter(StoreFile.folder_id == folder_id)

            if file_name:
                q = q.filter(StoreFile.file_name.contains(file_name))

            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            else:
                q = q.order_by(StoreFile.file_name)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_search error,error:{ex}")

    @model.list(StoreFileDetailSchema)
    def get_list_folder_id(self, folder_id: str, file_name: str, sort: str, order: str) -> DBResult[StoreFileDetail]:
        try:
            columns = self.columns
            q = self.session.query(*columns, AuthUser.user_name.label("create_user_id_name"),
                                   StoreFolder.folder_name.label("folder_id_name")) \
                .select_from(StoreFile) \
                .outerjoin(AuthUser, AuthUser.id == StoreFile.create_user_id) \
                .outerjoin(StoreFolder, StoreFolder.id == StoreFile.folder_id) \
                .filter(StoreFile.folder_id == folder_id)

            if file_name:
                q = q.filter(StoreFile.file_name.contains(file_name))

            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            else:
                q = q.order_by(StoreFile.file_name)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_folder_id error,error:{ex}")

    def add(self, entity: StoreFileEdit):
        try:
            schema = StoreFileSchema()
            d = schema.dump(entity)
            row = StoreFile(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: StoreFileEdit):
        try:
            schema = StoreFileSchema()
            d = schema.dump(entity)
            self.session.query(StoreFile).filter(StoreFile.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        try:
            self.session.query(StoreFile).filter(StoreFile.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def delete_folder_id(self, folder_id: str):
        try:
            self.session.query(StoreFile).filter(StoreFile.folder_id == folder_id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete_folder_id error,error:{ex}")

    def tran_delete(self, pks: List[str]):
        try:
            self.session.query(StoreFile).filter(
                StoreFile.id.in_(pks)).delete(synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")
