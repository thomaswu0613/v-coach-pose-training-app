import traceback
import cv2
import mediapipe as mp
import os
import sys

sys.path.insert(0, '/home/thomasw/workspace/v-coach/scoring_lib')

from calculations import get_Score




mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
fourcc = cv2.VideoWriter_fourcc('F','M','P','4')
out = cv2.VideoWriter("./tmp.mp4",fourcc,15.0,(640,480),True)


def  TUIMenu ( exceise_dir ):
    count = 0
    exceises = {}
    ok = False
    print("------------------------")
    for  name  in  os . listdir ( exceise_dir ):
        exceises[str(count)] = name
        print("{}. : {}".format(count,name))
    print("------------------------")
    print("")
    while True:
        try:
            ans = input("Please Enter the number of the exceise you want to practise : ")
            if int(ans) > count:
                pass
            else:
                ok = True
        except ValueError:
            print("Please enter nummber !")
        else:
            if  ok :
                return exceises[ans]
                break
            else:
                pass

lookup = TUIMenu("./lookups")

cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.4,
    model_complexity=2,
    min_tracking_confidence=0.4) as pose:
  while cap.isOpened():
    success, image = cap.read()
    
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    out.write(image)
    print("fps:"+str(round(cap.get(cv2.CAP_PROP_FPS))))
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Get landmarks
    # if results is not None:
    #   lm = BodyLandMarks(results, mp_pose)
    #   try:
    #     print("--------------")
    #     print(lm.return_all_points())
    #     print("--------------")
    #   except:
    #     traceback.print_exc()

    

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
out.release()

lookup = "./lookups/"+lookup
action = lookup.replace(".pickle", "")
action = action.replace("./lookups/", "")
action = action.replace("_", " - ")
print(action)
video = "./tmp.mp4"

g = get_Score(lookup)
final_score,score_list = g.calculate_Score(video,action)
print(final_score)
print(score_list)