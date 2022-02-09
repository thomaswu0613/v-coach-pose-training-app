import cv2
import mediapipe as mp
from scoring_manager import ScoringManager
from stageman import StageManager
from tools import BodyLandMarks


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
sm = StageManager("./execises/test")
ssm = ScoringManager("./execises/test")
old = -1
lastest = 0
rap_changed = False
frame_count = 0
frame_buffer_list = []

cap = cv2.VideoCapture(-1)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=2) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
      continue
      # print("Ignoring empty camera frame.")
      # # If loading a video, use 'break' instead of 'continue'.
      # break

    frame_count += 1
    # if len(frame_buffer_list) > 10:
    #   frame_buffer_list = frame_buffer_list[5:]

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    try:
      lm = BodyLandMarks(results,mp_pose)
    except:
      continue
    print("lm:",lm)
    blm = lm.return_all_points()
    frame_buffer_list.append(blm)
    stage,rep = sm.judge_stage(blm)
    
    
    lastest = stage
    if lastest == old:
      rap_changed = False
    elif lastest != old:
      rap_changed = True
      old = lastest
      
    if rap_changed:
      sim = ssm.score(stage,frame_buffer_list[(frame_count-6):(frame_count+6)])
      print("sim:",sim)
    print("Is rap changed:",rap_changed)
      

    print("Current Stage : ",stage,"Rep count",rep)
    

    # print("current stage:",cur_stage)
    # Draw the pose annotation on the image.
    
    image.flags.writeable = True
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    image = cv2.flip(image, 1)
    
    cv2.putText(image, "Current Rep Count : {}".format(rep), (5,20 ), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.putText(image, "Current Stage : {}".format(stage), (5,50 ), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.putText(image, "Is rap changed : {}".format(str(rap_changed)), (5,75 ), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.putText(image, "Stage {} similarity : {}".format(stage,sim), (5,100 ), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow('MediaPipe Pose', image)

    
    key = cv2.waitKey(5)
    if key == 27:
      
      break
cap.release()
ssm.close()
sm.close()