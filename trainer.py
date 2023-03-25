
import sys
from main import attendance
from datetime import datetime

# getClass = sys.argv[1].upper()
# print(getClass)
attender = attendance()
attender.sec = "ITB4"
attender.train()
# attender.markAttendance("VAMSHI", datetime.strptime("24/03/23", '%d/%m/%y'))
