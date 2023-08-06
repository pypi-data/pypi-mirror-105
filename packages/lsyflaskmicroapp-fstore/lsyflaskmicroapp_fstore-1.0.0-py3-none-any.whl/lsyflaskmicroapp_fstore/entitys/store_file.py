# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass


class StoreFileBase(AutoClass):
    """文件"""

    def __init__(self):
        # 文件id
        self.id = ""
        # 所属目录
        self.folder_id = ""
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


class StoreFileList(StoreFileBase):
    def __init__(self):
        super().__init__()
        self.file_url = ''


class StoreFileEdit(StoreFileBase):
    pass


class StoreFileDetail(StoreFileBase):
    def __init__(self):
        super().__init__()
        self.create_user_id_name = ""
        self.folder_id_name = ""


class StoreFileListQuery(AutoClass):
    def __init__(self):
        self.folder_id = None
        self.sort = ""
        self.order = ""


class StoreFileQuickSearchQuery(AutoClass):
    def __init__(self):
        self.folder_id = None
        self.search = ""


class StoreFileDownloadQuery(AutoClass):
    def __init__(self):
        self.file_id = ''
        self.file_name = ''
        # self.cookies = ''
