import RPi.GPIO as GPIO
import datetime
import csv
import ms5837
from time import sleep
from scd30_i2c import SCD30
import time
from PiPocketGeiger import RadiationWatch

bar02csv = open('bar02.csv','a+', newline='')
scd30csv = open('scd30.csv','a+', newline='')
geigercsv = open('geiger.csv','a+', newline='')

bar02_spam = csv.writer(bar02csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
bar02_spam.writerow(['Timestamp', 'Sensor', '(psi)', '(C)', '(m)'])

scd30_spam = csv.writer(scd30csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
scd30_spam.writerow(['Timestamp', 'Sensor', '(ppm)', '(C)', '(%)'])

geiger_writer = csv.writer(geigercsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
geiger_writer.writerow(['Timestamp'])

#### GPIO/PIN SETUP ####

GPIO.setmode(GPIO.BCM) # SIMPLY FROM EXAMPLE ONLINE, MAKE SURE THIS IS CORRECT LATER (ESPECIALLY IF USING ANALOG INPUT)
#define gpio pins

#Set GPIO mode
#GPIO.setmode(GPIO.BCM)

# Define GPIO pins
#GPIO_PIN_23 = 23
#GPIO_PIN_24 = 24

# Setup GPIO pins as inputs
#GPIO.setup(GPIO_PIN_23, GPIO.IN)
#GPIO.setup(GPIO_PIN_24, GPIO.IN)

def onRadiation():
    timestamp = datetime.datetime.now().strftime("  %m-%d-%Y  %H:%M:%S:%f")
    geiger_writer.writerow([timestamp])
def onNoise():
    print("Vibration! Stop moving!")
with RadiationWatch(24, 23) as radiationWatch:
   radiationWatch.register_radiation_callback(onRadiation)
   radiationWatch.register_noise_callback(onNoise)

#try:
    

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
        _data = [self.sensor.pressure(ms5837.UNITS_psi), self.sensor.temperature(ms5837.UNITS_Centigrade), self.sensor.altitude()]
        bar02_spam.writerow(_data)
        return _data

#scd30 = Sensor([3,5]) #Grove hookup with i2c at 3(SDA) and 5(SCL)
bar02 = Bar02()
scd30 = SCD30()
scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()

sleep(2)

while True:
    # Open CSV file for appending
    with open('bar02.csv', 'a+', newline='') as bar02csv:
        bar02_spam = csv.writer(bar02csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        bar02_data = bar02.read()
        print(bar02_data)
        # Write data to CSV file
        bar02_spam.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + bar02_data)
    
    # Open CSV file for appending
    with open('scd30.csv', 'a+', newline='') as scd30csv:
        scd30_spam = csv.writer(scd30csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        if scd30.get_data_ready():
            scd30_data = scd30.read_measurement()
            print(scd30_data)
            # Write data to CSV file
            scd30_spam.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + scd30_data)
    
    sleep(1)

