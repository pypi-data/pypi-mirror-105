# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from ..entitys.store_file import StoreFileBase, StoreFileEdit, StoreFileDetail, StoreFileListQuery, \
    StoreFileList, StoreFileDownloadQuery


class StoreFileSchema(Schema):
    """ 文件 Schema """
    # 文件id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36), description="文件id")
    # 所属目录
    folder_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="所属目录")
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
        return StoreFileBase().__fill__(**data)


class StoreFileListSchema(StoreFileSchema):
    file_url = fields.Str(required=False, allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return StoreFileList().__fill__(**data)


class StoreFileEditSchema(StoreFileSchema):

    @post_load
    def make(self, data, **kwargs):
        return StoreFileEdit().__fill__(**data)


class StoreFileDetailSchema(StoreFileSchema):
    # 创建人
    create_user_id_name = fields.Str(required=False, allow_none=True, description="创建人名字")
    # 所属目录id
    folder_id_name = fields.Str(required=False, allow_none=True, description="目录名称")
    # 文件所在完整目录
    folder_full_name = fields.Str(description="文件所在目录完整路径")
    # type
    type = fields.Str(description="类型")

    @post_load
    def make(self, data, **kwargs):
        return StoreFileDetail().__fill__(**data)


class StoreFileListQuerySchema(Schema):
    # 目录id
    folder_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="目录id")
    sort = fields.Str(missing="file_name", allow_none=True, description="排序字段，比如：file_name")
    order = fields.Str(missing="asc", allow_none=True, description="排序方式，asc升序 desc降序")

    @post_load
    def make(self, data, **kwargs):
        return StoreFileListQuery().__fill__(**data)


class StoreFileQuickSearchQuerySchema(Schema):
    # 目录id
    folder_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="目录id")
    search = fields.Str(required=True, description="搜索关键字")

    @post_load
    def make(self, data, **kwargs):
        return StoreFileListQuery().__fill__(**data)


class StoreFileDownloadQuerySchema(Schema):
    file_id = fields.Str(required=True, allow_none=False, description="文件id")
    file_name = fields.Str(required=True, allow_none=False, description="文件名")

    @post_load
    def make(self, data, **kwargs):
        return StoreFileDownloadQuery().__fill__(**data)
