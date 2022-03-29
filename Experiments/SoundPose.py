#!/usr/bin/env python
# coding: utf-8
# make sounds with you body

# argument parsing
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--camera", help="camera to use (0, 1, etc)",
                    type=int, default=0)
args = parser.parse_args()


# generate note frequencies
all_notes = []
for i in range(12 + 13):
    f = 110 * (2 ** (i/12))
    all_notes.append(f)
print(all_notes)

# slice a pendatonic scale
notes = [all_notes[i] for i in [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24]]


# start sound engine
from pyo import *
s = Server().boot()
t = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
beat = Beat(time=.100, taps=16, w1=[90,80], w2=50, w3=35, poly=1).play()
tr2 = TrigEnv(beat, table=t, dur=beat['dur'], mul=beat['amp'])

lfo4 = Sine(0.1).range(0.1, 0.75)
osc4 = SuperSaw(freq=notes[0], detune=lfo4, mul=tr2*0.3).out(1)
lfo5 = Sine(0.1888).range(0.1, 0.75)
osc5 = SuperSaw(freq=notes[5], detune=lfo5, mul=tr2*0.3).out(2)
sf = SfPlayer("kick-02.wav", speed=1, loop=True, mul=0.5).out()


# define motion processors
def y_freq(y):
    y = min(1.0, max(0.0, y))
    return notes[int((1 - y) * (len(notes) - 1))]

def process_landmark(landmark):

    y1 = landmark[19].y
    y2 = landmark[20].y

    f1 = y_freq(y1)
    f2 = y_freq(y2)*2

    osc4.setFreq(f1)
    osc5.setFreq(f2)

    return {"f1":f1, "f2":f2}
    

# start pose detection
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# start sound
s.start()

info = {}

# For webcam input:
cap = cv2.VideoCapture(args.camera)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # process landmarks
    if results.pose_landmarks:
        info = process_landmark(results.pose_landmarks.landmark)
    
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # Flip the image horizontally for a selfie-view display.
    image = cv2.flip(image, 1)

    # put text
    y = 50
    for text in ["%s: %.1f" % (key, info[key]) for key in info]:
        cv2.putText(image, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,255), 2, cv2.LINE_AA)
        y += 40


    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

s.stop()






