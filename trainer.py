
import sys
from main import attendance

getClass = sys.argv[1].upper()
print(getClass)
attender = attendance()
attender.sec = getClass
attender.train()
