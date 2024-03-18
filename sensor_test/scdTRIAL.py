import RPi.GPIO as GPIO
import datetime
import csv
import ms5837
from time import sleep
from scd30_i2c import SCD30
import time
from PiPocketGeiger import RadiationWatch

#GPIO.setmode(GPIO.BCM)

class Sensor:
    def __init__(self, pins):
        self.pins = pins
        for pin in self.pins:
            GPIO.setup(pin,GPIO.OUT)
        def read(self):
            return [GPIO.input(x) for x in self.pins]

scd30 = Sensor([3,5]) #Grove hookup with i2c at 3(SDA) and 5(SCL)
scd30 = SCD30()
scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()


try: 
    scd30 = SCD30()
    scd30_data = scd30.read_measurement()
    print('bar_data: ', scd30_data)
    C02level = scd30_data[0]
    scdTemperature = scd30_data[1]
    relativeHumidity = scd30_data[2]
except:
    C02level, scdTemperature, relativeHumidity = 'null', 'null', 'null' #read -1 instead of null

#ground station on campus talk to EE

        #psi, temperature, altitude = bar02_function()
        # can add alert after except from fail kindfa like the null read

total_values = [date_var, time_var, psi, temperature, altitude, C02level, relativeHumidity, scdTemperature]
     #our_team(total_values)       
print('total_values: ',total_values)
bar02_spam.writerow(total_values)


run_flag = True
while run_flag:

    
    read_all_sensors()


    time.sleep(30)

