#!/usr/bin/python
# Read temperature from TI TMP102, and report it to MQTT broker
# AMV 2020/09, modified from
# http://www.pibits.net/code/tmp102-sensor-and-raspberry-pi-python-example.php

import time
import smbus
import paho.mqtt.client as mqtt

# I2C Config
i2c_ch = 1
i2c_address = 0x48

# TMP102 Register addresses
reg_temp = 0x00
reg_config = 0x01

# MQTT Config
mqtt_broker = "keke"
mqtt_port = 1883
mqtt_topic = "baba/temp_sensor"

# Calculate the 2's complement of a number
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

# Read temperature registers and calculate Celsius
def read_temp():

    # Read temperature registers
    val = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
    temp_c = (val[0] << 4) | (val[1] >> 5)

    # Convert to 2s complement (temperatures can be negative)
    temp_c = twos_comp(temp_c, 12)

    # Convert registers value to temperature (C)
    temp_c = temp_c * 0.0625

    return temp_c

def to_fahrenheit(temp_c):
    return ( temp_c * 1.8 + 32 )

# Initialize I2C (SMBus)
bus = smbus.SMBus(i2c_ch)

# Read the CONFIG register (2 bytes)
val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("Old CONFIG:", val)

# Set to 4 Hz sampling (CR1, CR0 = 0b10)
val[1] = val[1] & 0b00111111
val[1] = val[1] | (0b10 << 6)

# Write 4 Hz sampling back to CONFIG
bus.write_i2c_block_data(i2c_address, reg_config, val)

# Read CONFIG to verify that we changed it
val = bus.read_i2c_block_data(i2c_address, reg_config, 2)
print("New CONFIG:", val)

# Print out temperature every second
while True:
    temperature = read_temp()
    print(round(temperature, 2), "C")
    print(round(to_fahrenheit(temperature), 2), "F")
    time.sleep(1)

