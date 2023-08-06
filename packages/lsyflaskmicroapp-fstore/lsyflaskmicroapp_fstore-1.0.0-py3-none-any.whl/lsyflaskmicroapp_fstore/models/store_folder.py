# -*- coding: utf-8 -*-

from typing import List

import sqlalchemy as sa
from lsyflasksdkcore.exceptions import DBError, DBRefError
from lsyflasksdkcore.model import DBResult, DBRef
from lsyflasksdkcore.schema import DBRefSchema
from marshmallow import ValidationError
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError

from lsyflaskmicroapp_fstore.entitys.store_folder import StoreFolderBase, StoreFolderEdit, StoreFolderDetail
from lsyflaskmicroapp_fstore.orm import StoreFile, StoreFolder, AuthUser
from lsyflaskmicroapp_fstore.orm import db, model
from lsyflaskmicroapp_fstore.schemas.store_folder import StoreFolderSchema, StoreFolderDetailSchema


class StoreFolderModel(object):
    """ 文件目录 Model
    """

    columns = [StoreFolder.id, StoreFolder.pre_folder_id, StoreFolder.folder_name, StoreFolder.user_id,
               StoreFolder.create_user_id, StoreFolder.create_time, StoreFolder.attribute, StoreFolder.remark]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(StoreFolder, sort), order)()
        return None

    @model.entity(StoreFolderSchema)
    def get_one(self, _id: str) -> DBResult[StoreFolderBase]:
        try:
            return self.session.query(StoreFolder).filter(StoreFolder.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(StoreFolderSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[StoreFolderBase]:
        try:
            q = self.session.query(StoreFolder)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.list(StoreFolderSchema)
    def get_list_pre_folder_id(self, pre_folder_id: str, sort=None, order=None) -> DBResult[StoreFolderBase]:
        try:
            query = self.session.query(StoreFolder).filter(StoreFolder.pre_folder_id == pre_folder_id)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                query = query.order_by(_sorted)
            return query.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_pre_folder_id error,error:{ex}")

    @model.list(DBRefSchema)
    def get_refer(self, _id: str) -> DBResult[DBRef]:
        try:
            q_storefile = self.session.query(sa.literal('StoreFile').label('ref_code'),
                                             sa.literal(u'文件').label('ref_desc'),
                                             sa.func.count('*').label('ref_count')).select_from(StoreFile).filter(
                StoreFile.folder_id == _id)

            q_storefolder = self.session.query(sa.literal('StoreFolder').label('ref_code'),
                                               sa.literal(u'文件目录').label('ref_desc'),
                                               sa.func.count('*').label('ref_count')).select_from(StoreFolder).filter(
                StoreFolder.pre_folder_id == _id)

            q = sa.union_all(q_storefile, q_storefolder)
            t = orm.aliased(q)
            rows = self.session.query(t).filter(t.c.ref_count > 0).all()
            return rows
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_refer error,error:{ex}")

    def add(self, entity: StoreFolderBase):
        try:
            schema = StoreFolderSchema()
            d = schema.dump(entity)
            row = StoreFolder(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: StoreFolderEdit):
        try:
            schema = StoreFolderSchema()
            d = schema.dump(entity)
            self.session.query(StoreFolder).filter(StoreFolder.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        refs = self.get_refer(_id).to_list()
        if refs:
            raise DBRefError(refs.pop())
        try:
            self.session.query(StoreFolder).filter(StoreFolder.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def delete_pre_folder_id(self, pre_folder_id: str):
        try:
            self.session.query(StoreFolder).filter(StoreFolder.pre_folder_id == pre_folder_id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete_pre_folder_id error,error:{ex}")

    def tran_delete(self, folder_ids: List[str], file_ids: List[str]):
        folder_refs_count = self.session.query(StoreFolder).filter(StoreFolder.pre_folder_id.in_(folder_ids)).count()
        if folder_refs_count > 0:
            ref = DBRef().withCount(folder_refs_count).withDesc("目录非空，目录中包含下级目录。")
            raise DBRefError(ref)

        file_refs_count = self.session.query(StoreFile).filter(StoreFile.folder_id.in_(folder_ids)).count()
        if file_refs_count > 0:
            ref = DBRef().withCount(file_refs_count).withDesc("目录非空，目录中包含文件。")
            raise DBRefError(ref)

        try:
            self.session.query(StoreFolder).filter(
                StoreFolder.id.in_(folder_ids)).delete(synchronize_session=False)

            self.session.query(StoreFile).filter(StoreFile.id.in_(file_ids)).delete(synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    def tran_move(self, target_folder_id: str, folder_ids: List[str], file_ids: List[str]):
        """
        批量移动文件和文件夹
        :param target_folder_id: 目标目录id
        :param folder_ids: 目录ids
        :param file_ids: 文件ids
        :return:
        """
        try:
            for file_id in file_ids:
                self.session.query(StoreFile).filter(StoreFile.id == file_id).update({"folder_id": target_folder_id})
            for folder_id in folder_ids:
                self.session.query(StoreFolder).filter(StoreFolder.id == folder_id).update(
                    {"pre_folder_id": target_folder_id})
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    @model.list(StoreFolderDetailSchema)
    def get_child_list_query(self, pre_folder_id: str, user_id: str,
                             sort: str, order: str) -> DBResult[StoreFolderDetail]:
        """
        获取下级目录列表包括用户私有目录和公有目录
        :param pre_folder_id: 上级目录id
        :param user_id: 用户id
        :param sort: 排序字段
        :param order: 排序方式
        :return:
        """
        try:
            t1 = orm.aliased(StoreFolder)
            columns = self.columns
            q = self.session.query(*columns, AuthUser.user_name.label("create_user_id_name"),
                                   t1.folder_name.label("pre_folder_id_name")) \
                .select_from(StoreFolder) \
                .outerjoin(AuthUser, AuthUser.id == StoreFolder.create_user_id) \
                .outerjoin(t1, t1.id == StoreFolder.pre_folder_id) \
                .filter(sa.or_(StoreFolder.user_id.is_(None), StoreFolder.user_id == user_id)) \
                .filter(StoreFolder.pre_folder_id == pre_folder_id)

            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            else:
                q = q.order_by(StoreFolder.folder_name)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_child_list_query error,error:{ex}")

    @model.list(StoreFolderSchema)
    def get_list_query(self, user_id: str, sort: str = "folder_name", order: str = "asc") -> DBResult[StoreFolderBase]:
        """
        获取目录列表包括用户私有目录和公有目录
        :param user_id: 用户id
        :param sort: 排序字段
        :param order: 排序方式
        :return:
        """
        try:
            q = self.session.query(StoreFolder) \
                .filter(sa.or_(StoreFolder.user_id.is_(None), StoreFolder.user_id == user_id))
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            else:
                q = q.order_by(StoreFolder.folder_name)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_query error,error:{ex}")
