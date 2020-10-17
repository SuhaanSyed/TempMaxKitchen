import time
from datetime import datetime
import sys


now = datetime.now()

i = 0
while ((datetime.now() - now).seconds < 10):
    pass
print("10 secs elapsed")

 
#while now + datetime.datetime.now() < now + 30:
#print(now)   
"""
def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time elapsed = {0}:{1}:{2}".format(int(hours),int(mins), sec))
    
input("Press Enter to Start")
start_time = time.time()

input("Press Enter to Stop")
end_time = time.time()

time_lapsed = end_time - start_time
time_convert(time_lapsed)
"""