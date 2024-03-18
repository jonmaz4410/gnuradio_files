import RPi.GPIO as GPIO
import datetime
import csv
import ms5837
from time import sleep
from scd30_i2c import SCD30
import time
from PiPocketGeiger import RadiationWatch

def bar02_function():

    # Get readings
    return psi, temperature, altitude

def scd_function():
    # Get readings

    return scdTemperature, C02level, relativeHumidity

with open('bar02.csv','w', newline='') as bar02csv, open('scd30.csv','w', newline='') as scd30csv, open('geiger.csv','w', newline='') as geigercsv:
    bar02_spam = csv.writer(bar02csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    bar02_spam.writerow(['Timestamp', 'Sensor', '(psi)', '(C)', '(m)'])

    scd30_spam = csv.writer(scd30csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    scd30_spam.writerow(['Timestamp', 'Sensor', '(ppm)', '(C)', '(%)'])

    geiger_writer = csv.writer(geigercsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    geiger_writer.writerow(['Timestamp'])

    #### GPIO/PIN SETUP ####

    GPIO.setmode(GPIO.BCM)

    radCount = 0

    def onRadiation():
        global radCount
        radCount += 1
        timestamp = datetime.datetime.now().strftime("  %m-%d-%Y  %H:%M:%S:%f")
        geiger_writer.writerow([timestamp])
    def onNoise():
        #onRadiation()
        print("Vibration! Stop moving!")
    with RadiationWatch(24, 23) as radiationWatch:
        radiationWatch.register_radiation_callback(onRadiation)
        radiationWatch.register_noise_callback(onNoise)   
    def getuSv():
        return (radCount/(((datetime.datetime.now() - timeStart).total_seconds())/60)) * 0.0057
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

    scd30 = Sensor([3,5]) #Grove hookup with i2c at 3(SDA) and 5(SCL)
    bar02 = Bar02()
    scd30 = SCD30()
    scd30.set_measurement_interval(2)
    scd30.start_periodic_measurement()

    sleep(2)

    while True:
        print(bar02.read())
        if scd30.get_data_ready():
            _data = scd30.read_measurement()
            print(_data)
            scd30_spam.writerow(_data)
        sleep(1)