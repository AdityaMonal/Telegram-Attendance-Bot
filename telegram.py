import os.path

import telebot
import constants as key
from main import attendance
import datetime
bot = telebot.TeleBot(key.API_KEY)
with open('resources\\user_ids.txt', 'r') as tfile:
    authIds = tfile.readline().split(',')
print(authIds)
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
    # start = 0
    # end = 0
    # i = 0
    req = False
    datereq = False
    date = ""
    response=False
class imNo:
    i=0
userImgs = {}
marker = {}
attender = {}
@bot.message_handler(commands=["markAttendance"])
def markAttendance(message):
    # class count:

    marker[message.from_user.id] = count()
    attender[message.from_user.id] = attendance()
    marker[message.from_user.id].sec = ""
    userImgs[message.from_user.id] = []
    # marker[message.from_user.id].start = 0
    # marker[message.from_user.id].end = 0
    # marker[message.from_user.id].i = 0
    print(message.from_user.id, authIds)
    if str(message.from_user.id) not in authIds:
        bot.send_message(message.chat.id, "Verify that you are faculty first:\n/authenticate")
        return
    marker[message.from_user.id].req = True
    marker[message.from_user.id].datereq = True
    marker[message.from_user.id].date = ""
    bot.send_message(message.chat.id, "Enter Date: \nPress /today for default")
    print(marker)
    print(userImgs)
    return
class get:
    req=False
@bot.message_handler(commands=["authenticate"])
def authentication(message):
    c=get()
    c.req=True
    bot.send_message(message.chat.id,"Enter vjit provided password:")
    def password(message):
        if c.req :
            c.req = False
            return True
        else:
            return False

    @bot.message_handler(func=password)
    def authenticator(message):
        if message.text==key.password:
            with open('resources\\user_ids.txt', 'a') as tfile:
                if len(authIds) == 1:
                    tfile.write(str(message.from_user.id))
                    authIds[0]=str(message.from_user.id)
                else:
                    tfile.write("," + str(message.from_user.id))
                    authIds.append(str(message.from_user.id))
            bot.send_message(message.chat.id, "Great you are authenticated \U0001F44D")
            return
        else:
            bot.send_message(message.chat.id, "You entered wrong password \U0001F44E")
            return





def dateParse(message):

    if len(message.text.split('/')) == 3 and marker[message.from_user.id].datereq:
        marker[message.from_user.id].datereq = False
        marker[message.from_user.id].date = message.text
        return True
    else:
        return False

@bot.message_handler(func=dateParse)
def dateGet(message):
    print(marker[message.from_user.id].date)
    bot.send_message(message.chat.id, "Enter class name:")
@bot.message_handler(commands=["today"])
def dateDefault(message):
    if marker[message.from_user.id].datereq:
        marker[message.from_user.id].datereq=False
        marker[message.from_user.id].date = ""
        bot.send_message(message.chat.id, "Enter class name:")
    else:
        return

def startText(message):
    # dec=message.text.split()
    if message.text.lower()[:-2] in ["it", "cse", "eee"] and int(message.text.lower()[-1]) <= 4 and marker[message.from_user.id].req:
        marker[message.from_user.id].sec = message.text.upper()
        print(marker[message.from_user.id].sec)
        return True

    else:
        return False

@bot.message_handler(func=startText)
def startAttendance(message):
    print(marker[message.from_user.id].date)
    attender[message.from_user.id].sec = marker[message.from_user.id].sec
    marker[message.from_user.id].start = imNo.i+1
    attender[message.from_user.id].initiate()
    bot.send_message(message.chat.id, "Upload class Photos:\n/exec")
    return

@bot.message_handler(content_types=['photo'])
def classPhotos(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    imNo.i += 1
    userImgs[message.from_user.id].append(imNo.i)
    print(marker)
    print(userImgs)
    if not os.path.exists("input_images"):
        os.mkdir("input_images")
    pat="input_images\image"+str(imNo.i)+".jpg"
    with open(pat, 'wb') as new_file:
        new_file.write(downloaded_file)

@bot.message_handler(commands=["exec"])
def triggerAttendance(message):
    if not marker[message.from_user.id].req:
        return
    else:
        marker[message.from_user.id].req = False
        marker[message.from_user.id].end = imNo.i
        print(marker[message.from_user.id].date)
        if len(marker[message.from_user.id].date)==0:
            markedNames = attender[message.from_user.id].execute(userImgs[message.from_user.id])
        else:
            markedNames = attender[message.from_user.id].execute(userImgs[message.from_user.id], marker[message.from_user.id].date)
        # marker[message.from_user.id].date = ""
        marked = """"""

        for name in markedNames:
            marked += name+'\n'
        if len(marked) > 0:
            bot.send_message(message.chat.id, marked)
            marker[message.from_user.id].response=True
            bot.send_message(message.chat.id, "To get dected faces: /detected ")
        else:
            bot.send_message(message.chat.id, "Barrrrrh")

@bot.message_handler(commands=["detected"])
def returnMarked(message):
    if marker[message.from_user.id].response :
        marker[message.from_user.id].response=False
        outPath = key.path + "\output_images"
        for cl in userImgs[message.from_user.id]:
            imgName = f'{outPath}\image{cl}.jpg'
            pic = open(imgName, 'rb')
            bot.send_photo(message.chat.id, pic)



@bot.message_handler(commands=["getAttendance"])
def getAttendance(message1):
    marker[message1.from_user.id] = count()
    attender[message1.from_user.id] = attendance()
    userImgs[message1.from_user.id] = []
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
        marked=attender[message1.from_user.id].getAttendance(i.sec)
        bot.send_message(message.chat.id, marked)

bot.polling()