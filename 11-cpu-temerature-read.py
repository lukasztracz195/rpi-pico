import time
from time import ticks_ms, ticks_us, sleep 
from machine import Pin, ADC


# GLOBAL_VARIABLES
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

while True:
    adc_voltage = read_adc_vcc(ADC)
    temp_celcius = adc_vcc2ceclius_temp(adc_voltage)
    temp_fahrenheit=celcius2farenheit(temp_celcius)
    print("Temperature: {}°C {}°F".format(temp_celcius,temp_fahrenheit))
    time.sleep_ms(500)