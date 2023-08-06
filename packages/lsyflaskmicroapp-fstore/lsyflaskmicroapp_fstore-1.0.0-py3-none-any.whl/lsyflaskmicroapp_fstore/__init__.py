# -*- coding: utf-8 -*-

from lsyflaskmicroapp_fstore import orm
from lsyflaskmicroapp_fstore.apis import store_file
from lsyflaskmicroapp_fstore.apis import store_folder


def init_app(app):
    orm.init_db(app)

    # 文件
    app.register_blueprint(store_file.bp, url_prefix='/api/fstore/store_file')
    # 文件目录
    app.register_blueprint(store_folder.bp, url_prefix='/api/fstore/store_folder')
