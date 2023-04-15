import network
import socket
import time
from machine import Pin
import machine
try:
    import urequests as requests
except ImportError:
    print("ERROR! urequest not found!!! - more: https://pypi.org/project/micropython-urequests/")
    import requests

# GLOBAL_VARIABLES
ssid = "YOUR-WIFI-SSID"
password = "YOUR-WIFI-PASSWORD"

wlan = None

def init():
    wlan = network.WLAN(network.STA_IF)
    connect_to_wifi(wlan,ssid, password)
    
def loop():
    while True:
        r = requests.get("https://ptsv3.com/t/tcore-test/post/")
        print("Response: ")
        print(r)
        print(r.content)
        print(r.text)
        print(r.json)
        # It's mandatory to close response objects as soon as you finished
        # working with them. On MicroPython platforms without full-fledged
        # OS, not doing so may lead to resource leaks and malfunction.
        r.close() # important!!!
        print("WAIT...")
        time.sleep_ms(3000)
      
def connect_to_wifi(wlan = None, ssid = "", password = ""):
    #Connect to WLAN
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep_ms(1000)
    print(wlan.ifconfig())
    print("WiFi "+ ssid + " connected!")
    
init()
loop()