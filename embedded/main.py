import machine
import pycom
import sys
import time
import network
import urequests
import ujson

# see https://github.com/inmcm/micropyGPS/blob/master/micropyGPS.py
from micropyGPS import MicropyGPS
from bme280 import BME280

GPS_TIMEOUT_SECS=10

# https://docs.pycom.io/chapter/datasheets/boards/pytrack.html
# BLACK/GND=P1, RED/HOT=P4, SDA=P10, SCL=P11
i2c_bme = machine.I2C(1, pins=('P10', 'P11'))
bme = BME280(i2c=i2c_bme)
print(bme)

# init I2C to P21/P22
i2c = machine.I2C(0, mode=machine.I2C.MASTER, pins=('P22', 'P21'))

while True:
    # write to address of GPS
    GPS_I2CADDR = const(0x10)
    raw = bytearray(1)
    i2c.writeto(GPS_I2CADDR, raw)

    # create MicropyGPS instance
    gps = MicropyGPS()

    # start a timer
    chrono = machine.Timer.Chrono()
    chrono.start()

    # store results here.
    last_data = {}

    def check_for_valid_coordinates(gps):
        '''
        Given a MicropyGPS object, this function checks if valid coordinate
        data has been parsed successfully. If so, prints it out.
        '''

        if gps.satellite_data_updated() and gps.valid:
            last_data['date'] = gps.date_string("long")
            last_data['latitude'] = gps.latitude_string()
            last_data['longitude'] = gps.longitude_string()

    while True:
        # read some data from module via I2C
        raw = i2c.readfrom(GPS_I2CADDR, 16)
        # feed into gps object
        for b in raw:
            sentence = gps.update(chr(b))
            if sentence is not None:
                # gps successfully parsed a message from module
                # see if we have valid coordinates
                res = check_for_valid_coordinates(gps)

        elapsed = chrono.read()
        if elapsed > GPS_TIMEOUT_SECS:
            break

    #print("Finished.")

    # construct tx object
    resp = {}

    #if 'date' in last_data:
    #    #print("@ ", last_data['date'])
    #    resp["date"] = last_data['date']
    #if 'time' in last_data:
    #    #print("@ ", last_data['time'])
    #    resp["time"] = last_data['time']
    if 'latitude' in last_data and 'longitude' in last_data:
        #print("> ", last_data['latitude'], " ", last_data['longitude'])
        resp["lat"] = last_data['latitude']
        resp["long"] = last_data['longitude']

    #i2c.deinit()


    #
    #print(bme.temperature)
    #print(bme.humidity)
    resp["temp"] = bme.temperature
    resp["hum"] = bme.humidity

    try:
        json = ujson.dumps(resp) + "\r\n"
        print(json)
        urequests.request("POST", "http://192.168.0.100:3000/tx/TRK-4711", data=json)
    except OSError:
        print("Error posting data...")

    time.sleep(60)
