import time
import sys
import os
import json
import glob

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging

from waveshare_POE_HAT_B import POE_HAT_B


logging.basicConfig(level=logging.INFO)


def get_available_fonts():
    font_dir = os.path.join(libdir, 'waveshare_POE_HAT_B')
    font_files = glob.glob(os.path.join(font_dir, '*.ttf'))
    return {os.path.basename(f) for f in font_files}


def read_config():
    try:
        with open("/data/options.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logging.warning("Could not read /data/options.json, using defaults")
        return {}


available_fonts = get_available_fonts()
logging.info(f"Available fonts: {sorted(available_fonts)}")

config = read_config()
fan_temp = config.get("fan_temp", 43)
brightness = config.get("brightness", 255)
font_name = config.get("font", "Courier_New.ttf")

if font_name not in available_fonts:
    logging.warning(f"Font '{font_name}' not found, falling back to Courier_New.ttf")
    font_name = "Courier_New.ttf"

POE = POE_HAT_B.POE_HAT_B(brightness=brightness, font_name=font_name)

try:
    while True:
        config = read_config()

        new_fan_temp = config.get("fan_temp", 43)
        new_brightness = config.get("brightness", 255)
        new_font_name = config.get("font", "Courier_New.ttf")

        if new_font_name not in available_fonts:
            new_font_name = "Courier_New.ttf"

        if new_brightness != brightness:
            brightness = new_brightness
            POE.set_brightness(brightness)
            POE.POE_HAT_Display(fan_temp)
            logging.info(f"Brightness updated to {brightness}")

        if new_fan_temp != fan_temp:
            fan_temp = new_fan_temp
            logging.info(f"Fan temperature threshold updated to {fan_temp}")

        if new_font_name != font_name:
            font_name = new_font_name
            POE.set_font(font_name)
            logging.info(f"Font updated to {font_name}")

        POE.POE_HAT_Display(fan_temp)
        time.sleep(1)

except KeyboardInterrupt:
    print("ctrl + c:")
    POE.FAN_OFF()
