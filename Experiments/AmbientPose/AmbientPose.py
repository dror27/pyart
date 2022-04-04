#!/usr/bin/env python
# coding: utf-8

import Pose
import Sound
import Process

# make sounds with you body, a more modular version

# argument parsing
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--camera", help="camera to use (0, 1, etc)",
                    type=int, default=0)
parser.add_argument("--scale", help="name of scale to use, defaults to minor_pentatonic",
                    default="minor_pentatonic")
parser.add_argument("--list-scales", help="list all available scales",
                    action="store_true")
args = parser.parse_args()

# print scales?
if args.list_scales:
    for s in Sound.all_scales():
        print(s)
    quit()

# initialize process
Sound.start(args)
Pose.capture(args, Process.process_landmarks)
Sound.stop()







