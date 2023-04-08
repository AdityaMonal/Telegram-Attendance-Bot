import os.path

import telebot
import constants as key
from main import attendance
import datetime
bot = telebot.TeleBot(key.API_KEY)
attender = attendance()
@bot.message_handler(commands=["start"])
def startup(message):
    bot.send_message(message.chat.id, "Mark : /markAttendance\nGet : /getAttendance")
@bot.message_handler(commands=["hey"])
def greet(message):
    bot.reply_to(message, "Hey Nibbaa!")


@bot.message_handler(commands=["Hi"])
def welcome(message):
    bot.send_message(message.chat.id, "savithri says hi")

def vjitGreet(message):
    if message.text.split()[0].lower() == "vjit":
        return True
    else:
        return False
@bot.message_handler(func=vjitGreet)
def sendVjit(message):
    bot.send_message(message.chat.id, "Welcome to Vjit ")


class count:
    sec = ""
    start = 0
    end = 0
    i = 0
    req = True
    datereq = True
    date = ""
@bot.message_handler(commands=["markAttendance"])
def markAttendance(message):
    # class count:
    count.sec = ""
    # count.start = 0
    # count.end = 0
    # count.i = 0
    count.req = True
    count.datereq = True
    count.date = ""
    bot.send_message(message.chat.id, "Enter Date: \nPress /today for default")
    def dateParse(message):

        if len(message.text.split('/')) == 3 and count.datereq:
            count.datereq = False
            count.date = message.text
            return True
        else:
            return False

    @bot.message_handler(func=dateParse)
    def dateGet(message):
        print(count.date)
        bot.send_message(message.chat.id, "Enter class name:")
    @bot.message_handler(commands=["today"])
    def dateDefault(message):
        if count.datereq:
            count.datereq=False
            count.date = ""
            bot.send_message(message.chat.id, "Enter class name:")
        else:
            return

    def startText(message):
        # dec=message.text.split()
        if message.text.lower()[:-2] in ["it", "cse", "eee"] and int(message.text.lower()[-1]) <= 4 and count.req:
            count.sec = message.text.upper()
            print(count.sec)
            return True

        else:
            return False

    @bot.message_handler(func=startText)
    def startAttendance(message):
        print(count.date)
        attender.sec = count.sec
        count.start = count.i+1
        attender.initiate()
        bot.send_message(message.chat.id, "Upload class Photos:\n/exec")

    @bot.message_handler(content_types=['photo'])
    def classPhotos(message):
        print('message.photo =', message.photo)
        fileID = message.photo[-1].file_id
        print('fileID =', fileID)
        file_info = bot.get_file(fileID)
        print('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)
        count.i += 1
        if not os.path.exists("input_images"):
            os.mkdir("input_images")
        pat="input_images\image"+str(count.i)+".jpg"
        with open(pat, 'wb') as new_file:
            new_file.write(downloaded_file)

    @bot.message_handler(commands=["exec"])
    def triggerAttendance(message):
        if not count.req:
            return
        else:
            count.req = False
            count.end = count.i
            print(count.date)
            if len(count.date)==0:
                markedNames = attender.execute(count.start, count.end)
            else:
                markedNames = attender.execute(count.start, count.end, count.date)
            # count.date = ""
            marked = """"""

            for name in markedNames:
                marked += name+'\n'
            if len(marked) > 0:
                bot.send_message(message.chat.id, marked)
            else:
                bot.send_message(message.chat.id, "Barrrrrh")


@bot.message_handler(commands=["getAttendance"])
def getAttendance(message1):
    bot.send_message(message1.chat.id, "enter class name")
    class i:
        c = True
        sec = ''
    def section(message):
        i.sec = message.text.split()[0].upper()
        if i.sec in ["ITB4", "ITC4"] and i.c:
            i.c = False
            return True
        else:
            return False
    @bot.message_handler(func=section)
    def retrieveAttendance(message):
        marked=attender.getAttendance(i.sec)
        bot.send_message(message.chat.id, marked)

bot.polling()