import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

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
        "https://boomstocks.herokuapp.com, указав логин - ваш номер телефона.\n"
        "Если вы уже зарегистрированы, нажмите 'Предоставить доступ'",
        reply_markup=markupSite)


def getNumber(update, context):
    print(update.message.contact.phone_number)
    print(update.message.contact.user_id)
    context.user_data[0] = update.message.contact.phone_number
    context.user_data[1] = update.message.contact.user_id
    openMenu(update, context)
    # запрос к бд, есть ли пользователь


def instructions(update, context):
    update.message.reply_text(
        """Команды:
/help - получение инструкций по работе с ботом
/menu - кнопки главного меню
/stocks - показать меню акций
/crypto - показать меню криптовалют
/addstock - добавить акцию для просмотра
/addcrypto - добавить криптовалюту для просмотра
/close - закрыть клавиатуру
        """
    )


def openMenu(update, context):
    update.message.reply_text("Выберите функцию:", reply_markup=markupMenu)
    print(context.user_data[0])


def getStocks(update, context):
    # обращение к бд и просмотр избранных акций пользователя
    print("Выдал кнопки акций")


def getCrypto(update, context):
    print("Выдал кнопки криптовалют")


def addStock(update, context):
    update.message.reply_text("Добавили акцию чего то")
    pass


def addCrypto(update, context):
    update.message.reply_text("Добавили крипту")
    pass


def getExcuse(update, context):
    update.message.reply_text("Простите, я не умею работать с сообщениями")


def closeKeyboard(update, context):
    update.message.reply_text("Закрыл клавиатуру", reply_markup=ReplyKeyboardRemove())


def start():
    updater = Updater("1619648579:AAFZ15uTggnT94_aupP9h0byM5ErkoyRVrs", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greeting))
    # если пользователь есть, если нет, то оставляем его на начальном меню
    dp.add_handler(CommandHandler("menu", openMenu))
    dp.add_handler(CommandHandler("stocks", getStocks))
    dp.add_handler(CommandHandler("crypto", getCrypto))
    dp.add_handler(CommandHandler("addstock", addStock))
    dp.add_handler(CommandHandler("addcrypto", addCrypto))
    dp.add_handler(CommandHandler("close", closeKeyboard))
    dp.add_handler(CommandHandler("help", instructions))
    dp.add_handler(MessageHandler(Filters.contact, getNumber))
    dp.add_handler(MessageHandler(Filters.text, getExcuse))
    updater.start_polling()
    updater.idle()
