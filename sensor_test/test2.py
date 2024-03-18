import csv
from time import sleep

while True:
    with open('/home/james/Desktop/test.csv', 'a+') as SENSORS:
        bar02_spam = csv.writer(SENSORS, delimiter=',')
        bar02_spam.writerow(['test','test'])