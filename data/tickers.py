import sqlalchemy
from .db_session import SqlAlchemyBase


class Ticker(SqlAlchemyBase):
    __tablename__ = 'tickers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
