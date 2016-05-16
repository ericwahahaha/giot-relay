import paho.mqtt.client as mqtt
import json
import urllib2

mcs_data_format = {
   "datapoints":[
      {
         "dataChnId":"lora_temp",
         "values":{
            "value":"28.00"
         }
      },
      {
         "dataChnId":"lora_humi",
         "values":{
            "value":"27.00"
         }
      }
   ]
}


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
    mcs_data_format['datapoints'][0]['values']['value'] = string_value[1:6]
    mcs_data_format['datapoints'][1]['values']['value'] = string_value[6:11]
#    print(mcs_data_format)
    req = urllib2.Request('http://api.mediatek.com/mcs/v2/devices/DUgyOyLY/datapoints')
    req.add_header('deviceKey', 'XOhNhdy4vxfLxr2B')
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(mcs_data_format))
#    print(response)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("200000019", password="86873039")
client.connect("52.193.146.103", 80, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
