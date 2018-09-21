import machine
import pycom
import sys
import time
import network

pycom.heartbeat(True)

print("Initializing...")

wlan = network.WLAN(mode=network.WLAN.STA)

# Place WiFi credentials here.
wlan.connect('ThingForwardWiFi', auth=(network.WLAN.WPA2, 'iotthingforward'))

while not wlan.isconnected():
    time.sleep_ms(50)

print(wlan.ifconfig())
