# Considered making a fronted for variable manipulation, but never came to fruition

import tkinter as tk
from tkinter import messagebox
import os

# Global configuration file settings
FILE_PATH = "./"
FILE = "config"

# List of all configuration keys
CONFIG_KEYS = [
    "SERIAL_PORT",
    "BAUD_RATE",
    "LOCAL_TIMEZONE",
    "OS",
    "SERVER_URL",
    "AUTH_ENDPOINT",
    "DATA_ENDPOINT",
    "REGISTRATION_KEY",
    "LOCATION",
    "SENSOR_ID",
    "NAME",
    "LAT",
    "LONG",
    "ELEVATION",
    "AUTHENTICATED",
    "FILE_PATH",
    "FILE"
]


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Create a canvas and a vertical scrollbar for scrolling it
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Position the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create a frame inside the canvas to hold the content
        self.scrollable_frame = tk.Frame(self.canvas)

        # Bind a configuration event to update the scrollregion
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create a window inside the canvas to hold the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")


window = tk.Tk()

window.title("Frontend")
window.geometry("500x500")
window.configure(background="white")

scrollable = ScrollableFrame(window)
scrollable.pack(fill="both", expand=True)

for i, text in enumerate(CONFIG_KEYS):
    label = tk.Label(scrollable.scrollable_frame, text=text, bg="white", fg="black", anchor="w", justify="left")
    label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

    entry = tk.Entry(scrollable.scrollable_frame, bg="white", fg="black")
    entry.grid(row=i, column=1, sticky="we", padx=10, pady=5)

    entry.insert(0, "DEFAULT")

window.mainloop()
