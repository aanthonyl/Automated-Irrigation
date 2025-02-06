import board
import digitalio
import time
from analogio import AnalogIn
import adafruit_bh1750
#from adafruit_onewire.bus import OneWireBus
#import adafruit_ds18x20

import alarm

#i2c = board.I2C()
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


vbat_voltage = AnalogIn(board.A0)
m_one = AnalogIn(board.A2)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

try:
    with open("/data.csv", "a") as temp_log:
        while True:
            bat_volt = get_voltage(vbat_voltage)

            # Write the data to the data.csv file every 10 mins.
            v1 = m_one.value
            #temp_log.write('{0:.2f}, {1:.1f}, {2:.1f}, {3:.1f}, {4:.1f}\n'.format((bat_volt, light_sens.lux, ds18b20.temperature, v1, v2)))
            temp_log.write('{0:.2f}, {1:.1f}'.format(bat_volt,v1))
            temp_log.flush()

            # deep sleep
            time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 600) #deeper sleep for 10 mins
            alarm.exit_and_deep_sleep_until_alarms(time_alarm)


except OSError as e:  # When the filesystem is NOT writable by CircuitPython...
    delay = 0.5  # ...blink\ the LED every half second.
    if e.args[0] == 28:  # If the file system is full...
        delay = 0.15  # ...blink the LED every 0.15 seconds!
    while True:
        led.value = not led.value
        print(('A0: {0:.2f} A1: {1}'.format(get_voltage(vbat_voltage), m_one.value)))
        time.sleep(delay)