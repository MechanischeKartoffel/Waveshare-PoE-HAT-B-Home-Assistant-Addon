import logging
import sys
import time
import smbus2 as smbus

import os
import socket
from PIL import Image,ImageDraw,ImageFont
from . import SSD1306


dir_path = os.path.dirname(os.path.abspath(__file__))


class POE_HAT_B:
    def __init__(self, address=0x20, brightness=255, font_name='Courier_New.ttf'):
        self.i2c = smbus.SMBus(1)
        self.address = address
        self.show = SSD1306.SSD1306()
        self.show.Init()
        self.show.SetBrightness(brightness)
        self._font_name = font_name
        self._load_fonts(font_name)
        self.FAN_ON()
        self.FAN_MODE = 0

    def _load_fonts(self, font_name):
        font_path = os.path.join(dir_path, font_name)
        if not os.path.exists(font_path):
            logging.warning(f"Font '{font_name}' not found, falling back to Courier_New.ttf")
            font_path = os.path.join(dir_path, 'Courier_New.ttf')
            self._font_name = 'Courier_New.ttf'
        self.font = ImageFont.truetype(font_path, 13)
        self.font_small = ImageFont.truetype(font_path, 12)

    def set_brightness(self, value):
        self.show.SetBrightness(value)

    def set_font(self, font_name):
        if font_name != self._font_name:
            self._font_name = font_name
            self._load_fonts(font_name)

    def FAN_ON(self):
        self.i2c.write_byte(self.address, 0xFE & self.i2c.read_byte(self.address))

    def FAN_OFF(self):
        self.i2c.write_byte(self.address, 0x01 | self.i2c.read_byte(self.address))

    def GET_IP(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            ip = '0.0.0.0'
        return ip

    def GET_Temp(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'rt') as f:
            temp = (int)(f.read()) / 1000.0
        return temp

    def POE_HAT_Display(self, FAN_TEMP):
        image1 = Image.new('1', (self.show.width, self.show.height), "WHITE")
        draw = ImageDraw.Draw(image1)
        ip = self.GET_IP()
        temp = self.GET_Temp()
        draw.text((0,1), 'IP:'+str(ip), font = self.font, fill = 0)
        draw.text((0,15), 'Temp:'+ str(((int)(temp*10))/10.0), font = self.font, fill = 0)
        if(temp>=FAN_TEMP):
            self.FAN_MODE = 1

        elif(temp<FAN_TEMP-2):
            self.FAN_MODE = 0

        if(self.FAN_MODE == 1):
            draw.text((77,16), 'FAN:ON', font = self.font_small, fill = 0)
            self.FAN_ON()
        else:
            draw.text((77,16), 'FAN:OFF', font = self.font_small, fill = 0)
            self.FAN_OFF()
        self.show.ShowImage(self.show.getbuffer(image1))
