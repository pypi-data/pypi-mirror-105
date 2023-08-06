from flask_sqlalchemy import SQLAlchemy
from lsyflasksdkcore.model import Model
from sqlalchemy import Column, String, DateTime, Text, BigInteger

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


class UEditorFile(db.Model):
    __tablename__ = 'ueditor_file'

    id = Column(String, primary_key=True)
    folder_code = Column(String(10), nullable=False)
    file_name = Column(String(100), nullable=False)
    file_format = Column(String(50), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_alias_name = Column(Text, nullable=False)
    create_time = Column(DateTime, nullable=False)
    create_user_id = Column(String)
    remark = Column(Text)
