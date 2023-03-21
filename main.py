import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
import joblib


# from PIL import ImageGrab

class attendance:
    # path = r"C:\Users\Harishith\Downloads\MAJOR PROJECTOG\MAJOR PROJECT\Training_images"
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

    def markAttendance(self, name):
        # print("bruh")
        with open(self.sec+'\\attendance.csv', 'a+') as f:
            if os.stat(self.sec+'\\attendance.csv').st_size == 0:
                f.write("Name,Date")
            f.seek(0)
            myDataList = f.readlines()
            nameList = []
            # print(myDataList)
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])

            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%a,(%b/%d/%y)')

                f.writelines(f'\n{name},{dtString}')

    def train(self):
        path = r"C:\Users\Harishith\Downloads\MAJOR PROJECTOG\MAJOR PROJECT\Training_images\\" + self.sec
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

    def execute(self, start=1, end=1):
        inpPath = r"C:\Users\Harishith\Downloads\MAJOR PROJECTOG\MAJOR PROJECT\input_images"
        myInps = os.listdir(inpPath)
        # print(myInps)
        for cl in myInps:
            # print(os.path.splitext(cl)[0])
            fileno = int(os.path.splitext(cl)[0][5:])
            # print(fileno)
            if fileno < start or fileno > end:
                continue

            img = cv2.imread(f'{inpPath}\{cl}')
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)
                print(matchIndex, self.classNames, len(self.encodeListKnown))
                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper()

                    # print(name)

                    # y1, x2, y2, x1 = faceLoc
                    # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    # cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    self.markAttendance(name)
                    # while True:
                    #     imgK = cv2.resize(imgS, (960, 540))
                    #     cv2.imshow('lol', imgK)
                    #     if cv2.waitKey(1) & 0xff == ord('q'):
                    #         break
