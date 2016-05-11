import paho.mqtt.client as mqtt
import json

azure_data_format = {
   "lora_temp":"87.87",
   "lora_humi":"78.78"
}

def on_azure_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("client/200000019/200000019-GIOT-MAKER")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))
    json_extractor = json.loads(msg.payload)
#    print(json_extractor['recv'])
#    print(json_extractor['macAddr'])
#    print(json_extractor['data'].decode("hex"))
    string_value = json_extractor['data'].decode("hex")
#    print(string_value[1:6])
#    print(string_value[6:11])
    azure_data_format['lora_temp'] = string_value[1:6]
    azure_data_format['lora_humi'] = string_value[6:11]
    azure_client.publish("devices/gtk01/messages/events/",  json.dumps(azure_data_format))



azure_client = mqtt.Client(client_id="gtk01", protocol=mqtt.MQTTv311)
azure_client.on_connect = on_azure_connect
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("200000019", password="86873039")
client.connect("52.193.146.103", 80, 60)

azure_client.tls_set("/root/bc2025.pem")
azure_client.username_pw_set("nthuiot.azure-devices.net/gtk01", password="SharedAccessSignature sr=nthuiot.azure-devices.net%2fdevices%2fgtk01&sig=8reDPNVhhqWOFedCR36MbxM%2bgmgpXXpsFAbcq5Htzzs%3d&se=1461435380")
azure_client.connect("nthuiot.azure-devices.net", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
