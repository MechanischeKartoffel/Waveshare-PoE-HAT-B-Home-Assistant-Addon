import time
import sys
import os
import json

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging

from waveshare_POE_HAT_B import POE_HAT_B


logging.basicConfig(level=logging.INFO)

try:
    with open("/data/options.json", "r") as f:
        config = json.load(f)
    fan_temp = config.get("fan_temp", 43)
except (FileNotFoundError, json.JSONDecodeError):
    logging.warning("Could not read /data/options.json, using default fan_temp=43")
    fan_temp = 43

POE = POE_HAT_B.POE_HAT_B()

try:
    while True:
        POE.POE_HAT_Display(fan_temp)
        time.sleep(1)

except KeyboardInterrupt:
    print("ctrl + c:")
    POE.FAN_OFF()
