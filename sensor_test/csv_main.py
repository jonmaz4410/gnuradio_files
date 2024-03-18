import RPi.GPIO as GPIO
import ms5837
from time import sleep
from scd30_i2c import SCD30
#csv addition
import os
import csv 
import datetime

#### GPIO/PIN SETUP ####

GPIO.setmode(GPIO.BCM) # SIMPLY FROM EXAMPLE ONLINE, MAKE SURE THIS IS CORRECT LATER (ESPECIALLY IF USING ANALOG INPUT)

class Sensor:
    def __init__(self, pins):
        self.pins = pins
        for pin in self.pins:
            GPIO.setup(pin,GPIO.OUT)
    def read(self):
        return [GPIO.input(x) for x in self.pins]

class Bar02:
    def __init__(self,i2cbus=1):
        self.sensor = ms5837.MS5837_30BA(i2cbus)
        self.sensor.init()
    def read(self):
        self.sensor.read()
        return [self.sensor.pressure(ms5837.UNITS_psi), self.sensor.temperature(ms5837.UNITS_Centigrade), self.sensor.altitude()]

#scd30 = Sensor([3,5]) #Grove hookup with i2c at 3(SDA) and 5(SCL)
bar02 = Bar02()
scd30 = SCD30()
scd30.set_measurement_interval(2) #play with time for accuracy
scd30.start_periodic_measurement()

sleep(2)

#### LOOP, WILL RUN FOREVER #####

# attempt at time control of sensors

runtime = 20        #code 2

start_time = datetime.datetime.now()        #code 2

#csv additions open and wite into csv file
with open('datadtf.csv','w',newline='') as csvfile:
    spam = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spam.writerow(['Timestamp', 'Sensor', 'Value1', 'Value2', 'Value3'])

    while (datetime.datetime.now() - start_time).total_seconds() < runtime:

#while True:        code 1 
    #print(bar02.read())    code 1
    #print(scd30.read_measurement())

        if scd30.get_data_ready():
            try:
                scd30_data = scd30.read_measurement()
                bar02_data = bar02.read()
            # code 1    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-_%H-%M-%S")
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            #with open('datadtf.csv','w',newline='') as csvfile:    code 1
#code 1         #spam = csv.writer(csvfile, delimiter= ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                spam.writerow([timestamp,'SCD30'] + list(scd30_data))
                spam.writerow([timestamp,'Bar02'] + list(bar02_data))
                csvfile.flush()
            except Exception as e : 
                print(f"An error occured: {e}") 
        sleep(1)


  
