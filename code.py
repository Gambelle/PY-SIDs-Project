# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time  # for recording time of mode alert trigger
import array
import math
import random
import board
import audiobusio
from adafruit_circuitplayground import cp
from adafruit_circuitplayground.express import cpx

# which mode to run
soundMode = False
pulseMode = False
threeMode = True

# on start temperature vars
alertTemp = 90

# on start breathing vars
notBreathingStartTime = 0
NOT_BREATHING_TIME = 5
breathing = True
startZ, startY, startX = cp.acceleration
breathingMovementZ = 0.0
breathingMovementY = 0.0
breathingMovementX = 0.0
checkZ = False
checkY = False
checkX = False
check = False
notBreathingStartTime = 0

# on start roll over vars
rollStartTime = 0
rolling = False
currentAngle = 0
rad2deg = 52.29578
rollAngle = 60.0
gravity = 9.80665
rollTime = 5


# on start lightshow defs
FLASH_RATE      = 0.250
SPIN_RATE       = 0.100
CYLON_RATE      = 0.100
BEDAZZLE_RATE   = 0.100
CHASE_RATE      = 0.100

# Change these to be whatever color you want
# Use color picker to come up with hex values
FLASH_COLOR     = 0x8B0000
SPIN_COLOR      = 0x4B0082
CYLON_COLOR     = 0x0000CD

# Define 10 colors here.
# Must be 10 entries.
# Use 0x000000 if you want a blank space.
RAINBOW_COLORS = (
  0xFF0000,
  0xFF5500,
  0xFFFF00,
  0x00FF00,
  0x0000FF,
  0xFF00FF,
  0x000000,
  0x000000,
  0x000000,
  0x000000
)


def flasher():
    for x in range(0, 3):
        # Turn on all the pixels to FLASH_COLOR
        cpx.pixels.fill(FLASH_COLOR)

        # Leave them on for a little bit
        time.sleep(FLASH_RATE)

        # Turn off all the NeoPixels
        cpx.pixels.fill(0)

        # Leave them off for a little bit
        time.sleep(FLASH_RATE)

def spinner():
    # Can be any two pixels
    pixel1 = 0
    pixel2 = 5

    for x in range(0, 10):
        # Turn off all the NeoPixels
        cpx.pixels.fill(0)

        # Turn on two pixels to SPIN_COLOR
        cpx.pixels[pixel1] = SPIN_COLOR
        cpx.pixels[pixel2] = SPIN_COLOR

        # Increment pixels to move them around the board
        pixel1 = pixel1 + 1
        pixel2 = pixel2 + 1

        # Check pixel values
        pixel1 = pixel1 if pixel1 < 10 else 0
        pixel2 = pixel2 if pixel2 < 10 else 0

        # Wait a little bit so we don't spin too fast
        time.sleep(SPIN_RATE)

    cpx.pixels.fill(0)

def cylon():
    pixel1 = 0
    pixel2 = 9

    for x in range(0, 3):
        # Scan in one direction
        for step in range(4):
            cpx.pixels.fill(0)

            cpx.pixels[pixel1] = CYLON_COLOR
            cpx.pixels[pixel2] = CYLON_COLOR

            pixel1 = pixel1 + 1
            pixel2 = pixel2 - 1

            time.sleep(CYLON_RATE)

        # Scan back the other direction
        for step in range(4):
            cpx.pixels.fill(0)

            cpx.pixels[pixel1] = CYLON_COLOR
            cpx.pixels[pixel2] = CYLON_COLOR

            pixel1 = pixel1 - 1
            pixel2 = pixel2 + 1

            time.sleep(CYLON_RATE)

    cpx.pixels.fill(0)

def bedazzler():
    for x in range(0, 10):
        # Turn off all the NeoPixels
        cpx.pixels.fill(0)

        # Turn on a random pixel to a random color
        cpx.pixels[random.randrange(10)] = ( random.randrange(256),
                                             random.randrange(256),
                                             random.randrange(256) )

        # Leave it on for a little bit
        time.sleep(BEDAZZLE_RATE)

    cpx.pixels.fill(0)





