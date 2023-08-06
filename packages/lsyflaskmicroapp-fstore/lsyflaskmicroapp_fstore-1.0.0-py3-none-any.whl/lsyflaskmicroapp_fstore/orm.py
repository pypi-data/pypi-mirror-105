from flask_sqlalchemy import SQLAlchemy
from lsyflasksdkcore.model import Model
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

db = SQLAlchemy()
model = Model()


def init_db(app):
    db.init_app(app)
    model.init_app(app)


class AuthUser(db.Model):
    __tablename__ = 'auth_user'

    id = Column(String, primary_key=True)
    user_name = Column(String(30), nullable=False)

    def __repr__(self):
        return '<AuthUser %r>' % self.user_name


class StoreFolder(db.Model):
    __tablename__ = 'store_folder'

    id = Column(String, primary_key=True)
    pre_folder_id = Column(ForeignKey('store_folder.id', ondelete='RESTRICT', onupdate='RESTRICT'))
    folder_name = Column(String(20), nullable=False)
    user_id = Column(String)
    create_user_id = Column(String)
    create_time = Column(DateTime, nullable=False)
    attribute = Column(JSONB(astext_type=Text()))
    remark = Column(Text)

    pre_folder = relationship('StoreFolder', remote_side=[id])


class StoreFile(db.Model):
    __tablename__ = 'store_file'

    id = Column(String, primary_key=True)
    folder_id = Column(ForeignKey('store_folder.id', ondelete='RESTRICT', onupdate='RESTRICT'))
    file_name = Column(String(100), nullable=False)
    file_format = Column(String(50), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_alias_name = Column(Text, nullable=False)
    create_time = Column(DateTime, nullable=False)
    create_user_id = Column(String)
    remark = Column(Text)

    folder = relationship('StoreFolder')
