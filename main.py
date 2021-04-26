import os
from multiprocessing import Process
from mainBot import start
from flask import Flask, redirect
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.tickers import Ticker
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.tickerAdd import TickerAdd
import sqlite3
import sqlalchemy.exc
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YandexLyceum144'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)
loginManager = LoginManager()
loginManager.init_app(app)
ACCESSKEY_POLYGON_API = "wdr4VAWtU28sQAFg1eYWWYDrQuIols_V"


@app.after_request
def redirectToSign(response):
    if response.status_code == 401:
        return redirect("/unauthorized")
    return response


@app.route("/unauthorized")
def unauthorized():
    return render_template('unauthorized.html')


@app.route("/")
def index():
    params = {"title": "Главная страница"}
    return render_template('index.html', **params)


@app.route("/stocks")
@login_required
def stocks():
    params = {"title": "Акции"}
    return render_template('stocks.html', **params)


@app.route("/addStock", methods=['GET', 'POST'])
@login_required
def addStock():
    form = TickerAdd()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Ticker).filter(Ticker.name == form.ticker.data).first() is None:
            ticker = Ticker()
            ticker.name = form.ticker.data
            db_sess.add(ticker)
            db_sess.commit()
        db_sess = db_session.create_session()
        ticker_id = str(db_sess.query(Ticker).filter(Ticker.name == form.ticker.data).first().id)
        user_login = current_user.login
        user = db_sess.query(User).filter(User.login == user_login).first()
        if user.tickers_id is None:
            user.tickers_id = ticker_id
        else:
            tickers_id = user.tickers_id.split(" ")
            if ticker_id in tickers_id:
                return render_template('addStock.html', title='Добавление акции', form=form,
                                       message="Данный тикер уже добавлен к вам")
            else:
                user.tickers_id += " " + ticker_id
        db_sess.commit()
        return render_template('addStock.html', title='Добавление акции', form=form,
                               message="Добавили тикер " + form.ticker.data)
    return render_template('addStock.html', title='Добавление акции', form=form)


@app.route("/crypto")
@login_required
def crypto():
    params = {"title": "Криптовалюта"}
    return render_template('crypto.html', **params)


@app.route("/addCrypto", methods=['GET', 'POST'])
@login_required
def addCrypto():
    form = TickerAdd()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Ticker).filter(Ticker.name == form.ticker.data).first() is None:
            ticker = Ticker()
            ticker.name = form.ticker.data
            db_sess.add(ticker)
            db_sess.commit()
        db_sess = db_session.create_session()
        ticker_id = str(db_sess.query(Ticker).filter(Ticker.name == form.ticker.data).first().id)
        user_login = current_user.login
        user = db_sess.query(User).filter(User.login == user_login).first()
        if user.tickers_id is None:
            user.tickers_id = ticker_id
        else:
            tickers_id = user.tickers_id.split(" ")
            if ticker_id in tickers_id:
                return render_template('addCrypto.html', title='Добавление криптовалюты', form=form,
                                       message="Данный тикер уже добавлен к вам")
            else:
                user.tickers_id += " " + ticker_id
        db_sess.commit()
        return render_template('addCrypto.html', title='Добавление криптовалюты', form=form,
                               message="Добавили тикер " + form.ticker.data)
    return render_template('addCrypto.html', title='Добавление криптовалюты', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = User()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if not user.checkNumber(form.login.data):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Неверный номер телефона")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user.login = form.login.data
        user.setPassword(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    params = {
        "title": "Регистрация",
    }
    return render_template('register.html', **params, form=form)


@loginManager.user_loader
def loadUser(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.checkPassword(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def startSite():
    try:
        db_session.global_init("db/stocks")
    except sqlite3.OperationalError:
        pass
    except sqlalchemy.exc.OperationalError:
        pass

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


def startBot():
    start()


def main():
    first = Process(target=startBot)
    second = Process(target=startSite)
    first.start()
    second.start()


if __name__ == '__main__':
    main()
