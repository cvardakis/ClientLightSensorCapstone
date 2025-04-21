"""
File: write_file.py
Author: connorvardakis
Date: 2/23/25
Updated: 2/7/25
Description: This is a test file to do tests that I think is necessary
             Tests to see if data cleaning function was working
"""
import os.path
from sensor_reader import clean_value

# payload = {
#                 "utc": utc_str,
#                 "local": local_str,
#                 "temp": data["temp"],
#                 "counts": data["counts"],
#                 "frequency": data["frequency"],
#                 "reading": data["reading"]
#             }
FILE_DIRECTORY = "./logs/"
FILE = "data.txt"
FILE_UX = "data2.txt"


def write_file(collection):
    data = list(collection.values())
    print(data)

    utc = data[0]
    local = data[1]
    temp = data[2]
    counts = data[3]
    freq = data[4]
    readings = data[5]
    with open(os.path.join(FILE_DIRECTORY, FILE), 'a') as file:
        file.write(f"{utc},{local},{temp},{counts},{freq},{readings}\n")
        file.close()

    print(f"[INFO] Data written to {os.path.join(FILE_DIRECTORY, FILE)}")


def test_clean_function():
    data = []
    with open(os.path.join(FILE_DIRECTORY, FILE), "r") as input_file:
        for line in input_file:
            data.append(line)

    with open(os.path.join(FILE_DIRECTORY, FILE_UX), "w") as output_file:
        for line in data:
            parsed = line.split(",")
            cleaned_values = [clean_value(value) for value in parsed]

            output = ",".join(cleaned_values)
            output_file.write(f"{output}\n")


# def write_ux_file(collection):
#     data = list(collection.values())
#     print(data)
#
#     utc = data[0]
#     local = data[1]
#     temp = data[2]
#     counts = data[3]
#     freq = data[4]
#     readings = data[5]
#     with open(os.path.join(FILE_DIRECTORY, FILE_UX), 'a') as file:
#         file.write(f"{utc},{local},{temp},{counts},{freq},{readings}\n")
#         file.close()
#
#     print(f"[INFO] Data written to {os.path.join(FILE_DIRECTORY, FILE)}")
