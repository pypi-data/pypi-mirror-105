# -*- coding: utf-8 -*-

"""
Store_File
~~~~~~~~~~~~~
文件
"""

import logging
import os
from datetime import datetime
from urllib.parse import quote

from flask import make_response, current_app, send_file, redirect
from flask import request
from flask_login import current_user
from lsyflaskplugin_minio.api import put_dropzone_object, get_presigned_object, fget_object
from lsyflasksdkcore import RequestQuery, eresponse, sresponse
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.exceptions import DBError
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery
from lsyflasksdkcore.swagger import doc
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_fstore.entitys.store_file import StoreFileEdit, StoreFileListQuery, StoreFileDownloadQuery, \
    StoreFileQuickSearchQuery
from lsyflaskmicroapp_fstore.models import create_store_file_model, create_store_folder_model
from lsyflaskmicroapp_fstore.schemas.store_file import StoreFileEditSchema, \
    StoreFileDetailSchema, StoreFileListQuerySchema, StoreFileDownloadQuerySchema, \
    StoreFileQuickSearchQuerySchema

logger = logging.getLogger(__name__)

bp = Blueprint('store_file', __name__)

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


def find_folder(folder_id, folders):
    for item in folders:
        if item.id == folder_id:
            return item
    return None


def find_depth(item, current_id, folders, result, depth):
    result.append({"name": item.folder_name, "pre_id": item.id, "chailds": current_id, "depth": depth})
    if item.pre_folder_id:
        folder = find_folder(item.pre_folder_id, folders)
        if folder:
            find_depth(folder, current_id, folders, result, depth + 1)


