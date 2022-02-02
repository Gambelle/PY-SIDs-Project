# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time  # for recording time of mode alert trigger
from adafruit_circuitplayground import cp
import math

# on start temperature vars
alertTemp = 74
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

# forever loop
while True:
    # Temperature Mode
    temp = (cp.temperature * 1.8) + 32
    print("Temperature F: ", temp)
    if temp > alertTemp:
        print("It's too hot!")
        cp.play_tone(300, 1)  # temperary

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
                cp.play_tone(262, 1)  # temperary
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
            cp.play_tone(370, 1)  # temperary
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
