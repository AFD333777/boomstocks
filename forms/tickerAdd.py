from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TickerAdd(FlaskForm):
    ticker = StringField('Тикер', validators=[DataRequired()])
    submit = SubmitField('Добавить')
