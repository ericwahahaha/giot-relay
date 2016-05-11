import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("devices/gtk01/messages/devicebound/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    client.publish("devices/gtk01/messages/events/", "87785555555")

client = mqtt.Client(client_id="gtk01", protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

client.tls_set("/root/bc2025.pem")
client.username_pw_set("nthuiot.azure-devices.net/gtk01", password="SharedAccessSignature sr=nthuiot.azure-devices.net%2fdevices%2fgtk01&sig=8reDPNVhhqWOFedCR36MbxM%2bgmgpXXpsFAbcq5Htzzs%3d&se=1461435380")
client.connect("nthuiot.azure-devices.net", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
