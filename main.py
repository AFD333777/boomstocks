import os
from multiprocessing import Process
from mainBot import start
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Главная страница"


def startSite():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


def startBot():
    start()


if __name__ == '__main__':
    first = Process(target=startBot)
    second = Process(target=startSite)
    first.start()
    second.start()
