# -*- coding: utf-8 -*- 

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputFile
from io import BytesIO
import logging
import pickle
import os
from tts import *
from get_tts import *
reload(sys)
sys.setdefaultencoding('utf-8')

WAITING = False
TYPE=None
BEATFNAME='bfree'
bio = BytesIO()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def echo(bot, update):
    splited_text = update.message.text.lower()
    print "MSG"
    chat_id = update.message.chat.id
    if (WAITING):
        if(TYPE=='easy'):
            words = splited_text = update.message.text.lower().split(' ')
            if (len(words)!=5):
                update.message.reply_text(u"давай пяток слов с иежду ними пробелы")
            else:
                print "Opening lyrics file. words: %s,id%i"%(words,chat_id)
                #lyr = open('lyrics_'+chat_id+'.txt','w+')
                c=[]
                for i in range(5):
                    c+=words[i]*5
                    #for j in range(5):
                        #lyr.write(' '+words[i])
                #lyr.close()
                save_tts(c)
                words= json.load(open('lyrics.json'))
                wavs = [w+".wav" for w in words]
                P,t = fft_pow(BEATFNAME,low_pass=True)
                tms = mark_beats(P,t)
                place_words(c,BEATFNAME,tms)
                print "Created Track."
                message = bot.send_audio(audio=open('result.wav'),
			     chat_id=chat_id)
                print "DONE"
        elif(TYPE=='mood'):
            update.message.reply_text(u"Сорри я пока не в настроении")
        else:
            update.message.reply_text(u"Сорри я пока не в настроении")
        WAITING=False

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def help_message(arguments, message):
    response = {'chat_id': message['chat']['id']}
    result = ["Hey, %s!" % message["from"].get("first_name"),
              "\rI can accept only these commands:"]
    for command in CMD:
        result.append(command)
    response['text'] = "\n\t".join(result)
    return response

def vanilia_gen(bot,update):
    update.message.reply_text("Отправляй свои словечки, я замиксую йоу!")
    WAITING=True
    TYPE='easy'

def main():
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_handler(CommandHandler("easypeasy", vanilia_gen))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
