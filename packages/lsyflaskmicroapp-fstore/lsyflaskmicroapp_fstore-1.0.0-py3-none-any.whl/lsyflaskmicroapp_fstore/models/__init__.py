# -*- coding: utf-8 -*-


def create_store_file_model():
    """ 文件 Model
    :return:
    """
    from .store_file import StoreFileModel
    return StoreFileModel()


def create_store_folder_model():
    """ 文件目录 Model
    :return:
    """
    from .store_folder import StoreFolderModel
    return StoreFolderModel()
