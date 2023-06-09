import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
import joblib
import constants


# from PIL import ImageGrab

class attendance:
    path = constants.path
    images = []
    name = []
    classNames = []
    sec=""
    myList = []

    encodeListKnown = []

    def findEncodings(self, images):
        encodeList = []

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(self, name, now=datetime.now()):
        # print("bruh")
        with open(self.sec+'\\attendance.csv', 'a+') as f:
            if os.stat(self.sec+'\\attendance.csv').st_size == 0:
                f.write("Name,Date\n")
            f.seek(0)
            myDataList = f.readlines()
            nameList = []
            # now = datetime(2023,3,22)
            dtString = now.strftime('(%d/%m/%y)')
            namedate = f'{name},{dtString}\n'
            # print(myDataList)
            for line in myDataList:
                # entry = line.split(',')
                nameList.append(line)

            if namedate not in nameList:
                # now = datetime.now()
                # dtString = now.strftime('(%d/%m/%y)')

                f.writelines(namedate)
            # f.writelines(f'\n')

    def train(self):
        path = self.path+"\Training_images\\" + self.sec
        myList = os.listdir(path)
        classNames = []
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            self.images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)
        # print("self",self.images)
        if not os.path.exists(self.sec):
            os.mkdir(self.sec)
        with open(self.sec+'\\' + self.sec + '.txt', 'w') as tfile:
            tfile.write(','.join(classNames))
        fil = self.sec + '\\' + self.sec + '.pkl'
        joblib.dump(self.findEncodings(self.images), fil)
        print('Encoding Complete')

    def initiate(self):
        fil = self.sec + '\\' + self.sec + '.pkl'
        self.encodeListKnown = joblib.load(fil)
        with open(self.sec+'\\' + self.sec + '.txt', 'r') as tfile:
            self.classNames=tfile.readline().split(',')


        print(self.classNames)
        print(self.encodeListKnown)

    def execute(self, imgs, dat=""):
        inpPath = self.path+"\input_images"
        myInps = os.listdir(inpPath)
        # print(myInps)
        marked = []
        for cl in imgs:
            # print(os.path.splitext(cl)[0])
            # fileno = int(os.path.splitext(cl)[0][5:])
            # # print(fileno)
            # if fileno < start or fileno > end:
            #     continue
            print(cl)
            imgName=f'{inpPath}\image{cl}.jpg'
            print(imgName)
            img = cv2.imread(imgName)
            # imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace, 0.5)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)
                print(matchIndex, self.classNames, len(self.encodeListKnown))
                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper()

                    # print(name)

                    y1, x2, y2, x1 = faceLoc
                    # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 44
                    part = int((y2 - y1) / 6)
                    cv2.rectangle(img, (x1, y1), (x2, y2 + part), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2), (x2, y2 + part), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + int(part / 5), y2 + part - int(part / 5)), cv2.FONT_HERSHEY_DUPLEX,
                                (1 / 35) * part, (255, 255, 255), int(part / 15))
                    if name not in marked:
                        marked.append(name)
                    if len(dat) > 0:
                        self.markAttendance(name, datetime.strptime(dat, '%d/%m/%y'))
                    else:
                        self.markAttendance(name)
            # while True:
            #     imgK = cv2.resize(img, (960, 540))
            #     cv2.imshow('lol', imgK)
            #     if cv2.waitKey(1) & 0xff == ord('q'):
            #         break
            if not os.path.exists("output_images"):
                os.mkdir("output_images")
            pat = "output_images\image" + str(cl) + ".jpg"
            cv2.imwrite(pat, img)
        return marked
    def getAttendance(self,sec):
        reg = {}
        marked=""""""
        with open(sec + '\\attendance.csv', 'r+') as f:
            dataList = f.readlines()
            c=1
            for line in dataList:
                if c==1:
                    c+=1
                    continue
                date=line.split(',')[-1][1:-2]
                if date not in reg:
                    reg[date]=[line.split(',')[0]]
                else:
                    reg[date].append(line.split(',')[0])
        for key in reg:
            marked += key+'\n'+"-----------------\n"+'\n'.join(reg[key])+'\n'+"-----------------\n"+"total: "+str(len(reg[key]))+'\n\n'
        return marked


