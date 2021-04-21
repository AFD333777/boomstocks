from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

ACCESSKEY = "82358a9c66b6a9c130cf8418aa52593f"
reply_keyboard = [['Акции', 'Криптовалюта']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)


def getStocks(update, context):
    # обращение к бд и просмотр избранных акций пользователя
    print("Выдал кнопки акций")


def getCrypto(update, context):
    print("Выдал кнопки криптовалют")


def greeting(update, context):
    update.message.reply_text("Здравствуйте!\nЯ бот для просмотра информации акций и криптовалют"
                              "\nВведите /help для получения инструкций", reply_markup=markup)


def close_keyboard(update, context):
    update.message.reply_text("Закрыл клавиатуру", reply_markup=ReplyKeyboardRemove())


def instructions(update, context):
    update.message.reply_text(
        """Команды:
/help - получение инструкций по работе с ботом
/stocks - показать меню акций
/crypto - показать меню криптовалют
/addstock - добавить акцию для просмотра
/addcrypto - добавить криптовалюту для просмотра
/close - закрыть клавиатуру
        """
    )


def addStock(update, context):
    update.message.reply_text("Добавили акцию")
    pass


def addCrypto(update, context):
    update.message.reply_text("Добавили крипту")
    pass


def start():
    # 1619648579:AAFZ15uTggnT94_aupP9h0byM5ErkoyRVrs
    updater = Updater("1764984239:AAGcPAVr_PNkUwsx_FXlQQi3lB_ey9Hfuj8", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greeting))
    dp.add_handler(CommandHandler("stocks", getStocks))
    dp.add_handler(CommandHandler("crypto", getCrypto))
    dp.add_handler(CommandHandler("addstock", addStock))
    dp.add_handler(CommandHandler("addcrypto", addCrypto))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("help", instructions))
    updater.start_polling()
    updater.idle()
