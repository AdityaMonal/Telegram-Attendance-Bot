import telebot
import constants as key
from main import attendance
import datetime
bot=telebot.TeleBot(key.API_KEY)
attender=attendance()
@bot.message_handler(commands=["start"])
def startup(message):
    bot.send_message(message.chat.id, "Take attendance \nEnter as : <Dept><sec><year> attendance \neg:ITB4 attendance")
@bot.message_handler(commands=["hey"])
def greet(message):
    bot.reply_to(message,"Hey Nibbaa!")


@bot.message_handler(commands=["Hi"])
def welcome(message):
    bot.send_message(message.chat.id,"savithri says hi")


def vjitGreet(message):
    if message.text.split()[0].lower()=="vjit":
        return True
    else:
        return False
@bot.message_handler(func=vjitGreet)
def sendVjit(message):
    bot.send_message(message.chat.id, "Welcome to Vjit ")





class count:
    sec=""
    start=0
    end=0
    i=0
def startText(message):
    dec=message.text.split()
    if dec[-1].lower()=="attendance":
        if dec[0].lower()[:-2] in ["it", "cse", "eee"] and int(dec[0].lower()[-1]) <= 4:
            count.sec=dec[0].upper()
            print(count.sec)
            return True

    else:
        # bot.send_message(message.chat.id, "Invalid class \nEnter as : <Dept><sec><year> eg:ITB4")
        return False
@bot.message_handler(func=startText)
def startAttendance(message):
    attender.sec=count.sec
    count.start = count.i+1
    attender.initiate()
    bot.send_message(message.chat.id, "Upload class Photos")



@bot.message_handler(content_types=['photo'])
def classPhotos(message):
    print ('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    count.i+=1
    pat="input_images\image"+str(count.i)+".jpg"
    with open(pat, 'wb') as new_file:
        new_file.write(downloaded_file)

def triggerText(message):
    if message.text.split()[0].lower() == "execute":
        return True
    else:
        return False

@bot.message_handler(func=triggerText)
def triggerAttendance(message):
    count.end = count.i
    markedNames=attender.execute(count.start,count.end)
    marked = """"""

    for name in markedNames:
        marked+=name+"""\n"""

    bot.send_message(message.chat.id, marked)
bot.polling()