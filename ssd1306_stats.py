# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.truetype("/home/admin/DejaVuSans.ttf", 10)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname"
    HOST = subprocess.check_output(cmd, shell=True).decode("utf-8")

    #cmd = "hostname -I | cut -d' ' -f1"
    cmd = "ifconfig eth0 2> /dev/null | awk '/^eth/{s=$1;getline;print s,$2}'"

    eth0 = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    cmd = "ifconfig eth0.10 2> /dev/null | awk '/^eth/{s=$1;getline;print s,$2}'"

    
    eth0_10 = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    cmd = 'cut -f 1 -d " " /proc/loadavg'
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
#    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB\", $3,$2,$3*100/$2 }'"

    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
#    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB", $3,$2,$5}\''

    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    cmd = "vcgencmd measure_temp | cut -f2 -d '='"
    TEMP =  subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    # Write four lines of text.

    draw.text((x, top + 0), "HOST: " + HOST, font=font, fill=255)
    draw.text((x, top + 11), "CPU load: " + CPU, font=font, fill=255)
    draw.text((x, top + 21), "CPU temp: " + TEMP, font=font, fill=255)
    draw.text((x, top + 31), MemUsage, font=font, fill=255)
    draw.text((x, top + 41), eth0_10 , font=font, fill=255)
    if "." in eth0:
       draw.text((x, top + 51), eth0, font=font, fill=255)
    
    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(1.0)
