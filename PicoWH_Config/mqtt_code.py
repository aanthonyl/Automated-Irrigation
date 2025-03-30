import time
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT
import wifi
import ssl
import socketpool
from secrets import secrets

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
        print("TRUE!")
    elif message == "OFF":
        print("FALSE!")
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

io.add_feed_callback("solenoid_control", on_toggle_msg)

# Connect to Adafruit IO
io.connect()
io.subscribe("solenoid_control")

prv_refresh_time = 0.0
while True:
    # Poll for incoming messages
    try:
        # get data from feed

    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        connect_wifi()
        io.reconnect()
        continue
    # Send a new temperature reading to IO every 30 seconds
    if (time.monotonic() - prv_refresh_time) > 30:
        # take the cpu's temperature
        cpu_temp = cpu.temperature
        # truncate to two decimal points
        cpu_temp = str(cpu_temp)[:5]
        print("CPU temperature is %s degrees C" % cpu_temp)
        # publish it to io
        print("Publishing %s to temperature feed..." % cpu_temp)
        io.publish("temperature", cpu_temp)
        print("Published!")
        prv_refresh_time = time.monotonic() # type: ignore