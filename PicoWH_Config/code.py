import wifi
import ssl
import socketpool
import adafruit_requests
from secrets import secrets

# Connecting to WiFi
print("Connecting to Wi-Fi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])

print("Connected!")
print("IP Address:", wifi.radio.ipv4_address)
print("MAC Address:", ":".join([f"{i:02X}" for i in wifi.radio.mac_address]))

# Connecting to Adafruit IO
AIO_USERNAME = secrets["ADAFRUIT_AIO_USERNAME"]
AIO_KEY = secrets["ADAFRUIT_AIO_KEY"]
FEED_NAME = "moisture-sensor"

# Adafruit IO URL Construction
AIO_URL = f"https://io.adafruit.com/api/v2/{AIO_USERNAME}/feeds/{FEED_NAME}/data"

# Socket and Requests Session
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()
requests = adafruit_requests.Session(pool, ssl_context=ssl_context)

# Test sending data to Adafruit IO
data = {"value": 59}
headers = {"X-AIO-Key": AIO_KEY}

print("Sending data to Adafruit IO...")
response = requests.post(AIO_URL, json=data, headers=headers)

# Outputting Response Code
print("Response Code:", response.status_code)