@bp.route('/quick_search', methods=['GET', 'POST'])
@doc.post("fstore", StoreFileQuickSearchQuerySchema.__name__, [StoreFileDetailSchema.__name__])
@bp.auth.grant_view
def quick_search():
    """快速搜索"""
    try:
        query = RequestQuery(StoreFileQuickSearchQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StoreFileQuickSearchQuery = query.data
        if not qd.search:
            return eresponse("搜索关键字不能为空")

        model = create_store_folder_model()
        folders = model.get_all().data
        result = []
        for item in folders:
            find_depth(item, item.id, folders, result, 0)

        model = create_store_file_model()
        search_lst = model.get_list_search(None, qd.search, "file_name", "asc").to_list()
        for item in search_lst:
            ps = [item1["name"] for item1 in result if item1["chailds"] == item.folder_id]
            ps.reverse()
            item.folder_full_name = os.path.join("./", "/".join(ps))
            item.type = 0

        data = StoreFileDetailSchema().dump(search_lst, many=True)
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/list', methods=['GET', 'POST'])
@doc.post("fstore", StoreFileListQuerySchema.__name__, [StoreFileDetailSchema.__name__])
@bp.auth.grant_view
def lst():
    """获取文件列表"""
    try:
        query = RequestQuery(StoreFileListQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        model = create_store_folder_model()
        folder_lst = model.get_all().data
        result = []
        for item in folder_lst:
            find_depth(item, item.id, folder_lst, result, 0)

        qd: StoreFileListQuery = query.data
        model = create_store_file_model()
        dbr = model.get_list_folder_id(qd.folder_id, "", qd.sort or "file_name", qd.order or "asc")
        return sresponse(dbr.json)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@doc.post("fstore", StoreFileEditSchema.__name__)
@bp.auth.grant_edit
def modify():
    """修改"""
    try:
        query = RequestQuery(StoreFileEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: StoreFileEdit = query.data
        model = create_store_file_model()
        model.modify(entity.id, entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/delete', methods=['POST'])
@doc.post("fstore", PksQuerySchema.__name__)
@bp.auth.grant_delete
def delete():
    """删除"""
    try:
        query = RequestQuery(PksQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: PksQuery = query.data
        model = create_store_file_model()
        model.tran_delete(qd.ids)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


def upload_record_to_db(file_name, file_alias_name, file_size, folder_id, user_id):
    _name, file_type = os.path.splitext(file_name)
    file_class = file_classify.get(file_type[1:], 'unknown')
    entity = StoreFileEdit()
    entity.id = get_uuid_str()
    entity.file_name = file_name
    entity.file_format = file_class
    entity.file_alias_name = file_alias_name
    entity.file_size = file_size
    entity.create_time = datetime.now()
    entity.create_user_id = user_id
    entity.folder_id = folder_id
    try:
        model = create_store_file_model()
        model.add(entity)
    except DBError as ex:
        raise ex


@bp.route('/upload', methods=['POST'])
@bp.auth.grant_view
def upload():
    """上传文件"""
    try:
        f = request.files['file']
        folder_id = request.form.get('id', None)
        if folder_id == "null":
            folder_id = None

        bucket_name = current_app.config['MINIO_FSTORE_BUCKET_NAME']
        minio_file = put_dropzone_object(bucket_name, f)
        if minio_file:
            upload_record_to_db(f.filename, minio_file.object_name, minio_file.object_size,
                                folder_id, current_user.get_id())
            return make_response(("上传成功", 200))
        return sresponse(None)
    except Exception as ex:
        logger.error(ex)
        return make_response(("服务器内部错误", 500))


@bp.route('/share', methods=['POST'])
@bp.auth.grant_view
def share():
    pass


@bp.route('/public_file', methods=['GET'])
def public_file():
    try:
        oid = request.args.get("o", None)
        if oid is None:
            return eresponse("参数错误")
        bucket_name = current_app.config['MINIO_FSTORE_BUCKET_NAME']
        presingned_url = get_presigned_object(bucket_name, oid)
        return redirect(presingned_url, code=302)
    except Exception as ex:
        logger.error(ex)
        return make_response(("服务器内部错误", 500))


# 流式读取
def rb_file(filename):
    store_path = filename
    with open(store_path, 'rb') as targetfile:
        while 1:
            data = targetfile.read(20 * 1024 * 1024)  # 每次读取20M
            if not data:
                break
            yield data


@bp.route('/minio_download', methods=['POST'])
@bp.auth.grant_view
def minio_download():
    query = RequestQuery(StoreFileDownloadQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    qd: StoreFileDownloadQuery = query.data

    model = create_store_file_model()
    store_file = model.get_one(qd.file_id).data
    if not store_file:
        return eresponse("文件不存在。")

    bucket_name = current_app.config['MINIO_FSTORE_BUCKET_NAME']
    presingned_url = get_presigned_object(bucket_name, store_file.file_alias_name)
    return redirect(presingned_url, code=302)


@bp.route('/download', methods=['POST'])
@bp.auth.grant_view
def download():
    """
    文件下载，通过将minio中的文件先保存到本地，然后再发送给浏览器，这样做的目的是可以对输出的文件名自定义。
    没有对保存在本地的文件做清理，方便重复再利用，直接发送给浏览器。
    :return:
    """
    query = RequestQuery(StoreFileDownloadQuerySchema)
    if not query.is_valid():
        return eresponse(query.valid_message)

    qd: StoreFileDownloadQuery = query.data

    model = create_store_file_model()
    store_file = model.get_one(qd.file_id).data
    if not store_file:
        return eresponse("文件不存在。")

    bucket_name = current_app.config['MINIO_FSTORE_BUCKET_NAME']
    full_path = fget_object(bucket_name, store_file.file_alias_name)

    rv = send_file(full_path, as_attachment=True, attachment_filename=quote(store_file.file_name))
    rv.headers['Content-Disposition'] += "attachment; filename={0}; filename*=utf-8''{0}".format(quote(qd.file_name))
    # rv.headers['Content-Type'] = 'application/octet-stream'
    return rv


@bp.route('/preview', methods=['GET'])
def preview():
    """
    文件预览，目前采用xdoc的技术方案。
    :return:
    """
    _xdoc = request.args.get("_xdoc")
    _expire = request.args.get("_expire")
    bucket_name = current_app.config['MINIO_FSTORE_BUCKET_NAME']
    presingned_url = get_presigned_object(bucket_name, _xdoc)
    # xdoc_url = "http://view.xdocin.com/xdoc?_xdoc={}&_expire={}".format(parse.quote(presingned_url), _expire)
    return redirect(presingned_url, code=302)
