"""
File: data_logger.py
Author: connorvardakis
Date: 2/17/25
Updated: 2/17/25
Description: data_logger.py saves, loads, and clears unsent data
"""
import json
import os

LOG_FILE_DIRECTORY = "logs/"
LOG_FILE = "logs/unsent_date.json"


# noinspection PyBroadException
def save_unsent_data(data):
    """
    Saves unsent data to JSON file

    :param data:
    Data formated for sending to the server
    """
    if not os.path.exists(LOG_FILE_DIRECTORY):
        os.makedirs(LOG_FILE_DIRECTORY)

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                unsent_data = json.load(f)
        else:
            unsent_data = []

        unsent_data.append(data)
        with open(LOG_FILE, "w") as f:
            json.dump(unsent_data, f, indent=4)

            print("[INFO] Data logged for later use")

    except Exception:
        print("[ERROR] Failed to log data")


def load_unsent_data():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)

    return []


def clear_unsent_data():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print("[INFO] Cleared unsent data")
