import paho.mqtt.client as mqtt
import json
import urllib2

mcs_data_format = {
   "datapoints":[
      {
         "dataChnId":"lora_temp",
         "values":{
            "value":"00.00"
         }
      },
      {
         "dataChnId":"lora_humi",
         "values":{
            "value":"00.00"
         }
      }
   ]
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("GIOT-GW/UL/1C497B498D80")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    json_extractor = json.loads(msg.payload)
    # print(json_extractor[0]['channel'])
    # print(json_extractor[0]['macAddr'])
    # print(json_extractor[0]['data'].decode("hex"))

    if json_extractor[0]['macAddr'] == "000000000500005f":

        string_value = json_extractor[0]['data'].decode("hex")
        # print(string_value[1:6])
        # print(string_value[6:11])
        mcs_data_format['datapoints'][0]['values']['value'] = string_value[1:6]
        mcs_data_format['datapoints'][1]['values']['value'] = string_value[6:11]
        # print(mcs_data_format)
        req = urllib2.Request('http://api.mediatek.com/mcs/v2/devices/D2vxFwNV/datapoints')
        req.add_header('deviceKey', 'd98BVa78SaYEj8MG')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(mcs_data_format))
        # print(response)

client = mqtt.Client(client_id="1C497B498D81", protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("lazyengineers", password="lazyengineers")
client.connect("104.155.21.63", port=1883, keepalive=60)

downlink_data = [{
    "macAddr": "000000000500005f",
    "data": "0090",
    "id": "998877abcd0123",
    "extra": {
        "port": 2,
        "txpara": 6
    }
}]


client.publish("GIOT-GW/DL/1C497B498D80", payload=json.dumps(downlink_data), qos=0, retain=False)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
