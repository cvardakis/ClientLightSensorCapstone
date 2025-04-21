"""
File: sensor_reader.py
Author: connorvardakis
Date: 2/17/25
Updated: 2/17/25
Description: sensor_reader.py takes data measurements from the SQM via serial USB interaction
"""
import json
import serial
import time
import re
import pytz
import datetime

import config


def read_sensor():
    """
    Collects data and formats it for json usage

    :return:
    Dictionary of sensor data
    """
    try:
        # Open the serial connection
        print(f"Using Serial Port: {config.SERIAL_PORT}")
        with serial.Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=1) as ser:
            ser.write(b"rx")  # Send command rx - reading request - ref. 79 of user manual
            time.sleep(0.5)

            response = ser.readline().decode('utf-8').strip()
            parts = response.split(',')

            data = {
                "reading": parts[1],
                "frequency": parts[2],
                "counts": parts[3],
                "temp": parts[5]
            }

            clean_data = {key: clean_value(value) for key, value in data.items()}  # Remove extra 0s and units
            utc_now = datetime.datetime.now(pytz.utc)
            local_now = utc_now.astimezone(pytz.timezone(config.LOCAL_TIMEZONE))

            utc_str = utc_now.strftime("%Y-%m-%dT%H:%M:%S")  # Format UTC timezone
            local_str = local_now.strftime("%Y-%m-%dT%H:%M:%S")  # Format Local timezone

            # Return data in format order for json server POST request
            payload = {
                "utc": utc_str,
                "local": local_str,
                "temp": data["temp"],
                "counts": data["counts"],
                "frequency": data["frequency"],
                "reading": data["reading"]
            }

            clean_payload = {
                "utc": utc_str,
                "local": local_str,
                "temp": clean_value(data["temp"]),
                "counts": clean_value(data["counts"]),
                "frequency": clean_value(data["frequency"]),
                "reading": clean_value(data["reading"])
            }

            print(f"[INFO] Data collected: {json.dumps(payload)}")
            print(f"[INFO] Clean Data: {json.dumps(clean_payload)}")
            return clean_payload
    except serial.SerialException as e:
        print(f"[ERROR] Serial USB connection error:", e)


def clean_value(value):
    """
    Clean up values from sensor. Removes all units and leading zeros.
    Returns 0 if blank

    :param value:
    Singular string of data

    :return:
    Cleaned string of data
    """
    pattern = r'\b0*([1-9]\d*(?:\.\d+)?|0(?:\.\d+)?)(?=\D|$)'

    match = re.findall(pattern, value)

    measurement = match[0]

    if measurement == "0":
        measurement = "0.0"

    return measurement
