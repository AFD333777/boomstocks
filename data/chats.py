import sqlalchemy
from .db_session import SqlAlchemyBase


class Chat(SqlAlchemyBase):
    __tablename__ = 'chats'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    chat_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False, unique=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
