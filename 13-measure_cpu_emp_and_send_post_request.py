import network
import socket
import time
from time import ticks_ms, ticks_us, sleep 
from machine import Pin, ADC
import urequests as requests

# GLOBAL_VARIABLES
SSID = "YOUR-WIFI-SSID"
PASSWORD = "YOUR-WIFI-PASSWORD"
WLAN = None
ADC = machine.ADC(4)

def read_adc_vcc(adc):
    vcc = 3.3
    u16_max_int_value = 65535
    return adc.read_u16() * (vcc/ (u16_max_int_value))

def adc_vcc2ceclius_temp(adc_voltage):
    normal_temperature_diode_in_celcius_degree = 27
    diode_vcc_for_27_celcius_degree = 0.706
    diode_vcc_per_one_celcius_degree = 0.001721
    current_adc_vcc = (adc_voltage - diode_vcc_for_27_celcius_degree)
    return normal_temperature_diode_in_celcius_degree - current_adc_vcc/diode_vcc_per_one_celcius_degree

def celcius2farenheit(temp_in_celcius):
    return 32+(1.8*temp_in_celcius)
    
def create_payload(variable, value):
    return [
            {
                "variable": variable,
                "value": value
            }
        ]


def send_payload(payload,  sleep_ms=3000):
    url = "http://srv12.mikr.us:40154/data"
    headers = {
            "Content-Type": "application/json",
            "device-token": "DEVICE_TOKEN"
            }
    r = requests.request("POST", url, json=payload, headers=headers)

    print("Response: ")
    print(r.text)
    r.close() # important!!!
    print("WAIT...")
    time.sleep_ms(sleep_ms)

    
def init():
    WLAN = network.WLAN(network.STA_IF)
    connect_to_wifi(WLAN,SSID, PASSWORD)

    
def loop():
    while True:
        adc_voltage = read_adc_vcc(ADC)
        temp_celcius = adc_vcc2ceclius_temp(adc_voltage)
        payload = create_payload(variable="TEMP_C", value=temp_celcius)
        send_payload(payload)
    
    
def connect_to_wifi(wlan = None, ssid = "", password = ""):
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep_ms(1000)
    print("WiFi "+ ssid + " connected!")
    
init()
loop()