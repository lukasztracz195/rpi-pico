import network
import socket
import time
from machine import Pin
import machine

# GLOBAL_VARIABLES
ssid = "TP-Link_0A51"
password = "11111111"
led = Pin(1, Pin.OUT)
wlan = None

def init():
    wlan = network.WLAN(network.STA_IF)
    connect_to_wifi(wlan,ssid, password)
    
def loop():
    while True: 
      led.value(1) 
      time.sleep_ms(500) 
      led.value(0) 
      time.sleep_ms(500)
      
def connect_to_wifi(wlan = None, ssid = "", password = ""):
    #Connect to WLAN
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())
    
init()
loop()




