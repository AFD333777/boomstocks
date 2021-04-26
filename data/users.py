import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import phonenumbers


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tickers_id = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def setPassword(self, password):
        self.hashed_password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.hashed_password, password)

    def checkNumber(self, number):
        try:
            parse = phonenumbers.parse(number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
        return phonenumbers.is_valid_number(parse)
