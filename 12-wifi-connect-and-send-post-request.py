import network
import socket
import time
from machine import Pin
import machine
import urequests as requests

# GLOBAL_VARIABLES
ssid = "YOUR-WIFI-SSID"
password = "YOUR-WIFI-PASSWORD"

wlan = None

def init():
    wlan = network.WLAN(network.STA_IF)
    connect_to_wifi(wlan,ssid, password)
    
def loop():
    while True:
        url = "http://srv12.mikr.us:40154/data"

        payload = [
            {
                "variable": "a",
                "value": 222
            }
        ]
        headers = {
            "Content-Type": "application/json",
            "device-token": "REPLACE"
        }

        r = requests.request("POST", url, json=payload, headers=headers)

        print("Response: ")
        print(r.text)
        r.close() # important!!!
        print("WAIT...")
        time.sleep_ms(3000)
      
def connect_to_wifi(wlan = None, ssid = "", password = ""):
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep_ms(1000)
    print("WiFi "+ ssid + " connected!")
    
init()
loop()