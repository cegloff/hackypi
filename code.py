# This Programme is for Windows, but it adjustable for every OS 
import time
import os
import board
import usb_hid
import digitalio
import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard, Keycode
from keyboard_layout_win_uk import KeyboardLayout
from adafruit_st7789 import ST7789
import time
import storage

# First set some parameters used for shapes and text
BORDER = 12
FONTSCALE = 2
FONTSCALE1 = 3


BACKGROUND_COLOR = 0xFF0000  # red
FOREGROUND_COLOR = 0xFFFF00  # Purple
TEXT_COLOR = 0x000000

# Release any resources currently in use for the displays
displayio.release_displays()

tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
tft_bl  = board.GP13
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

tft_bl  = board.GP13
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=270, width=240, height=135,rowstart=40, colstart=53)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

def inner_rectangle():
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(display.width - BORDER * 2, display.height - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)
inner_rectangle()

# Draw a label
text = "Welcome to"
text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
text_group = displayio.Group(scale=FONTSCALE1,x=30,y=40,)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

text1 = "HackyPi"
text_area1 = label.Label(terminalio.FONT, text=text1, color=TEXT_COLOR)
text_group1 = displayio.Group(scale=FONTSCALE1,x=50,y=80,)
text_group1.append(text_area1)  # Subgroup for text scaling
splash.append(text_group1)

time.sleep(0.3)

try:
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayout(keyboard)
    time.sleep(0.3)
    keyboard.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(0.3)
    keyboard_layout.write('cmd.exe')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.3)
    keyboard.send(Keycode.F11)
    time.sleep(0.3)
    keyboard_layout.write("start https://shop.sb-components.co.uk")
    keyboard.send(Keycode.ENTER)
    keyboard.release_all()
except Exception as ex:
    keyboard.release_all()
    raise ex

time.sleep(0.3)

def inner_rectangle1():
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(display.width - BORDER * 2, display.height - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x00FFFF#cryon
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)
inner_rectangle1()

# Draw a label
text = "SB COMPONENTS"
text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
text_group = displayio.Group(scale=FONTSCALE,x=20,y=30,)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

# Draw a label
text1 = "THANKS FOR BUYING"
text_area1 = label.Label(terminalio.FONT, text=text1, color=TEXT_COLOR)
text_group1 = displayio.Group(scale=FONTSCALE,x=20,y=60,)
text_group1.append(text_area1)  # Subgroup for text scaling
splash.append(text_group1)

text3 = "OUR PRODUCTS...."
text_area3 = label.Label(terminalio.FONT, text=text3, color=TEXT_COLOR)
text_group3 = displayio.Group(scale=FONTSCALE,x=20,y=90,)
text_group3.append(text_area3)  # Subgroup for text scaling
splash.append(text_group3)

time.sleep(0.3)

import adafruit_sdcard
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
cs = digitalio.DigitalInOut(board.GP17)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

def print_directory(path, tabs=0):
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if filesize < 1000:
            sizestr = str(filesize) + " bytes"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)

        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print("{0:<40} Size: {1:>10}".format(prettyprintname, sizestr))

        # recursively print directory contents
        if isdir:
            print_directory(path + "/" + file, tabs + 1)


print("Files on filesystem:")
print("====================")
print_directory("/sd")
