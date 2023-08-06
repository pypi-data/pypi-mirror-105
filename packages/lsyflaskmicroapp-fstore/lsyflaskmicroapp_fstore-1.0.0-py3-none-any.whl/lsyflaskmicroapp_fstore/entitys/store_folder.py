# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass


class StoreFolderBase(AutoClass):
    """文件目录"""

    def __init__(self):
        # 目录Id
        self.id = ""
        # 上级目录
        self.pre_folder_id = ""
        # 目录名称
        self.folder_name = ""
        # 所属用户
        self.user_id = ""
        # 创建人
        self.create_user_id = ""
        # 创建时间
        self.create_time = None
        # 属性
        self.attribute = None
        # 备注
        self.remark = ""


class StoreFolderCreate(AutoClass):
    def __init__(self):
        # 是否公开
        self.is_public = 0
        # 上级目录
        self.pre_folder_id = ""
        # 目录名称
        self.folder_name = ""
        # 属性
        self.attribute = None
        # 备注
        self.remark = ""


class StoreFolderEdit(StoreFolderCreate):
    def __init__(self):
        super().__init__()
        self.id = ""


class StoreFolderDetail(StoreFolderBase):
    def __init__(self):
        super().__init__()
        self.create_user_id_name = ""
        self.pre_folder_id_name = ""


class StoreFolderListQuery(AutoClass):
    def __init__(self):
        self.pre_folder_id = None
        self.sort = ""
        self.order = ""


class TranDelete(AutoClass):
    def __init__(self):
        self.folder_ids = None
        self.file_ids = None


class TranMove(TranDelete):
    def __init__(self):
        super().__init__()
        self.target_folder_id = ""
