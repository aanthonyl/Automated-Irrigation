import wifi
import ssl
import socketpool
import adafruit_requests
import board
import digitalio
import time
from analogio import AnalogIn
from secrets import secrets

# LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Analog Sensors
m_one = AnalogIn(board.A2)
vbat_voltage = AnalogIn(board.A0)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

# Connecting to WiFi
connected = False
while not connected:
    try:
        print("Connecting to Wi-Fi...")
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        connected = True
    except:
        print("Error Connecting")
    
    time.sleep(5)

print("Connected!")
print("IP Address:", wifi.radio.ipv4_address)
print("MAC Address:", ":".join([f"{i:02X}" for i in wifi.radio.mac_address]))

# Connecting to Adafruit IO
AIO_USERNAME = secrets["ADAFRUIT_AIO_USERNAME"]
AIO_KEY = secrets["ADAFRUIT_AIO_KEY"]
FEED_NAME = "moisture"
FEED_NAME2 = "battery"

# Adafruit IO URL Construction
AIO_URL = f"https://io.adafruit.com/api/v2/{AIO_USERNAME}/feeds/{FEED_NAME}/data"
AIO_URL2 = f"https://io.adafruit.com/api/v2/{AIO_USERNAME}/feeds/{FEED_NAME2}/data"

# Socket and Requests Session
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()
requests = adafruit_requests.Session(pool, ssl_context=ssl_context)

while True:
    try:
        with open("/data.csv", "a") as temp_log:
            while True:
                # Collecting Data
                bat_volt = get_voltage(vbat_voltage)
                v1 = m_one.value

                # Logging Data to CSV file
                with open("/data.csv", "a") as log_file:
                    log_file.write('{0:.2f}, {1:.1f}\n'.format(bat_volt,v1))
                    log_file.flush()

                # Defining Data to Send
                data_moisture = {"value": (v1)}
                data_battery = {"value": (bat_volt)}
                headers = {"X-AIO-Key": AIO_KEY}

                # Sending Data to Adafruit
                print("Sending data to Adafruit IO...")
                response = requests.post(AIO_URL, json=data_moisture, headers=headers)
                response2 = requests.post(AIO_URL2, json=data_battery, headers=headers)
                # Outputting Response Code
                print("Response Code 1:", response.status_code)
                print("Response Code 2:", response2.status_code)

                time.sleep(600)

    # When the filesystem is NOT writable by CircuitPython...
    except OSError as e:
        print(f"Filesystem Error: {e}")
        # Blink the LED every 0.15 seconds if the File System is full
        if e.args[0] == 28:
            delay = 0.15
        while True:
            print(m_one.value)
            led.value = True
            time.sleep(1)
            led.value = False

    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(20)