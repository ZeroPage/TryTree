#!/usr/bin/env python3
#
# Christmas Tree Lighting
#

import time
import signal
import sys
import RPi.GPIO as GPIO

def sigint_handler(sig, frame):
    GPIO.cleanup()
    print()
    sys.exit(0x1)

signal.signal(signal.SIGINT, sigint_handler)

pins = (6, 13, 19, 26)
pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))

idxs = tuple(range(8))
star_idx = len(idxs) - 1

divtime = 1000

def light_on(led_idx):
    pin1 = pins[pairs[led_idx // 2][0]]
    pin2 = pins[pairs[led_idx // 2][1]]

    for pin in pins:
        if pin == pin1:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False if led_idx % 2 else True)
        elif pin == pin2:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, True if led_idx % 2 else False)
        else:
            GPIO.setup(pin, GPIO.IN)

GPIO.setmode(GPIO.BCM)

while True:
    for i in range(3 * divtime):
        for idx in idxs:
            light_on(idx)
        time.sleep(1 / divtime)

    for i in range(3):
        for i in range(divtime):
            for idx in idxs[::2]:
                light_on(idx)
            light_on(star_idx)
            time.sleep(1 / divtime)

        for i in range(divtime):
            for idx in idxs[1::2]:
                light_on(idx)
            light_on(star_idx)
            time.sleep(1 / divtime)

    t = 100
    while (t > 10):
        for i in range(3):
            for i in range(int(divtime / (len(idxs) * t))):
                for idx in idxs:
                    light_on(idx)
                    time.sleep(t / divtime)
        t /= 2

# GPIO.cleanup()
