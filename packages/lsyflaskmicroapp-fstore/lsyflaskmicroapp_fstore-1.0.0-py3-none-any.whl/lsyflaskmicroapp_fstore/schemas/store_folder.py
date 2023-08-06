# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from ..entitys.store_folder import StoreFolderBase, StoreFolderEdit, StoreFolderDetail, \
    StoreFolderCreate, StoreFolderListQuery, TranDelete, TranMove


class StoreFolderSchema(Schema):
    """ 文件目录 Schema """
    # 目录Id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36), description="目录Id")
    # 上级目录
    pre_folder_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="上级目录")
    # 目录名称
    folder_name = fields.Str(required=True, validate=validate.Length(max=20), description="目录名称")
    # 所属用户
    user_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="所属用户")
    # 创建人
    create_user_id = fields.Str(required=True, validate=validate.Length(max=36), description="创建人")
    # 创建时间
    create_time = fields.DateTime(required=True, description="创建时间")
    # 属性
    attribute = fields.Dict(required=False, allow_none=True, description="属性")
    # 备注
    remark = fields.Str(required=False, allow_none=True, description="备注")

    @post_load
    def make(self, data, **kwargs):
        return StoreFolderBase().__fill__(**data)


class StoreFolderCreateSchema(Schema):
    """ 创建目录 Schema """
    # 上级目录
    pre_folder_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="上级目录id")
    # 目录名称
    folder_name = fields.Str(required=True, validate=validate.Length(max=20), description="目录名称")
    # 是否公开
    is_public = fields.Int(required=True, validate=validate.OneOf((0, 1)), description="是否公开")
    # 属性
    attribute = fields.Dict(required=False, allow_none=True, description="属性")
    # 备注
    remark = fields.Str(required=False, allow_none=True, description="备注")

    @post_load
    def make(self, data, **kwargs):
        return StoreFolderCreate().__fill__(**data)


class StoreFolderEditSchema(StoreFolderCreateSchema):
    # 目录Id
    id = fields.Str(required=True, validate=validate.Length(max=36), description="目录id")

    @post_load
    def make(self, data, **kwargs):
        return StoreFolderEdit().__fill__(**data)


class StoreFolderCreateSchema(Schema):
    """ 创建目录 Schema """
    # 上级目录
    pre_folder_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="上级目录id")
    # 目录名称
    folder_name = fields.Str(required=True, validate=validate.Length(max=20), description="目录名称")
    # 是否公开
    is_public = fields.Int(required=True, validate=validate.OneOf((0, 1)), description="是否公开")
    # 属性
    attribute = fields.Dict(required=False, allow_none=True, description="属性")
    # 备注
    remark = fields.Str(required=False, allow_none=True, description="备注")

    @post_load
    def make(self, data, **kwargs):
        return StoreFolderCreate().__fill__(**data)


class StoreFolderDetailSchema(StoreFolderSchema):
    create_user_id_name = fields.Str(required=False, allow_none=True, description="创建用户名称")
    pre_folder_id_name = fields.Str(required=False, allow_none=True, description="上级目录名称")

    @post_load
    def make(self, data, **kwargs):
        return StoreFolderDetail().__fill__(**data)


class StoreFolderListQuerySchema(Schema):
    # 上级目录id
    pre_folder_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="上级目录id")
    sort = fields.Str(missing="folder_name", allow_none=True, description="排序字段")
    order = fields.Str(missing="asc", allow_none=True, description="排序方式:asc升序,desc降序")

    @post_load
    def make(self, data, **kwargs):
        return StoreFolderListQuery().__fill__(**data)


class TranDeleteSchema(Schema):
    folder_ids = fields.List(fields.Str(), description="目录id")
    file_ids = fields.List(fields.Str(), description="文件id")

    @post_load
    def make(self, data, **kwargs):
        return TranDelete().__fill__(**data)


class TranMoveSchema(TranDeleteSchema):
    target_folder_id = fields.Str(required=False, description="目标目录id", allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return TranMove().__fill__(**data)
