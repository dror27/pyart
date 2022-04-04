#!/usr/bin/env python
# coding: utf-8

import Pose
import pyo
import time

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
osc = pyo.Sine().out()
s.start()

# landmark processing function
def process_landmarks(landmarks):

    if (Pose.frame_id % 4) != 0:
        return None

    y = landmarks[Pose.mp_pose.PoseLandmark.LEFT_INDEX].y

    global osc
    f = 220 * (2 - y)
    osc.setFreq(f)

    return {
        "y": y,
        "f": f, 
        "frame_id": Pose.frame_id
        }



# initialize process
Pose.capture(args, process_landmarks)

# stop the the sound (need to delay to let sound shutdown properly)
s.stop()
time.sleep(1)





