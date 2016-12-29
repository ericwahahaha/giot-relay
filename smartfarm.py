import requests
import socket
import threading
import logging
import time
import mraa

import json
import urllib2

# change this to the values from MCS web console

smart_farm_channel = {
   "datapoints":[
      {
      	"dataChnId":"farm_temp",
         "values":{
            "value":"28.10"
         }
      },
      {
         "dataChnId":"farm_humi",
         "values":{
            "value":"27.02"
         }
      }
   ]
}


DEVICE_INFO = {
    'device_id' : 'Dis819KB',
    'device_key' : 'ICdmPAER0h0dvy9r'
}

# change 'INFO' to 'WARNING' to filter info messages
logging.basicConfig(level='INFO')

heartBeatTask = None

def establishCommandChannel():
    # Query command server's IP & port
    connectionAPI = 'https://api.mediatek.com/mcs/v2/devices/%(device_id)s/connections.csv'
    r = requests.get(connectionAPI % DEVICE_INFO,
                 headers = {'deviceKey' : DEVICE_INFO['device_key'],
                            'Content-Type' : 'text/csv'})
    logging.info("Command Channel IP,port=" + r.text)
    (ip, port) = r.text.split(',')

    # Connect to command server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.settimeout(None)

    # Heartbeat for command server to keep the channel alive
    def sendHeartBeat(commandChannel):
        keepAliveMessage = '%(device_id)s,%(device_key)s,0' % DEVICE_INFO
        commandChannel.sendall(keepAliveMessage)
        logging.info("beat:%s" % keepAliveMessage)
        # check the value - it's either 0 or 1
        getTH()

    def heartBeat(commandChannel):
        sendHeartBeat(commandChannel)
        # Re-start the timer periodically
        global heartBeatTask
        heartBeatTask = threading.Timer(40, heartBeat, [commandChannel]).start()

    heartBeat(s)
    return s

def waitAndExecuteCommand(commandChannel):
    while True:
        command = commandChannel.recv(1024)
        logging.info("recv:" + command)
        # command can be a response of heart beat or an update of the LED_control,
        # so we split by ',' and drop device id and device key and check length
        fields = command.split(',')[2:]

        if len(fields) > 1:
            timeStamp, dataChannelId, commandString = fields
            if dataChannelId == 'farm_led':
                # check the value - it's either 0 or 1
                commandValue = int(commandString)
                logging.info("led :%d" % commandValue)
                setLED(commandValue)
            elif dataChannelId == 'farm_fan':
                # check the value - it's either 0 or 1
                commandValue = int(commandString)
                logging.info("led :%d" % commandValue)
                setFAN(commandValue)

pin = None
def setupLED():
    global led_pin
    # on LinkIt Smart 7699, pin 44 is the Wi-Fi LED.
    led_pin = mraa.Gpio(0)
    led_pin.dir(mraa.DIR_OUT)

def setupFAN():
    global fan_pin
    # on LinkIt Smart 7699, pin 44 is the Wi-Fi LED.
    fan_pin = mraa.Gpio(1)
    fan_pin.dir(mraa.DIR_OUT)

def setLED(state):
    # Note the LED is "reversed" to the pin's GPIO status.
    # So we reverse it here.
    if state:
        led_pin.write(0)
    else:
        led_pin.write(1)

def setFAN(state):
    # Note the LED is "reversed" to the pin's GPIO status.
    # So we reverse it here.
    if state:
        fan_pin.write(0)
    else:
        fan_pin.write(1)

def setupSHT20():
    global i2c
    i2c = mraa.I2c(0)
    i2c.address(0x40)

def getTH():
    Tcmd = 0xF3
    RHcmd = 0xF5

    i2c.writeByte(Tcmd)
    time.sleep(0.1)
    d = i2c.read(3)
    bdata = bytearray(d)
    St = bdata[0]*256+bdata[1]
    T = (175.72*St/2**16)-46.85
    print(T)

    time.sleep(1)
    i2c.writeByte(RHcmd)
    time.sleep(0.1)
    d = i2c.read(3)
    bdata = bytearray()
    bdata.extend(d)

    Srh = bdata[0]*256+bdata[1]
    RH = (125*Srh/2**16)-6

    print(RH)
    smart_farm_channel['datapoints'][0]['values']['value'] = T
    smart_farm_channel['datapoints'][1]['values']['value'] = RH
    req = urllib2.Request('http://api.mediatek.com/mcs/v2/devices/Dis819KB/datapoints')
    req.add_header('deviceKey', 'ICdmPAER0h0dvy9r')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(smart_farm_channel))
    print(response)


if __name__ == '__main__':
    setupLED()
    setupFAN()
    setupSHT20()
    channel = establishCommandChannel()
    waitAndExecuteCommand(channel)
