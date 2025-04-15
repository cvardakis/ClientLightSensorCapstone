"""
File: main.py
Author: connorvardakis
Date: 2/17/25
Updated: 3/2/25
Description: main.py controls the client side for getting data from SQM sensor and sending
             data to online server. If server is not online the data should save locally
             until connection is made with the server
"""
import sys
import time
import os
import datetime
import threading
import traceback

from config import load_config
from sensor_reader import read_sensor
from data_sender import send_sensor_data, retry_unsent_data
from data_logger import save_unsent_data
from setup import startup


def wait_until_5_minute(now=None):
    """
    Calculate the time until the next 5-minute mark (with second fixed to 30)
    and return that datetime. If no datetime is provided, uses the current time.
    """
    if now is None:
        now = datetime.datetime.now()
    current_minute = now.minute
    next_minute = (current_minute // 5 + 1) * 5

    if next_minute < 60:
        next_trigger = now.replace(minute=next_minute, second=0, microsecond=0)
    else:
        minutes_to_add = 60 - current_minute
        next_trigger = (now + datetime.timedelta(minutes=minutes_to_add)).replace(second=0, microsecond=0)
    sleep_time = (next_trigger - now).total_seconds()

    print(f"[INFO] Waiting {sleep_time:.2f} seconds until {next_trigger.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(sleep_time)


def measurement_loop():
    """
    This loop will run every 5 minutes and trigger the data to read from the sensor.
    Then it will attempt to send the data to online server.
    If server is not online the data should save locally until connection is made.
    """
    while True:
        wait_until_5_minute()
        data = read_sensor()
        if data:
            if not send_sensor_data(data):
                save_unsent_data(data)


def retry_loop():
    """
    This loop will run every 30 minutes to see if failed data is present and attempt to resend it.
    """
    while True:
        retry_unsent_data()
        time.sleep(1800)


def project_startup():
    # Startup Checks
    load_config()
    startup()

    # Upon startup, two threads will be started for measurement and retry loops.
    measurement_thread = threading.Thread(target=measurement_loop, daemon=True)
    retry_thread = threading.Thread(target=retry_loop, daemon=True)

    print("[INFO] Started measurement thread")
    print("[INFO] Started retry thread")

    measurement_thread.start()
    retry_thread.start()

    # Keep the main thread alive.
    while True:
        time.sleep(10)


def main():
    while True:
        try:
            project_startup()
        except Exception as exc:
            now = datetime.datetime.now()
            print(f"[ERROR - {now}]: {exc}")
            traceback.print_exc()
            # Give a short pause before restarting
            time.sleep(1)
            # Restart the process to reset the system state
            os.execv(sys.executable, [sys.executable] + sys.argv)


if __name__ == "__main__":
    main()
