import os
from multiprocessing import Process
from mainBot import start
from flask import Flask, redirect
from flask import render_template
from data import db_session
from register import RegisterForm
from data.users import User
from login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YandexLyceum144'


@app.route("/<int:cond>")
def index(cond):
    if cond == 1:
        params = {"title": "Главная страница", "cond": 1}
    else:
        params = {"title": "Главная страница", "cond": 0}

    return render_template('index.html', **params)


@app.route("/stocks")
def stocks():
    params = {"title": "Акции"}
    return render_template('stocks.html', **params)


@app.route("/crypto")
def crypto():
    params = {"title": "Криптовалюта"}
    return render_template('crypto.html', **params)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = User()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    params = {
        "title": "Регистрация",
    }
    return render_template('register.html', **params, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


def startSite():
    # db_session.global_init("db/stocks")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


def startBot():
    start()


if __name__ == '__main__':
    first = Process(target=startBot)
    # second = Process(target=startSite)
    first.start()
    # second.start()
