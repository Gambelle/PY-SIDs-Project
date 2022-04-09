# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import audiobusio
import array
import math
import board
import random
from adafruit_circuitplayground import cp
from adafruit_circuitplayground.express import cpx


BEDAZZLE_RATE   = 0.100
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


#---| User Configuration |---------------------------
SAMPLERATE = 16000
SAMPLES = 1024
THRESHOLD = 100
MIN_DELTAS = 5
DELAY = 0.2
#----------------------------------------------------
def normalized_rms(values):
    minbuf = sum(values) / len(values)
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values)

    return math.sqrt(samples_sum / len(values))

def mean(values):
    return sum(values) / len(values)

# Create a buffer to record into
samples = array.array('H', [0] * SAMPLES)

# Setup the mic input
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK,
                       board.MICROPHONE_DATA,
                       sample_rate=SAMPLERATE,
                       bit_depth=16)

alertDB = 130
alertHZlow = 1000.5
alertHZhigh = 1700
spectrum = 0
avg = 0

while True:
    mic.record(samples, SAMPLES)

    magnitude = normalized_rms(samples)


    # Compute DC offset (mean) and threshold level
    mean = int(sum(samples) / len(samples) + 0.5)
    threshold = mean + THRESHOLD

    # Compute deltas between mean crossing points
    # (this bit by Dan Halbert)
    deltas = []
    last_xing_point = None
    crossed_threshold = False
    for i in range(SAMPLES-1):
        sample = samples[i]
        if sample > threshold:
            crossed_threshold = True
        if crossed_threshold and sample < mean:
            if last_xing_point:
                deltas.append(i - last_xing_point)
            last_xing_point = i
            crossed_threshold = False

    # Try again if not enough deltas
    if len(deltas) < MIN_DELTAS:
        continue

    # Average the deltas
    mean = sum(deltas) / len(deltas)

    # Compute frequency
    freq = SAMPLERATE / mean


    print("crossings: {}  mean: {}  freq: {} ".format(len(deltas), mean, freq))

    print("Sound level: ", magnitude)
    print("Freq level: ", freq)
    if (alertHZlow < freq and alertHZhigh > freq):
        print("right freq detected")
        if (alertDB < magnitude):
            cp.play_tone(600, .2)  # temperary
            cp.play_tone(300, .2)
            cp.play_tone(600, .2)
            bedazzler();
    time.sleep(0.1)
