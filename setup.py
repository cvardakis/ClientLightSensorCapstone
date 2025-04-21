"""
File: setup.py
Author: connorvardakis
Date: 3/14/25
Updated: 4/20/25
Description: Define all setup processes to verify the sensor is working and authentication can
             be reached with server
"""

import platform
import requests
import serial
import serial.tools.list_ports
import time
import config


def get_os():
    """
    Gets the operating system - UNUSED
    """
    operating_system = platform.system()
    config.set_os(operating_system)
    print("[STARTUP] Operating System: ", operating_system)


def find_sensor():
    """
    Locates the sensor and test to ensure it works
    """
    # Find all ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Search for a port with FT description - defined in user manual
        if "FT" in port.description or "FT" in port.hwid:
            sensor_port = port.device
            print(f"[STARTUP] Potential USB port: {sensor_port}")

            try:
                # After finding port attempts a reading
                with serial.Serial(sensor_port, config.BAUD_RATE, timeout=1) as ser:
                    ser.write(b"rx")
                    time.sleep(0.5)

                    response = ser.readline().decode('utf-8').strip()

                    if response:
                        print("[STARTUP] Sensor mount found")
                        config.set_serial(sensor_port)
                        return

            except Exception as e:
                print(f"[STARTUP] Failed to get response from detected port: {e}")

    print("[ERROR] No USB ports found")
    exit(1)


def authenticate_sensor():
    """
    Authenticates sensor on server

    :return:
    Manipulates authenticated state and updates ID based on serve assigned ID
    """

    payload = {
        "registration_key": config.REGISTRATION_KEY,
        "id": config.SENSOR_ID,
        "name": config.NAME,
        "location": config.LOCATION,
        "latitude": config.LAT,
        "longitude": config.LONG,
        "elevation": config.ELEVATION
    }

    print(f"[INFO] Authenticating sensor...")
    response = requests.post(config.AUTH_ENDPOINT, json=payload)

    if response.status_code in [200, 201]:
        data = response.json()
        print(f"[INFO] Sensor Authenticated: {data}")
        config.set_id(data["sensor_id"])
        config.set_auth(True)
    else:
        print(f"[ERROR] Failed to authenticate sensor: {response.text}")


def get_coords():
    """
    Find Long and Lat coordinates -- UNUSED
    """
    # set manually?
    ip_response = requests.get("https://api.ipify.org?format=json")
    ip = ip_response.json()['ip']

    geo_response = requests.get(f'https://ipinfo.io/{ip}/json')
    geo_data = geo_response.json()
    lat, lon = map(float, geo_data['loc'].split(','))

    elevation_response = requests.get(f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}')
    elevation_data = elevation_response.json()
    elevation = elevation_data['results'][0]['elevation']

    print(f"[INFO] Location Coordinates: {lat}, {lon}, {elevation}")


def startup():
    print("[INFO] Starting setup...")
    find_sensor()
    authenticate_sensor()
