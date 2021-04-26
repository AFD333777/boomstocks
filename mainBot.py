from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton
import sqlite3
import requests
import sqlalchemy.exc
import telegram
import datetime
from data import db_session
from data.chats import Chat
from data.users import User
from data.tickers import Ticker

ACCESSKEY_POLYGON_API = "wdr4VAWtU28sQAFg1eYWWYDrQuIols_V"
keyboardMenu = [
    [InlineKeyboardButton("Показать избранное", callback_data="assets")],
    [InlineKeyboardButton("Добавить акцию", callback_data="addstock")],
    [InlineKeyboardButton("Добавить криптовалюту", callback_data="addcrypto")]
]
markupSite = telegram.InlineKeyboardMarkup(
    [[InlineKeyboardButton("Перейти", url="https://boomstocks.herokuapp.com")]])
markupMenu = telegram.InlineKeyboardMarkup(keyboardMenu)
markupConfirm = ReplyKeyboardMarkup([[telegram.KeyboardButton("Предоставить телефон", request_contact=True)]],
                                    resize_keyboard=True, one_time_keyboard=True)


def greeting(update, context):
    update.message.reply_text("Здравствуйте!\nЯ бот для просмотра информации акций и криптовалют"
                              "\nВведите /help для получения инструкций", reply_markup=markupConfirm)
    update.message.reply_text(
        "Чтобы воспользоватся ботом:\n"
        "1) Зарегистрироваться на сайте https://boomstocks.herokuapp.com,"
        " указав логин - ваш номер телефона в международном формате.\n"
        "2) Предоставить номер телефона только после регистрации на сайте и нажать кнопку 'Предоставить доступ'",
        reply_markup=markupSite)


def getNumber(update, context):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == update.message.contact.phone_number).first()
    if user is None:
        greeting(update, context)
    else:
        chat = Chat()
        chat.chat_id = update.message.contact.user_id
        chat.phone_number = update.message.contact.phone_number
        db_sess.add(chat)
        db_sess.commit()


def checkUser(chat_id):
    db_sess = db_session.create_session()
    if db_sess.query(Chat).filter(Chat.chat_id == chat_id).first():
        number = db_sess.query(Chat).filter(Chat.chat_id == chat_id).first().phone_number
        if db_sess.query(User).filter(User.login == number).first():
            return True
    return False


def instructions(update, context):
    if checkUser(update.message.chat.id):
        update.message.reply_text(
            """Команды:
/help - получение инструкций по работе с ботом
/menu - кнопки главного меню
/assets - показать избранное
/addstock - добавить акцию для просмотра
/addcrypto - добавить криптовалюту для просмотра
/close - закрыть клавиатуру
            """
        )
    else:
        greeting(update, context)


def openMenu(update, context):
    if checkUser(update.message.chat.id):
        update.message.reply_text("Выберите действие:", reply_markup=markupMenu)
    else:
        greeting(update, context)


def checkCallback(update, context):
    choice = update.callback_query.data
    if choice == "assets":
        getAssets(update=update.callback_query, context=context)
    elif choice == "addstock":
        addStock(update=update.callback_query, context=context)
    elif choice == "addcrypto":
        addCrypto(update=update.callback_query, context=context)
    elif choice[0] == "s":
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        url = f"https://api.polygon.io/v1/open-close/{choice[1:]}/{date}?unadjusted=true&apiKey={ACCESSKEY_POLYGON_API}"
        response = requests.get(url)
        if not response.ok:
            url = f"https://api.polygon.io/v2/aggs/ticker/{choice[1:]}/prev?" \
                  f"unadjusted=true&apiKey={ACCESSKEY_POLYGON_API}"
            update.callback_query.message.reply_text("Информация по текущее закрытие торгов недоступна.\n"
                                                     "Предоставляю последнее закрытие торгов.")
            response = requests.get(url)
            data = response.json()['results'][0]
            update.callback_query.message.reply_text(f"Тикер {choice[1:]}\n"
                                                     f"Open - {data['o']}\n"
                                                     f"Close - {data['c']}\n"
                                                     f"High - {data['h']}\n"
                                                     f"Low - {data['l']}")
        else:
            data = response.json()
            update.callback_query.message.reply_text(f"Тикер {choice[1:]}\n"
                                                     f"Open - {data['open']}\n"
                                                     f"Close - {data['close']}\n"
                                                     f"High - {data['high']}\n"
                                                     f"Low - {data['low']}")


def getAssets(update, context):
    if checkUser(update.message.chat.id):
        db_sess = db_session.create_session()
        phone_number = db_sess.query(Chat).filter(Chat.chat_id == update.message.chat.id).first().phone_number
        user = db_sess.query(User).filter(User.login == phone_number).first()
        keyboardAssets = []
        for ticker_id in user.tickers_id.split(" "):
            assetName = db_sess.query(Ticker).filter(Ticker.id == int(ticker_id)).first().name
            keyboardAssets.append([InlineKeyboardButton(assetName, callback_data='s' + assetName)])
        markupAssets = telegram.InlineKeyboardMarkup(keyboardAssets)
        update.message.reply_text("Выберите акцию для просмотра", reply_markup=markupAssets)
    else:
        greeting(update, context)


def addStock(update, context):
    if checkUser(update.message.chat.id):
        update.message.reply_text(
            "Для добавления акции для просмотра:\n"
            "1) Зайдите на сайт https://boomstocks.herokuapp.com\n"
            "2) Авторизируйтесь\n"
            "3) Добавьте акцию в избранные",
            reply_markup=markupSite)
    else:
        greeting(update, context)


def addCrypto(update, context):
    if checkUser(update.message.chat.id):
        update.message.reply_text(
            "Для добавления криптовалюты для просмотра:\n"
            "1) Зайдите на сайт https://boomstocks.herokuapp.com\n"
            "2) Авторизируйтесь\n"
            "3) Добавьте криптовалюту в избранные",
            reply_markup=markupSite)
    else:
        greeting(update, context)


def closeKeyboard(update, context):
    update.message.reply_text("Закрыл клавиатуру", reply_markup=ReplyKeyboardRemove())


def start():
    try:
        db_session.global_init("db/stocks")
    except sqlite3.OperationalError:
        pass
    except sqlalchemy.exc.OperationalError:
        pass
    updater = Updater("1619648579:AAFZ15uTggnT94_aupP9h0byM5ErkoyRVrs", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greeting))
    dp.add_handler(CommandHandler("menu", openMenu))
    dp.add_handler(CommandHandler("assets", getAssets))
    dp.add_handler(CommandHandler("addstock", addStock))
    dp.add_handler(CommandHandler("addcrypto", addCrypto))
    dp.add_handler(CommandHandler("close", closeKeyboard))
    dp.add_handler(CommandHandler("help", instructions))
    dp.add_handler(CallbackQueryHandler(checkCallback))
    dp.add_handler(MessageHandler(Filters.contact, getNumber))
    updater.start_polling()
    updater.idle()
