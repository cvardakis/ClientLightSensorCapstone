"""
File: data_sender.py
Author: connorvardakis
Date: 2/17/25
Updated: 2/17/25
Description: data_sender.py authenticates sensor on server. Sends data off to server
"""
import requests
import config
from config import set_auth
from setup import authenticate_sensor
from data_logger import save_unsent_data, load_unsent_data, clear_unsent_data


def send_sensor_data(data):
    """
    Sends data off to server

    :param data:
    Data formated for sending to server

    :return:
    Successful or not Successful for sending data to server
    """
    if not config.AUTHENTICATED:
        authenticate_sensor()

    while True:
        payload = {"id": config.SENSOR_ID, **data}  # Include Sensor ID in json of data

        response = requests.post(config.DATA_ENDPOINT, json=payload)

        if response.status_code == 201:
            print(f"[INFO] Data Sent Successfully: {payload}")
            return True

        else:
            print(f"[ERROR] Failed to send data: {response.text} - {payload}")
            if "recognized" in response.text:
                set_auth(False)
            return False


def retry_unsent_data():
    """
    Collects unsent data from local logs and attempts to send data to server
    """
    unsent_data = load_unsent_data()
    if not unsent_data:
        return

    print("[INFO] Attempting to send unsent data to server...]")
    for data in unsent_data[:]:
        if send_sensor_data(data):
            unsent_data.remove(data)

    if not unsent_data:
        clear_unsent_data()
    else:
        for data in unsent_data[:]:
            save_unsent_data(data)
