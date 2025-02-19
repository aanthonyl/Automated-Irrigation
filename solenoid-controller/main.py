import board
import digitalio
import time
from analogio import AnalogIn
#from adafruit_onewire.bus import OneWireBus
#import adafruit_ds18x20

import alarm

#i2c = board.I2C()
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


p1 = digitalio.DigitalInOut(board.D10)
p2 = digitalio.DigitalInOut(board.D9)

p1.direction = digitalio.Direction.OUTPUT
p2.direction = digitalio.Direction.OUTPUT

toggle = digitalio.DigitalInOut(board.D12)
toggle.direction = digitalio.Direction.OUTPUT

once = True


vbat_voltage = AnalogIn(board.A0)
m_one = AnalogIn(board.A2)


input_pin = digitalio.DigitalInOut(board.D6)  # Replace 'D5' with your desired pin
input_pin.direction = digitalio.Direction.INPUT  # Set the pin as an input

def turn_off():
    p1.value = True 
    p2.value = False
    time.sleep(0.01)
    p1.value = False 
    p2.value = False

def turn_on():
    p1.value = False 
    p2.value = True
    time.sleep(0.01)
    p1.value = False 
    p2.value = False

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

current_State = 0
value = -1
toggle.value = True
try:
    if value == -1:
        with open("/vars.txt","r") as file:
            value = file.read().strip()
            print(value)
            if value == '1':
                turn_on()
                current_State = 0
            else:
                turn_off()
                current_State = 1
        with open("/vars.txt","w") as file:
            file.write(str(current_State))

        time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 5) #deeper sleep for 5 seconds
        alarm.exit_and_deep_sleep_until_alarms(time_alarm)


    '''
    with open("/data.csv", "a") as temp_log:
        while True:
            bat_volt = get_voltage(vbat_voltage)

            # Write the data to the data.csv file every 10 mins.
            v1 = m_one.value
            #temp_log.write('{0:.2f}, {1:.1f}, {2:.1f}, {3:.1f}, {4:.1f}\n'.format((bat_volt, light_sens.lux, ds18b20.temperature, v1, v2)))
            #temp_log.write('{0:.2f}, {1:.1f}'.format(bat_volt,v1))
            temp_log.flush()

            # deep sleep
            time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 600) #deeper sleep for 10 mins
            alarm.exit_and_deep_sleep_until_alarms(time_alarm)
    '''

except OSError as e:  # When the filesystem is NOT writable by CircuitPython...
    delay = 0.5  # ...blink\ the LED every half second.
    if e.args[0] == 28:  # If the file system is full...
        delay = 0.15  # ...blink the LED every 0.15 seconds!
    while True:
        if once:
            #turn_on()
            print("set value!")
            once = False
            time.sleep(0.01)
        p1.value = False 
        p2.value = False
        led.value = not led.value
        print(('A0: {0:.2f}'.format(get_voltage(vbat_voltage))))
        # Read the value from the input pin
        time.sleep(delay)

'''
delay = 0.5
while True:
    print(('A0: {0:.2f}'.format(get_voltage(vbat_voltage))))
    time.sleep(delay)
    '''