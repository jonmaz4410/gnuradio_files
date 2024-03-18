import RPi.GPIO as GPIO
import datetime
import csv
import ms5837
from time import sleep
from scd30_i2c import SCD30
from PiPocketGeiger import RadiationWatch

class Bar02:
    def __init__(self, i2cbus=1):
        self.sensor = ms5837.MS5837_30BA(i2cbus)
        self.sensor.init()
    
    def read(self):
        self.sensor.read()
        return [
            self.sensor.pressure(ms5837.UNITS_psi),
            self.sensor.temperature(ms5837.UNITS_Centigrade),
            self.sensor.altitude()
        ]

def read_all_sensors():
    try:
        bar02 = Bar02()
        bar_data = bar02.read()
        print('bar_data:', bar_data)
    except Exception as e:
        print('Error reading Bar02 sensor:', e)
        bar_data = ['null', 'null', 'null']

    try:
        scd30 = SCD30()
        scd30_data = scd30.read_measurement()
        print('scd30_data:', scd30_data)
    except Exception as e:
        print('Error reading SCD30 sensor:', e)
        scd30_data = ['null', 'null', 'null']

    # Write data to CSV, handle timestamps, etc.

GPIO.setmode(GPIO.BCM)

try:
    run_flag = True
    while run_flag:
        read_all_sensors()
        sleep(30)
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup()
