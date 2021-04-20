from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler


def echo(update, context):
    update.message.reply_text("Я получил сообщение: " + update.message.text)


def start():
    updater = Updater("1619648579:AAFZ15uTggnT94_aupP9h0byM5ErkoyRVrs", use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()
