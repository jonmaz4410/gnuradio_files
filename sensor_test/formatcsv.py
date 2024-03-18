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
scd30 = SCD30()
scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()

# Set runtime and start time
runtime = 20
start_time = datetime.datetime.now()

# Open CSV file for writing
#with open('datadtf.csv', 'w', newline='') as csvfile:
with open('bar02_data.csv', 'w', newline='') as bar02_file, open('scd30_data.csv', 'w', newline='') as scd30_file:

    #spam = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #spam.writerow(['Timestamp', 'Sensor', '(psi)', '(C)', '(m)'])
    bar02_spam = csv.writer(bar02_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    bar02_spam.writerow(['Timestamp', 'Sensor', '(psi)', '(C)', '(m)'])

    scd30_spam = csv.writer(scd30_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    scd30_spam.writerow(['Timestamp', 'Sensor', '(ppm)', '(C)', '(%)'])


    while (datetime.datetime.now() - start_time).total_seconds() < runtime:
        if scd30.get_data_ready():
            try:
                scd30_data = scd30.read_measurement()
                #bar02_data = bar02.read()
                timestamp = datetime.datetime.now().strftime("  %m-%d-%Y  %H:%M:%S:%f")
                
                # Write to CSV file
                #scd30_formatted = f"SCD30 - CO2: {scd30_data[0]} ppm, Humidity: {scd30_data[1]} %, Temperature: {scd30_data[2]} C"
                #bar02_formatted = f"Bar02 - Pressure: {bar02_data[0]} psi, Temperature: {bar02_data[1]} C, Altitude: {bar02_data[2]} m"
                #spam.writerow([timestamp, 'SCD30', scd30_formatted])       code 2
                #spam.writerow([timestamp, 'Bar02', bar02_formatted])       code 2
                #spam.writerow([timestamp, 'SCD30'] + list(scd30_data))     code 1
                #spam.writerow([timestamp, 'Bar02'] + list(bar02_data))     code 1
                scd30_spam.writerow(['SCD30', timestamp])

                scd30_spam.writerow([f"   CO2: {scd30_data[0]} ppm"])
                scd30_spam.writerow([f"   Humidity: {scd30_data[2]} %"])
                scd30_spam.writerow([f"   Temperature: {scd30_data[1]} C"])
                scd30_spam.writerow(' ')

                scd30_file.flush()

                # Print scd30 to screen
                print(f"Timestamp: {timestamp}")
                print(f"SCD30 - CO2: {scd30_data[0]} ppm, Humidity: {scd30_data[2]} %, Temperature: {scd30_data[1]} C")
                
               
                #print(f"Timestamp: {timestamp}") code 2
                #print(f"Timestamp: {scd30_formatted}") code 2
                #print(f"Timestamp: {bar02_formatted}") code 2

                #print(f"SCD30-  CO2: {scd30_data[0]:.2f}ppm, temp: {scd30_data[1]:.2f}'C, rh: {scd30_data[2]:.2f}%")
                #print(f"SCD30: {scd30_data}")
                #print(f"Pressure: {bar02_data[0]:.2f}psi, temp: {bar02_data[1]:.2f}'C, altitude: {bar02_data[2]:.2f}m%")
                #print(f"Bar02: {bar02_data}")
                print()
                
            except Exception as e:
                print(f"An error occurred: {e}")

        sleep(0.4)

        if bar02:
            try:
                bar02_data = bar02.read()
                timestamp = datetime.datetime.now().strftime("  %m-%d-%Y  %H:%M:%S")
                
                # Write each Bar02 reading to a new line in the CSV file
                bar02_spam.writerow(['Bar02', timestamp])
                
                bar02_spam.writerow([f"   Pressure: {bar02_data[0]} psi"])
                bar02_spam.writerow([f"   Temperature: {bar02_data[1]} C"])
                bar02_spam.writerow([f"   Altitude: {bar02_data[2]} m"])
                bar02_spam.writerow(' ')
                bar02_file.flush()
                

                #print bar02 to screen
                print(f"Timestamp: {timestamp}")
                print(f"Bar02 - Pressure: {bar02_data[0]} psi, Temperature: {bar02_data[1]} C, Altitude: {bar02_data[2]} m")
                

            except Exception as e:
                print(f"An error occurred: {e}")

        sleep(1)

