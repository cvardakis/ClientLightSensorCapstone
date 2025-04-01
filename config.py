import os

SERIAL_PORT = None
BAUD_RATE = 115200
LOCAL_TIMEZONE = 'America/Denver'
OS = None

# Server API Endpoints
SERVER_URL = "http://localhost:8000"
AUTH_ENDPOINT = f"{SERVER_URL}/sensor-auth"
DATA_ENDPOINT = f"{SERVER_URL}/sensor-data"

# Sensor Configuration
REGISTRATION_KEY = "test"
LOCATION = "Building A"
SENSOR_ID = "STANDIN"
NAME = "Sensor One"
LAT = 40.9875
LONG = 19.08945
ELEVATION = 4500
AUTHENTICATED = False

# Config File Path
FILE_PATH = "./"
FILE = "config"


def set_serial(serial_port: str):
    global SERIAL_PORT
    SERIAL_PORT = serial_port
    print(f"[CONFIG] SERIAL_PORT: {SERIAL_PORT}")


def set_baud(baud: int):
    global BAUD_RATE
    BAUD_RATE = baud
    print(f"[CONFIG] BAUD: {BAUD_RATE}")


def set_timezone(timezone: str):
    global LOCAL_TIMEZONE
    LOCAL_TIMEZONE = timezone
    print(f"[CONFIG] LOCAL_TIMEZONE: {LOCAL_TIMEZONE}")


def set_os(operating_system: str):
    global OS
    OS = operating_system
    print(f"[CONFIG] OS: {OS}")


def set_server_url(url: str):
    global SERVER_URL
    SERVER_URL = url
    print(f"[CONFIG] SERVER_URL: {SERVER_URL}")


def set_auth_url(url: str):
    global AUTH_ENDPOINT
    AUTH_ENDPOINT = f"{SERVER_URL}{url}"
    print(f"[CONFIG] AUTH_ENDPOINT: {AUTH_ENDPOINT}")


def set_data_url(url: str):
    global DATA_ENDPOINT
    DATA_ENDPOINT = f"{SERVER_URL}{url}"
    print(f"[CONFIG] DATA_ENDPOINT: {DATA_ENDPOINT}")


def set_registration_key(key: str):
    global REGISTRATION_KEY
    REGISTRATION_KEY = key
    print(f"[CONFIG] REGISTRATION_KEY: {REGISTRATION_KEY}")


def set_location(location: str):
    global LOCATION
    LOCATION = location
    print(f"[CONFIG] LOCATION: {LOCATION}")


def set_id(sensor_id: str):
    global SENSOR_ID
    SENSOR_ID = sensor_id
    print(f"[CONFIG] SENSOR_ID: {SENSOR_ID}")


def set_name(name: str):
    global NAME
    NAME = name
    print(f"[CONFIG] NAME: {NAME}")


def set_lat(lat: float):
    global LAT
    LAT = lat
    print(f"[CONFIG] LAT: {LAT}")


def set_lon(lon: float):
    global LONG
    LONG = lon
    print(f"[CONFIG] LONG: {LONG}")


def set_elevation(elevation: float):
    global ELEVATION
    ELEVATION = elevation
    print(f"[CONFIG] ELEVATION: {ELEVATION}")


def set_auth(authenticated: bool):
    global AUTHENTICATED
    AUTHENTICATED = authenticated
    print(f"[CONFIG] AUTHENTICATED: {AUTHENTICATED}")


def set_file_path(file_path: str):
    global FILE_PATH
    FILE_PATH = file_path
    print(f"[CONFIG] FILE_PATH: {FILE_PATH}")


def set_file(file: str):
    global FILE
    FILE = file
    print(f"[CONFIG] FILE: {FILE}")


def load_config():
    print("[INFO] Loading config...")
    # Mapping of config keywords to their corresponding set functions.
    # For some values, we wrap the setter in a lambda to handle type conversion.
    setters = {
        'SERIAL_PORT': set_serial,
        'BAUD_RATE': lambda v: set_baud(int(v)),
        'LOCAL_TIMEZONE': set_timezone,
        'OS': set_os,
        'SERVER_URL': set_server_url,
        'AUTH_ENDPOINT': set_auth_url,
        'DATA_ENDPOINT': set_data_url,
        'REGISTRATION_KEY': set_registration_key,
        'LOCATION': set_location,
        'SENSOR_ID': set_id,
        'NAME': set_name,
        'LAT': lambda v: set_lat(float(v)),
        'LONG': lambda v: set_lon(float(v)),
        'ELEVATION': lambda v: set_elevation(float(v)),
        'AUTHENTICATED': lambda v: set_auth(v.lower() in ("true", "1", "yes")),
        'FILE_PATH': set_file_path,
        'FILE': set_file,
    }

    # Open the configuration file using the global FILE_PATH and FILE
    if os.path.exists(os.path.join(FILE_PATH, FILE)):
        with open(os.path.join(FILE_PATH, FILE), "r") as config_file:
            for line in config_file:
                line = line.strip()
                # Skip empty lines or comments
                if not line or line.startswith('#'):
                    continue
                try:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # Only call the set function if the keyword is in our mapping.
                    if key in setters:
                        setters[key](value)
                except Exception as e:
                    print(f"Failed to process line: {line}. Error: {e}")
