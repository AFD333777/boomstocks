import os
from multiprocessing import Process
from mainBot import start
from flask import Flask
from flask import render_template
from data import db_session

app = Flask(__name__)


@app.route("/")
def index():
    params = {"title": "Главная страница"}
    return render_template('index.html', **params)


@app.route("/stocks")
def stocks():
    params = {"title": "Акции"}
    return render_template('stocks.html', **params)


@app.route("/crypto")
def crypto():
    params = {"title": "Криптовалюта"}
    return render_template('crypto.html', **params)


def startSite():
    # db_session.global_init("db/stocks")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


def startBot():
    start()


if __name__ == '__main__':
    pass
    # first = Process(target=startBot)
    # second = Process(target=startSite)
    # first.start()
    # second.start()
