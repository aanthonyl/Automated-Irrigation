import time
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT
import wifi
import ssl
import socketpool
from secrets import secrets
import board
from analogio import AnalogIn
import digitalio


#define solenoid and moisture sensor and voltage divider
# LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Analog Sensors
m_one = AnalogIn(board.A2)
vbat_voltage = AnalogIn(board.A0)

# digital solenoid out
p1 = digitalio.DigitalInOut(board.GP13)
p2 = digitalio.DigitalInOut(board.GP14)
power_on = digitalio.DigitalInOut(board.GP16)

p1.direction = digitalio.Direction.OUTPUT
p2.direction = digitalio.Direction.OUTPUT
power_on.direction = digitalio.Direction.OUTPUT

def turn_off():
    power_on.value = True
    time.sleep(0.1)
    p1.value = True 
    p2.value = False
    time.sleep(.01)
    p1.value = False 
    p2.value = False
    time.sleep(.01)
    power_on.value = False

def turn_on():
    power_on.value = True
    time.sleep(0.01)
    p1.value = False 
    p2.value = True
    time.sleep(0.01)
    p1.value = False 
    p2.value = False
    time.sleep(.01)
    power_on.value = False

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    print("Connected to Adafruit IO! ")


def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def publish(client, userdata, topic, pid):
    # This method is called when the client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))
    if userdata is not None:
        print("Published User data: ", end="")
        print(userdata)

def disconnected(client):
    print("Disconnected from Adafruit IO!")


def on_toggle_msg(client, topic, message):
    # Method called whenever user/feeds/led has a new value
    print("New message on topic {0}: {1} ".format(topic, message))
    if message == "ON":
        turn_on()
    elif message == "OFF":
        turn_off()
    else:
        print("Unexpected message on the feed.")

# Connecting to WiFi
def connect_wifi():
    connected = False
    while not connected:
        try:
            print("Connecting to Wi-Fi...")
            wifi.radio.connect(secrets["ssid"], secrets["password"])
            connected = True
        except:
            print("Error Connecting")
        
        time.sleep(5)

def connect_io(_io):
    connected = False
    while not connected:
        try:            
            print("Connecting to Adafruit IO....")     
            _io.connect()
            _io.subscribe("solenoid-control")
            connected = True
        except:
            print("Error connecting to IO")

def blink_led():
    led.value = True
    time.sleep(1)
    led.value = False

def get_feed_value():
    try:
        print("Fetching latest feed value...")
        response = io.receive("solenoid_control")
        current_value = response["value"]
        print(f"Latest Value: {current_value}")
        return current_value
    except Exception as e:
        print(f"Error fetching feed: {e}")
        return None

connect_wifi()
blink_led()
print("Connected!")
print("IP Address:", wifi.radio.ipv4_address)
print("MAC Address:", ":".join([f"{i:02X}" for i in wifi.radio.mac_address]))


print("Initializing mqtt connection to adafruit...")
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=1883,
    username=secrets["ADAFRUIT_AIO_USERNAME"],
    password=secrets["ADAFRUIT_AIO_KEY"],
    socket_pool=pool,
    ssl_context=ssl_context,
)

io = IO_MQTT(mqtt_client)

print("Initialized!")

io.on_connect = connected
io.on_disconnect = disconnected
io.on_subscribe = subscribe
io.on_publish = publish

io.add_feed_callback("solenoid-control", on_toggle_msg)

# Connect to Adafruit IO
connect_io(io)
blink_led()

prv_refresh_time = 0.0
while True:
    # Poll for incoming messages
    try:
        mqtt_client.loop()
        # get data from feed

        if (time.monotonic() - prv_refresh_time) > 900:
            #io.publish("battery1", 4.1)
            #io.publish("moisture1", m_one.value)
            print("wanna print")
            prv_refresh_time = time.monotonic()


    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        connect_wifi()
        io.reconnect()
        continue # type: ignore