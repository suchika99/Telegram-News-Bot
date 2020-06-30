import logging
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,Dispatcher
from flask import Flask,request
from telegram import Bot,Update, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger=logging.getLogger(__name__)

TOKEN="1269183685:AAEDu2nuxt5_cYMX6I60I_0C0XZitPaAbBE"

app=Flask(__name__)
@app.route('/')
def index():
    return "hello"

@app.route(f'/{TOKEN}',methods=['GET','POST'])
def webhook():
    update=Update.de_json(request.get_json(),bot)
    dp.process_update(update)
    return "ok"

def start(bot,update):
    print(update)
    author=update.message.from_user.first_name
    reply="Hi! {}".format(author)
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def _help(bot,update):
    help_txt="Hey! This is a help text."
    bot.send_message(chat_id=update.message.chat_id, text=help_txt)

def news(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text="Choose a category",
            reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard,one_time_keyboard=True))


def reply_text(bot,update):
    intent, reply=get_reply(update.message.text, update.message.chat_id)
    if intent=="get_news":
        articles=fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(bot,update):
    bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)

def error(bot,update):
    logger.error("Update %s caused error %s",update,update.error)


    
bot=Bot(TOKEN)
try:
    bot.set_webhook("https://shrouded-springs-90527.herokuapp.com/"+TOKEN)
except Exception as ex:
    print(ex)

dp=Dispatcher(bot,None)

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("news",news))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)
    

if __name__ == "__main__":
    app.run(port=8443)
