import cv2
import mediapipe as mp


# general setup
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# capture frames loop
def capture(args, process_landmarks):

    info = {}

    # For webcam input:
    cap = cv2.VideoCapture(args.camera)
    print("cap: %s" % cap)
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
            info = process_landmarks(results.pose_landmarks.landmark)
        
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
        for text in ["%s: %s" % (key, str(info[key])) for key in info]:
            cv2.putText(image, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0,0,255), 2, cv2.LINE_AA)
            y += 40


        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break
    cap.release()






