# -*- coding: utf-8 -*-

"""
Store_Folder
~~~~~~~~~~~~~
文件目录
"""

import logging
import typing
from datetime import datetime as dt

from flask_login import current_user
from lsyflasksdkcore import RequestQuery, eresponse, sresponse
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.exceptions import DBRefError
from lsyflasksdkcore.swagger import doc
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_fstore.entitys.store_folder import StoreFolderEdit, StoreFolderCreate, \
    StoreFolderBase, StoreFolderListQuery, TranDelete, TranMove
from lsyflaskmicroapp_fstore.models import create_store_folder_model
from lsyflaskmicroapp_fstore.schemas.store_folder import StoreFolderEditSchema, StoreFolderCreateSchema, \
    StoreFolderListQuerySchema, \
    TranDeleteSchema, StoreFolderDetailSchema, TranMoveSchema

logger = logging.getLogger(__name__)

bp = Blueprint('store_folder', __name__)


@bp.route('/list', methods=['POST'])
@doc.post("fstore", StoreFolderListQuerySchema.__name__, [StoreFolderDetailSchema.__name__])
@bp.auth.grant_view
def child_lst():
    """获取下级文件夹列表"""
    try:
        query = RequestQuery(StoreFolderListQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StoreFolderListQuery = query.data

        order = qd.order or "asc"
        sort = "folder_name"
        if qd.sort is None or qd.sort == "file_name" or qd.sort == "file_size":
            sort = "folder_name"

        user_id = current_user.get_id()
        model = create_store_folder_model()
        data = model.get_child_list_query(qd.pre_folder_id, user_id, sort, order).json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
@doc.post("fstore", StoreFolderCreateSchema.__name__)
@bp.auth.grant_add
def add():
    """新增"""
    try:
        query = RequestQuery(StoreFolderCreateSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StoreFolderCreate = query.data
        entity = StoreFolderBase()
        entity.id = get_uuid_str()
        entity.create_time = dt.now()
        entity.create_user_id = current_user.get_id()
        entity.folder_name = qd.folder_name
        entity.attribute = qd.attribute
        entity.pre_folder_id = qd.pre_folder_id
        entity.remark = qd.remark

        if qd.is_public:
            entity.user_id = None
        else:
            entity.user_id = current_user.get_id()

        model = create_store_folder_model()
        model.add(entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@doc.post("fstore", StoreFolderEditSchema.__name__)
@bp.auth.grant_edit
def modify():
    """修改"""
    try:
        query = RequestQuery(StoreFolderEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StoreFolderEdit = query.data

        entity = StoreFolderBase()
        entity.id = qd.id
        entity.create_time = dt.now()
        entity.create_user_id = current_user.get_id()
        entity.folder_name = qd.folder_name
        entity.attribute = qd.attribute
        entity.pre_folder_id = qd.pre_folder_id
        entity.remark = qd.remark
        if qd.is_public:
            entity.user_id = None
        else:
            entity.user_id = current_user.get_id()

        model = create_store_folder_model()
        model.modify(entity.id, entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/tran_delete', methods=['POST'])
@doc.post("fstore", TranDeleteSchema.__name__)
@bp.auth.grant_view
def tran_delete():
    """批量删除文件夹及文件"""
    try:
        query = RequestQuery(TranDeleteSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: TranDelete = query.data
        model = create_store_folder_model()
        model.tran_delete(qd.folder_ids, qd.file_ids)
        return sresponse()
    except DBRefError as ex:
        return eresponse(ex.message)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


def _depth_find_pre_folder_id(folder_lst: typing.List[StoreFolderBase], pre_folder_id: str,
                              pre_folder_id_lst: typing.List[str]):
    lst = [item for item in folder_lst if item.id == pre_folder_id]
    if lst:
        pre_folder = lst.pop()
        pre_folder_id_lst.append(pre_folder.id)
        _depth_find_pre_folder_id(folder_lst, pre_folder.pre_folder_id, pre_folder_id_lst)


@bp.route('/tran_move', methods=['POST'])
@doc.post("fstore", TranMoveSchema.__name__)
@bp.auth.grant_view
def tran_move():
    """批量移动文件夹及文件"""
    try:
        query = RequestQuery(TranMoveSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: TranMove = query.data

        """
        target_folder_id不为null的时候需判断:
        1、目标文件夹是否存在
        2、目标文件夹是否正常，不能将自己移动到自己的子集。
        """
        model = create_store_folder_model()
        if qd.target_folder_id:
            user_id = current_user.get_id()
            folder_lst = model.get_list_query(user_id).to_list()
            # 1、目标文件夹是否存在
            target_folders = [item for item in folder_lst if item.id == qd.target_folder_id]
            if not target_folders:
                return eresponse("目标文件夹不存在")
            target_folder = target_folders.pop()

            # 2、目标文件夹是否正常，不能将自己移动到自己的子集，采用的方式是通过查找目标文件夹的上级是否包括要移动的文件夹。
            pre_folder_id_lst = []
            if target_folder.pre_folder_id:
                _depth_find_pre_folder_id(folder_lst, target_folder.pre_folder_id, pre_folder_id_lst)

            if pre_folder_id_lst:
                for folder_id in qd.folder_ids:
                    if folder_id in pre_folder_id_lst:
                        return eresponse("复制中断,目标文件夹是源文件夹的子文件夹")

        model = create_store_folder_model()
        model.tran_move(qd.target_folder_id, qd.folder_ids, qd.file_ids)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
