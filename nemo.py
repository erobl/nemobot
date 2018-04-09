import telegram
import logging
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
import sqlite3

def log(bot, update):
    is_reply = update.message.reply_to_message is not None

    tpl = (update.message.chat.id, 
            update.message.message_id, 
            update.message.date, 
            update.message.text,
            is_reply,
            None if not is_reply else update.message.reply_to_message.message_id,
            False,
            None
            )
    con = sqlite3.connect("messages.db")
    c = con.cursor()
    c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?)", tpl)
    con.commit()


def sticker(bot, update):
    is_reply = update.message.reply_to_message is not None
    tpl = (update.message.chat.id,
            update.message.message_id,
            update.message.date,
            None,
            is_reply,
            None if not is_reply else update.message.reply_to_message.message_id,
            True,
            update.message.sticker.file_id
            )
    con = sqlite3.connect("messages.db")
    c = con.cursor()
    c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?)", tpl)
    con.commit()
    # bot.send_sticker(update.message.chat.id, update.message.sticker.file_id)


updater = Updater(token='secreto')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

log_handler = MessageHandler(Filters.text, log)
dispatcher.add_handler(log_handler)

sticker_handler = MessageHandler(Filters.sticker, sticker)
dispatcher.add_handler(sticker_handler)

updater.start_polling()

