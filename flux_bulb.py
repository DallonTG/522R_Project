#!/usr/bin/env python

import colorsys
import math
import sys
import time
import argparse
import re
import pexpect

SATURATION = 1.0         # Constant val for color saturation - full saturation
VALUE      = 1.0         # Constant val for value - full value
SLEEP_TIME  = 0.01       # Time to sleep between loop iterations

# Parse args
parser = argparse.ArgumentParser(description='Control a Flux BLE Bulb')
parser.add_argument('mac',help='Bluetooth MAC address in format xx:xx:xx:xx:xx:xx',	type=str)
args = parser.parse_args()
bulb = args.mac

# Run gatttool
gatt = pexpect.spawn('gatttool -I')

# Connect to the bulb
gatt.sendline('connect {0}'.format(bulb))
gatt.expect('Connection successful')

# Start at minimum hue.
hue = 0

# Turn bulb on
line = 'char-write-cmd 0x002e cc2333'
gatt.sendline(line)

time.sleep(1)

try:
    while True:
        # How much to change hue by on every iteration
        hue_delta = .1
        hue += hue_delta
        r, g, b = map(lambda x: int(x*255.0), colorsys.hsv_to_rgb(hue, SATURATION, VALUE))
        # Format the packet and send it
        line = 'char-write-cmd 0x002e 56{0:02X}{1:02X}{2:02X}00f0aa'.format(r, g, b)
        print line
        gatt.sendline(line)
        # Wait before next iteration
        time.sleep(SLEEP_TIME)
except KeyboardInterrupt:
    # turn off the light and disconnect on exit
    line = 'char-write-cmd 0x002e cc2433'
    time.sleep(SLEEP_TIME)
    gatt.sendline(line)
    time.sleep(SLEEP_TIME)
    gatt.sendline('disconnect')