# forever loop
while True:
    # Temperature Mode
    temp = (cp.temperature * 1.8) + 32
    print("Temperature F: ", temp)
    if temp > alertTemp:
        print("It's too hot!")
        cp.play_tone(300, .2)
        cp.play_tone(400, .2)
        cp.play_tone(500, .2)
        flasher();

    time.sleep(1) # to avoid crash while montioring serial

    # Breating Mode
    breathingMovementZ, breathingMovementY, breathingMovementX = cp.acceleration

    print("  Z: ")
    print(breathingMovementZ)
    print("  Y: ")
    print(breathingMovementY)
    print("  X: ")
    print(breathingMovementX)

    # Check if not breathing
    checkZ = breathingMovementZ >= startZ - 0.05 and breathingMovementZ <= startZ + 0.05
    checkY = breathingMovementY >= startY - 0.05 and breathingMovementY <= startY + 0.05
    checkX = breathingMovementX >= startX - 0.05 and breathingMovementX <= startX + 0.05
    check = checkZ or checkY or checkX

    if check:
        if breathing:
            print("Not breathing")
            breathing = False
            notBreathingStartTime = time.monotonic()
        if not breathing:
            if (time.monotonic() - notBreathingStartTime > NOT_BREATHING_TIME):
                # music.baDing.play()
                # play wav file
                # light.showAnimation(light.sparkleAnimation, 1000)
                # use https://learn.adafruit.com/circuit-playground-bike-light/the-all-of-them-circuitpython
                cp.play_tone(300, .1)  # temperary
                cp.play_tone(400, .1)
                cp.play_tone(600, .2)
                cp.play_tone(400, .1)
                cp.play_tone(300, .1)
                cylon() ;
                print("  sZ: ")
                print(startZ)
                print("  sY: ")
                print(startY)
                print("  sX: ")
                print(startX)
                print("notBreathingStartTime: ")
                print(notBreathingStartTime)
                print("  millis: ")
                print(time.monotonic())
                print("  Not Breathing Time: ")
                print(NOT_BREATHING_TIME)
            else:
                print("Not 5 seconds yet")
                print("  notBreathingStartTime: ")
                print(notBreathingStartTime)
                print("  millis: ")
                print(time.monotonic())
                print("  Not Breathing Time: ")
                print(NOT_BREATHING_TIME)
                print("Difference")
                print(time.monotonic() - notBreathingStartTime)
    else:
        breathing = True

    startZ, startY, startX = cp.acceleration
    time.sleep(1) # to avoid crash while montioring serial

    # RollOver Mode
    x, y, zMotion = cp.acceleration
    currentAngle = (rad2deg * math.asin(abs(zMotion) / gravity))
    if currentAngle > rollAngle and zMotion < 0:
        if (not(rolling)):
            rolling = True
            print("Just started rolling")
            print("Current Angle: ")
            print(currentAngle)
            rollStartTime = time.monotonic()
    elif (abs(currentAngle) > 0):
        rolling = False
        print("Current Angle: ")
        print("Motion Z: ")
        x, y, zMotion = cp.acceleration
        print(zMotion)
        rollStartTime = time.monotonic()

    if (rolling):
        if (time.monotonic() - rollStartTime > rollTime):
            cp.play_tone(100, .1)  # temperary
            cp.play_tone(150, .1)
            cp.play_tone(200, .1)
            cp.play_tone(250, .1)
            cp.play_tone(300, .1)  # temperary
            cp.play_tone(350, .1)
            spinner()     ;
            print("  rollStartTime: ")
            print(rollStartTime)
            print("  millis: ")
            print(time.monotonic())
            print("  Roll Time: ")
            print(rollTime)
        else:
            print("Not 5 seconds yet")
            print("  rollStartTime: ")
            print(rollStartTime)
            print("  millis: ")
            print(time.monotonic())
            print("  Roll Time: ")
            print(rollTime)
            print("Difference")
            print(time.monotonic() - rollStartTime)

    time.sleep(1) # to avoid crash while montioring serial
