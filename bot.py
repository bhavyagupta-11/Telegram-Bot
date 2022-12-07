import logging
from flask import Flask, request
from telegram.ext import MessageHandler, Filters, Updater, Dispatcher, CommandHandler
from telegram import Bot, Update, ReplyKeyboardMarkup
from conversationalbot import get_reply, fetch_news, topics_keyboard

#enable logging which send the data of the recieved message like name time and level of importance
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger= logging.getLogger(__name__)

#HTTP API
TOKEN = "5695725037:AAHm60y5lxaT6EB85X49dM5Ep4P2bC1oDgs"

#Creating a webhook program ..for that need to create a server
app=Flask(__name__)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}',methods=['GET','POST'])
def webhook():
    #it recieves updates from the telegram

    #creates update object from json-format request
    update=Update.de_json(request.get_json(),bot)
    #process update
    dp.process_update(update)
    return "ok"

#THIS IS A POLLING PROGRAM - continuous sending of requests

def start(bot,update):
    author=update.message.from_user.first_name
    reply="Hii! {}".format(author)
    bot.sendMessage(chat_id=update.message.chat_id, text=reply)

def _help(bot,update):
    help_text="For any doubts contact telegram or BG iykyk"
    bot.sendMessage(chat_id=update.message.chat_id, text=help_text)

def echo_text(bot,update):
    reply=update.message.text
    bot.sendMessage(chat_id=update.message.chat_id,text=reply)

def news(bot,update):
    bot.sendMessage(chat_id=update.message.chat_id,text="Choose a category",reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard,one_time_keyboard=True))

#for dialogflow conversational bot
def reply_text(bot,update):
    intent,reply=get_reply(update.message.text,update.message.chat_id)
    if intent == "get_answer":
        articles=fetch_news(reply)
        for article in articles:
            bot.sendMessage(chat_id=update.message.chat_id,text=article['link'])
    else:
        bot.sendMessage(chat_id=update.message.chat_id,text=reply)

def echo_sticker(bot,update):
    reply=update.message.sticker.file_id
    bot.sendSticker(chat_id=update.message.chat_id,text=reply)

def error(bot,update):
    logger.error("Update '%s' caused error '%s'",update,update.error)

# FOR THE POLLING METHOD AND THEN THE WEBHOOK METHOD
#updater=Updater(TOKEN)
#dp= updater.dispatcher

bot=Bot(TOKEN)

#create a public url for your server using ngrok

try:
    bot.set_webhook("https://0d49-42-105-139-30.in.ngrok.io/" + TOKEN)
except Exception as e:
    print(e)

dp=Dispatcher(bot,None)

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)

#code to end program
    
#updater.start_polling()
#updater.idle()

if __name__=="__main__":
    app.run(port=8443)
