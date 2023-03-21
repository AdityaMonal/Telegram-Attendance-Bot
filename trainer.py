import os

from main import attendance


classes = os.listdir(r"C:\Users\Harishith\Downloads\MAJOR PROJECTOG\MAJOR PROJECT\Training_images")
for cl in classes:
    attender = attendance()
    attender.sec = cl
    attender.train()
# attender.initiate('ITB4')
# attender.execute()