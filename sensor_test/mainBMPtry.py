import RPi.GPIO as GPIO
import datetime
import csv
import ms5837
from time import sleep
from scd30_i2c import SCD30
import time
from PiPocketGeiger import RadiationWatch
from bmp180 import bmp180  # Import the BMP180 class
from setuptools import setup

# bar02 class
class Bar02:
    def __init__(self, i2cbus=1):
        self.sensor = ms5837.MS5837_30BA(i2cbus)
        self.sensor.init()

    def read(self):
        self.sensor.read()
        _data = [self.sensor.pressure(ms5837.UNITS_psi), self.sensor.temperature(ms5837.UNITS_Centigrade),
                 self.sensor.altitude()]
        return _data

# scd30 class
class Sensor:
    def __init__(self, pins):
        self.pins = pins
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

    def read(self):
        return [GPIO.input(x) for x in self.pins]

# Initialize the BMP180 sensor
bmp = bmp180(0x77)

# Ground station on campus talk to EE
ran_already = False

def read_all_sensors():
    global ran_already
    date_var, time_var, psi, temperature, altitude, CO2level, relativeHumidity, scdTemperature, bmp_temperature, bmp_pressure, bmp_altitude = 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'
    timeStart = datetime.datetime.now()
    date_and_time = str(timeStart)
    dt_split = date_and_time.split(' ')
    date_var = dt_split[0]
    time_var = dt_split[1]
    with open('/home/james/Desktop/sensor_test/SENSORDATA.csv', 'a+', newline='') as SENSORS:
        bar02_spam = csv.writer(SENSORS, delimiter=',')
        if not (ran_already):
            bar02_spam.writerow(['Date', 'Time', 'psi', 'temperature', 'altitude', 'CO2level', 'relativeHumidity', 'scdTemperature', 'bmp_temperature', 'bmp_pressure', 'bmp_altitude'])
            ran_already = True

        try:
            bar02 = Bar02()
            bar_data = bar02.read()
            psi = bar_data[0]
            temperature = bar_data[1]
            altitude = bar_data[2]
        except:
            psi, temperature, altitude = 'null', 'null', 'null'

        try:
            scd30 = SCD30()
            scd30_data = scd30.read_measurement()
            CO2level = scd30_data[0]
            scdTemperature = scd30_data[1]
            relativeHumidity = scd30_data[2]
        except:
            CO2level, scdTemperature, relativeHumidity = 'null', 'null', 'null'

        try:
            # Read data from BMP180 sensor
            bmp_temperature = bmp.get_temp()
            bmp_pressure = bmp.get_pressure()
            bmp_altitude = bmp.get_altitude()
        except:
            bmp_temperature, bmp_pressure, bmp_altitude = 'null', 'null', 'null'

        total_values = [date_var, time_var, psi, temperature, altitude, CO2level, relativeHumidity, scdTemperature, bmp_temperature, bmp_pressure, bmp_altitude]
        print('total_values: ', total_values)
        bar02_spam.writerow(total_values)

run_flag = True
while run_flag:
    read_all_sensors()
    time.sleep(1)
