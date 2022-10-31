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
parser.add_argument("--add-beat", help="add a base drum beat",
                    action="store_true")
parser.add_argument("--bpm", help="beats per minute",
                    type=int, default=120)
parser.add_argument("--beat-pattern", help="bitwise beat pattern",
                    type=int, default=1)
parser.add_argument("--note-left", help="lower note on left",
                    default="A2")
parser.add_argument("--note-right", help="lower note on left",
                    default="A3")
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







