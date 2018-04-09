import telegram
import logging
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
import sqlite3
from model import Model

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

    c.execute("select rate from rate where chatid = ?", 
            (update.message.chat.id,))
    rate = c.fetchall()[0][0]
    m = Model(rate=rate)
    (reply, stickerid) = m.eval(update.message.text)
    if reply:
        bot.send_sticker(update.message.chat.id, stickerid, reply_to_message_id=update.message.message_id)


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

def stats(bot, update):
    con = sqlite3.connect("messages.db")
    c = con.cursor()
    c.execute("select count(*) from messages;")
    count = c.fetchall()[0][0]
    c.execute("select count(*) from messages where messageid in (select reply_messageid from messages where is_sticker);")
    stickers = c.fetchall()[0][0]
    c.execute("select count(*) from messages where is_sticker")
    stickers_total = c.fetchall()[0][0]
    statsstr = """Stats:
Mensajes recolectados: %d
Mensajes que son replies con stickers: %d
Stickers recolectados: %d
Meta para que Edgar active el modelo: %d""" % (count, stickers, stickers_total, stickers*100/80) + "%"
    bot.send_message(update.message.chat.id, statsstr)

def set_rate(bot, update, args):
    if len(args) < 1:
        bot.send_message(update.message.chat.id, 
                "Comando equivocado, uso: /set_rate rate")
        return

    try:
        val = float(args[0])
    except:
        bot.send_message(update.message.chat.id, 
                "Comando equivocado, uso: /set_rate rate")

    con = sqlite3.connect("messages.db")
    c = con.cursor()
    c.execute("update rate set rate = ? where chatid = ?", 
            (val, update.message.chat.id))
    con.commit()
    
def start(bot, update):
    con = sqlite3.connect("messages.db")
    c = con.cursor()
    c.execute("insert into rate (chatid, rate) values (?, 0.5)",
            (update.message.chat.id,))
    con.commit()

updater = Updater(token='secreto')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

set_rate_handler = CommandHandler("set_rate", set_rate, pass_args=True)
dispatcher.add_handler(set_rate_handler)

stats_handler = CommandHandler("stats", stats)
dispatcher.add_handler(stats_handler)

log_handler = MessageHandler(Filters.text, log)
dispatcher.add_handler(log_handler)

sticker_handler = MessageHandler(Filters.sticker, sticker)
dispatcher.add_handler(sticker_handler)


updater.start_polling()

