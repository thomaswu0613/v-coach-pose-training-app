import cv2
import yaml
import mediapipe as mp
import traceback
import numpy as np
import os

#variables declartion
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
stage_number = 0
exceise_name = "test_exceise"

#read exceises path config
f = open("./path.yml","r")
path_config = yaml.load(f,Loader=yaml.FullLoader)

#calc angle
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    if sum(a)+sum(b)+sum(c) > 5:
        return None
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def get_stages(exceise_dir):
    return len([name for name in os.listdir(exceise_dir) if os.path.isfile(os.path.join(exceise_dir, name))])

cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip Image
    cv2.flip(image,1)
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = pose.process(image)

    try:

        #Get points (x,y) and calc angle
        landmarks = results.pose_landmarks.landmark
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        elbow_right = calculate_angle(right_shoulder, right_elbow, right_wrist)
        elbow_left = calculate_angle(left_shoulder, left_elbow, left_wrist)
        knee_right = calculate_angle(right_hip, right_knee, right_ankle)
        knee_left = calculate_angle(left_hip, left_knee, left_ankle)
        hip_left = calculate_angle(left_hip, right_hip, left_knee)
        points = {"elbow_left":elbow_left,"elbow_right":elbow_right,"knee_left":knee_left,"knee_right":knee_left,"hip_left":hip_left}

        #Read yaml stage file
        f = open("{}/stage{}.yaml".format(path_config[exceise_name],stage_number),"r")
        yml = yaml.load(f,Loader=yaml.FullLoader)


        #Stage_scoring
        stage_scoring = []
        for i in range(0,len(yml)-1):
            print(yml[i])

            try:
                if yml[i]["Standards"]["Basic"]["min"] <= points[yml[i]["Angle_Name"]] <= yml[i]["Standards"]["Basic"]["max"]:
                    stage_scoring.append(1)
            except TypeError:
                print("Not enough points")

        print("----------------")
        print("Stage Scoring : {}".format(sum(stage_scoring)))
        print(stage_scoring)
        print(points)
        print("----------------")

        if sum(stage_scoring) >= len(yml)*0.75:
            if stage_number == get_stages(path_config["test_exceise"])-1:
                stage_number = 0
            else:
                stage_number += 1

        print("Stage:{}".format(stage_number))
        image = cv2.putText(image, "Stage:"+str(stage_number), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 
                   2, (0,0,255), 3, cv2.LINE_AA)

    except AttributeError:
        print("No body detected.")


    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )
    cv2.imshow('MediaPipe Pose', image)

    key = cv2.waitKey(5)
    if key in [27,ord("q")]:
      break
cap.release()