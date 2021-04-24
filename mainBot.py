import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import db_session
from data.users import User
import logging

ACCESSKEY = "82358a9c66b6a9c130cf8418aa52593f"
keyboardMenu = [['Акции все', 'Криптовалюта'], ['Добавить акцию', 'Добавить криптовалюту']]
markupSite = telegram.InlineKeyboardMarkup(
    [[telegram.InlineKeyboardButton("Перейти", url="https://boomstocks.herokuapp.com")]])
markupMenu = ReplyKeyboardMarkup(keyboardMenu, one_time_keyboard=False, resize_keyboard=True)
markupConfirm = ReplyKeyboardMarkup([[telegram.KeyboardButton("Предоставить телефон", request_contact=True)]],
                                    resize_keyboard=True, one_time_keyboard=True)


def greeting(update, context):
    update.message.reply_text("Здравствуйте!\nЯ бот для просмотра информации акций и криптовалют"
                              "\nВведите /help для получения инструкций", reply_markup=markupConfirm)
    update.message.reply_text(
        "Чтобы воспользоватся ботом, вам нужно предоставить номер телефона и зарегистрироваться на сайте "
        "https://boomstocks.herokuapp.com, указав логин - ваш номер телефона в международном формате.\n"
        "Если вы уже зарегистрированы, нажмите 'Предоставить доступ'",
        reply_markup=markupSite)


def getNumber(update, context):
    context.user_data['phone_number'] = update.message.contact.phone_number


def checkUser(number):
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.login == number).first():
        return False
    else:
        return True


def instructions(update, context):
    if checkUser(context.user_data['phone_number']):
        update.message.reply_text(
            """Команды:
/help - получение инструкций по работе с ботом
/stocks - показать меню акций
/menu - кнопки главного меню
/crypto - показать меню криптовалют
/addstock - добавить акцию для просмотра
/addcrypto - добавить криптовалюту для просмотра
/close - закрыть клавиатуру
            """
        )
    else:
        greeting(update, context)


def openMenu(update, context):
    if checkUser(context.user_data['phone_number']):
        update.message.reply_text("Выберите функцию:", reply_markup=markupMenu)
    else:
        greeting(update, context)


def getStocks(update, context):
    if checkUser(context.user_data['phone_number']):
        # обращение к бд и просмотр избранных акций пользователя
        update.message.reply_text("Список акций")
    else:
        greeting(update, context)


def getCrypto(update, context):
    if checkUser(context.user_data['phone_number']):
        update.message.reply_text("Список крптовалют")
    else:
        greeting(update, context)


def addStock(update, context):
    if checkUser(context.user_data['phone_number']):
        update.message.reply_text("Добавил акцию")
    else:
        greeting(update, context)


def addCrypto(update, context):
    if checkUser(context.user_data['phone_number']):
        update.message.reply_text("Добавил криптовалюту")
    else:
        greeting(update, context)


def getExcuse(update, context):
    update.message.reply_text("Простите, я не умею работать с сообщениями")


def closeKeyboard(update, context):
    update.message.reply_text("Закрыл клавиатуру", reply_markup=ReplyKeyboardRemove())


def start():
    db_session.global_init("db/stocks")
    updater = Updater("1619648579:AAFZ15uTggnT94_aupP9h0byM5ErkoyRVrs", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greeting))
    dp.add_handler(MessageHandler(Filters.contact, getNumber))
    dp.add_handler(CommandHandler("menu", openMenu))
    dp.add_handler(CommandHandler("stocks", getStocks))
    dp.add_handler(CommandHandler("crypto", getCrypto))
    dp.add_handler(CommandHandler("addstock", addStock))
    dp.add_handler(CommandHandler("addcrypto", addCrypto))
    dp.add_handler(CommandHandler("close", closeKeyboard))
    dp.add_handler(CommandHandler("help", instructions))
    updater.start_polling()
    updater.idle()
