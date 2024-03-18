import datetime
from time import sleep

radCount=0
timeStart=datetime.datetime.now()

sleep(27)

def getuSv():
    global radCount
    global startTime
    return (radCount/(((datetime.datetime.now() - timeStart).total_seconds())/1)) * 0.0057
radCount = 1151
print(getuSv())