import Sound
import Pose

# https://developers.google.com/android/reference/com/google/mlkit/vision/pose/PoseLandmark

# empty landmark processor
def process_landmarks_empty(landmark):
    return {}

# landmark processor
def process_landmarks(landmark):

    y1 = landmark[Pose.mp_pose.PoseLandmark.LEFT_INDEX].y
    y2 = landmark[Pose.mp_pose.PoseLandmark.RIGHT_INDEX].y

    n1 = Sound.y_note(y1, Sound.scale1)
    n2 = Sound.y_note(y2, Sound.scale2)

    Sound.osc4.setFreq(n1.frequency())
    Sound.osc5.setFreq(n2.frequency())

    return {
        "n1": note_info(n1), 
        "n2": note_info(n2),
        }
    
def note_info(note):
    return "%s %.1f" % (note.scientific_notation(), note.frequency()) 






