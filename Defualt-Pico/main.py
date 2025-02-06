# Author: Anthony Liao
# Pi Pico #1, no battery voltage reading

import board
import busio
import digitalio
import time
import alarm
from analogio import AnalogIn
#import adafruit_bh1750 # light sensor
#from adafruit_onewire.bus import OneWireBus # used by temperature sensor
#import adafruit_ds18x20 # temperature sensor

#i2c = busio.I2C(scl=board.GP15, sda=board.GP14)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


m_one = AnalogIn(board.GP27) #1.2 moisture sensor
m_two = AnalogIn(board.GP26) #2.0

#light_sens = adafruit_bh1750.BH1750(i2c)

# Temperature sensor inits
#ow_bus = OneWireBus(board.D25)
#devices = ow_bus.scan()
#ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])



try:
    with open("/data.csv", "a") as temp_log:
        # This is where you will write your code that runs when not connected

        # Write the data to the data.csv file ever cycle
        #v1 = m_one.value
        #v2 = m_two.value

        #write volt lux, temp, two sensors
        #temp_log.write('{0:.2f}, {1:.1f}, {2:.1f}, {3:.1f}, {4:.1f}\n'.format(bat_volt, light_sens.lux, ds18b20.temperature, v1, v2))
        #write lux and two sensors
        #temp_log.write('{0:.2f}, {1:.1f},{2:1f}\n'.format(light_sens.lux, v1, v2))


        # Writing two sensors, you can do up to 4- since there are 4 analog pins on the pico
        temp_log.write('{0:.1f}, {1:.1f}\n'.format(m_one.value, m_two.value))
        temp_log.flush()

        # Go to sleep for set time, then wake up 
        time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 600) #deeper sleep for 10 mins

        alarm.exit_and_deep_sleep_until_alarms(time_alarm)

except OSError as e:  # When the filesystem is NOT writable by CircuitPython...
    delay = 0.5  # ...blink\ the LED every half second.
    if e.args[0] == 28:  # If the file system is full...
        delay = 0.15  # ...blink the LED every 0.15 seconds!
    while True:
        # This is where you will write code that prints to the serial monitor, since when connected to your computer
        # the filesystem will not be writeable.


        led.value = not led.value
        # voltage and three moist sensors
        #print(('A0: {0:.2f} A1: {1} A2: {2} A3: {3}'.format(get_voltage(vbat_voltage), m_one.value, m_two.value, m_three.value)))
        # volt,lux, temp, two moist
        #print('A0: {0:.2f} A1: {1} A2:{2} A3:{3:.1f} A4:{4:.1f}'.format(get_voltage(vbat_voltage), light_sens.lux, ds18b20.temperature,m_one.value, m_two.value))
        time.sleep(delay)

        #print('Lux: {0:.2f} moist: {1:.1f} moist2: {2:1f}\n'.format(light_sens.lux, m_one.value, m_two.value))
        print('moist: {0:.1f} moist2: {1:1f}\n'.format(m_one.value, m_two.value))
        #print('moist: {0:.1f}\n'.format(m_one.value))
		
		