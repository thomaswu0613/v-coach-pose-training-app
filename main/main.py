import cv2
import yaml
import mediapipe as mp
import traceback
import numpy as np
import os
import pathlib

#variables declartion
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
stage_number = 0
base_path = pathlib.Path(os.path.abspath(os.getcwd())).parent



#TUI Menu
def TUIMenu(exceise_dir):
    count = 0
    exceises = {}
    ok = False
    print("------------------------")
    for name in os.listdir(exceise_dir):
        exceises[str(count)] = name
        print("{}. : {}".format(count,name))
    print("------------------------")
    print("")
    while True:
        try:
            ans = input("Please Enter the number of the exceise you want to practise : ")
            int(ans)
            if int(ans) > count:
                pass
            else:
                ok = True
        except ValueError:
            print("Please enter nummber !")
        else:
            if ok:
                return exceises[ans]
                break
            else:
                pass
            
exceise_name = TUIMenu("{}\exceises".format(base_path))
print("Exceise Selected : {}".format(exceise_name))


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
    min_detection_confidence=0.5,
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

    #create empty frame to display data
    data = np.zeros([600,600,3])

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
        f = open("{}\exceises\{}\stage{}.yaml".format(base_path,exceise_name,stage_number),"r")
        yml = yaml.load(f,Loader=yaml.FullLoader)


        #Stage_scoring and Pose scoring
        stage_scoring = []
        overall = []
        for i in range(0,len(yml)-1):
            print(yml[i])

            try:

                #Stage Scoring

                if yml[i]["Standards"]["Basic"]["min"] <= points[yml[i]["Angle_Name"]] <= yml[i]["Standards"]["Basic"]["max"]:
                    stage_scoring.append(1)

                #Pose Scoring

                if yml[i]["Standards"]["Perfect"]["min"] <= points[str(yml[i]["Angle_Name"])] < yml[i]["Standards"]["Perfect"]["max"]:
                    key = "Perfect"
                    #image = cv2.putText(image, "{}!".format(key), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3, cv2.LINE_AA)
                elif yml[i]["Standards"]["Good"]["min"] <= points[str(yml[i]["Angle_Name"])] < yml[i]["Standards"]["Good"]["max"]:
                    key = "Good"
                    #image = cv2.putText(image, "{}!".format(key), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3, cv2.LINE_AA)
                elif yml[i]["Standards"]["Add-oil"]["min"] <= points[str(yml[i]["Angle_Name"])] < yml[i]["Standards"]["Add-oil"]["max"]:
                    key = "Add-oil"
                    #image = cv2.putText(image, "{}!".format(key), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3, cv2.LINE_AA)                                
                else:
                     key = "Other"           
                overall.append(yml[i]["Standards"][key]["score"])
            except TypeError:
                print("Not enough points")

        print("----------------")
        print("Stage Scoring : {}".format(sum(stage_scoring)))
        print("Overall Scoring : {}".format(sum(overall)))
        print(points)
        print("----------------")

        if len(yml)*2 <= sum(overall) <= len(yml)*3:
            data = cv2.putText(data, "Perfect!", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 3, cv2.LINE_AA)
        elif len(yml) <= sum(overall) <= len(yml)*2:
            data = cv2.putText(data, "Good!", (20,1200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 3, cv2.LINE_AA) 
        elif sum(overall) <= len(yml):
            data = cv2.putText(data, "Keep going!", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 3, cv2.LINE_AA)

        if sum(stage_scoring) >= len(yml)*0.75:
            if stage_number == get_stages("{}\\exceises".format(base_path)):
                stage_number = 0
            else:
                stage_number += 1

        print("Stage:{}".format(stage_number))
        data = cv2.putText(data, "Stage:"+str(stage_number), (20,60), cv2.FONT_HERSHEY_SIMPLEX, 
                   2, (255,0,255), 3, cv2.LINE_AA)

        data = cv2.putText(data, "Overall Score:"+str(sum(overall)), (20,180), cv2.FONT_HERSHEY_SIMPLEX, 
                   2, (255,0,255), 3, cv2.LINE_AA)

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
    cv2.moveWindow('MediaPipe Pose',1000,200)
    cv2.imshow('Data Display',data)
    cv2.moveWindow('Data Display',350,200)

    key = cv2.waitKey(5)
    if key in [27,ord("q")]:
      break
cap.release()
