#!/usr/bin/env python
# coding: utf-8

import Pose
import pyo
import time
import math

# make sounds with you body, a more modular version

# argument parsing
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--camera", help="camera to use (0, 1, etc)",
                    type=int, default=0)
args = parser.parse_args()

# initialize sound
s = pyo.Server().boot()
s.amp = 0.1
sf1 = pyo.SfPlayer("kick-02.wav", speed=1, loop=False, mul=0.5).out(0)
sf2 = pyo.SfPlayer("hihat-02.wav", speed=1, loop=False, mul=0.5).out(0)
s.start()

# keep last y
last_y1 = 0
last_y2 = 0

# landmark processing function
def process_landmarks(landmarks):

    global sf1, sf2, last_y1, last_y2
    y1 = landmarks[Pose.mp_pose.PoseLandmark.LEFT_INDEX].y
    y2 = landmarks[Pose.mp_pose.PoseLandmark.RIGHT_INDEX].y
    if last_y1 < 0.5 and y1 > 0.5:
        sf1.out(0)
    if last_y2 < 0.5 and y2 > 0.5:
        sf2.out(0)
    last_y1 = y1
    last_y2 = y2

    return {
        "y1": y1,
        "y2": y2,
        "frame_id": Pose.frame_id
        }



# initialize process
Pose.capture(args, process_landmarks)

# stop the the sound (need to delay to let sound shutdown properly)
s.stop()
time.sleep(1)





