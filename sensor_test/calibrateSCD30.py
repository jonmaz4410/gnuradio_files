import RPi.GPIO as GPIO
import ms5837
import csv 
import datetime
from time import sleep
from scd30_i2c import SCD30

#### GPIO/PIN SETUP ####

GPIO.setmode(GPIO.BCM)

class Sensor:
    def __init__(self, pins):
        self.pins = pins
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
    def read(self):
        return [GPIO.input(x) for x in self.pins]

class Bar02:
    def __init__(self, i2cbus=1):
        self.sensor = ms5837.MS5837_30BA(i2cbus)
        self.sensor.init()
    def read(self):
        self.sensor.read()
        return [self.sensor.pressure(ms5837.UNITS_psi), self.sensor.temperature(ms5837.UNITS_Centigrade), self.sensor.altitude()]

# Initialize sensors
bar02 = Bar02()

# Initialize SCD30 sensor
scd30 = SCD30()
scd30.set_measurement_interval(2)
scd30.self_calibration_enabled = True  # Enable self-calibration
scd30.start_periodic_measurement()

# Set runtime and start time
runtime = 20
start_time = datetime.datetime.now()

# Open CSV file for writing
with open('datadtf.csv', 'w', newline='') as csvfile:
    spam = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spam.writerow(['Timestamp', 'Sensor', 'Reading'])

    while (datetime.datetime.now() - start_time).total_seconds() < runtime:
        if scd30.get_data_ready():
            try:
                scd30_data = scd30.read_measurement()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Write each SCD30 reading to a new line in the CSV file
                spam.writerow([timestamp, 'SCD30', f"CO2: {scd30_data[0]} ppm"])
                spam.writerow([timestamp, 'SCD30', f"Humidity: {scd30_data[1]} %"])
                spam.writerow([timestamp, 'SCD30', f"Temperature: {scd30_data[2]} C"])
                csvfile.flush()

                # Print SCD30 readings to the screen
                print(f"Timestamp: {timestamp}")
                print(f"SCD30 - CO2: {scd30_data[0]} ppm, Humidity: {scd30_data[1]} %, Temperature: {scd30_data[2]} C")
                
            except Exception as e:
                print(f"An error occurred: {e}")

        if bar02:
            try:
                bar02_data = bar02.read()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Write each Bar02 reading to a new line in the CSV file
                spam.writerow([timestamp, 'Bar02', f"Pressure: {bar02_data[0]} psi"])
                spam.writerow([timestamp, 'Bar02', f"Temperature: {bar02_data[1]} C"])
                spam.writerow([timestamp, 'Bar02', f"Altitude: {bar02_data[2]} m"])
                csvfile.flush()

                # Print Bar02 readings to the screen
                print(f"Timestamp: {timestamp}")
                print(f"Bar02 - Pressure: {bar02_data[0]} psi, Temperature: {bar02_data[1]} C, Altitude: {bar02_data[2]} m")
                
            except Exception as e:
                print(f"An error occurred: {e}")

        sleep(1)
