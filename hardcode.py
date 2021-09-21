import cv2
import yaml
import mediapipe as mp
import traceback
import numpy as np
import os
mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
camera_index = 0
same = False
overall = []
skip = False
s = 0
exceise_name = "test_exceise"



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

stage = 0
#loop = int(input("How many cycles ? :"))

cap = cv2.VideoCapture(camera_index)

#load exceise standard yaml


print("there are {} stages".format(get_stages("./exceises/{}".format(exceise_name))))

with mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    skip = False
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


    # judge process

    try:
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
        image.flags.writeable = True
        
        #armpit_left = calculate_angle(left_hip,left_shoulder,left_elbow)
        #knee_left_inner = calculate_angle(left_hip,left_knee,left_ankle)
        #knee_right_inner = calculate_angle(right_hip,right_knee,right_ankle)
        print("angles:",elbow_right,elbow_left)
        #if skip is True:
        #    cv2.imshow('MediaPipe Pose', image)
        
        image = cv2.putText(image, "Left elbow:"+str(round(elbow_right,2)), (30,20), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 1, cv2.LINE_AA)
        image = cv2.putText(image, "Right elbow:"+str(round(elbow_left,2)), (30,50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 1, cv2.LINE_AA)
        image = cv2.putText(image, "Right knee:"+str(round(knee_left,2)), (30,80), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 1, cv2.LINE_AA)
        image = cv2.putText(image, "Left knee:"+str(round(knee_right,2)), (30,100), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 1, cv2.LINE_AA)
        print("stage",stage)
        #judge

        #f = open(r"./exceises/{}/stage{}.yaml".format(exceise_name,stage),"r")
        #y = yaml.load(f,Loader=yaml.FullLoader)

        overall = []

        if (s == 0):
            print("XX",elbow_left)
            if 140<elbow_left<180 and 140<elbow_right<180 and 160<knee_left<180 and 160<knee_right<180:
                image = cv2.putText(image, "Perfect!", (30,110), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255,255,255), 2, cv2.LINE_AA)
            print("Hello")
            stage = 1
        else:
            if 160<elbow_left<180 and 160<elbow_right<180 and 60<knee_left<90 and 60<knee_right<90 and 60<hip_left<90:
                image = cv2.putText(image, "Perfect!", (30,110), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255,255,255), 2, cv2.LINE_AA)
            if 150<elbow_left<160 and 150<elbow_right<160 and 40<knee_left<60 and 40<knee_right<60 and 20<hip_left<40:
                image = cv2.putText(image, "Good!", (30,110), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255,255,255), 2, cv2.LINE_AA)
            if 120<elbow_left<150 and 120<elbow_right<150 and 20<knee_left<40 and 20<knee_right<40 and 20<hip_left<40:
                image = cv2.putText(image, "Add Oil!", (30,110), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255,255,255), 2, cv2.LINE_AA)
            stage = 0
                
    except :
        traceback.print_exc()
        image = cv2.putText(image, "No body detected.", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,255), 2, cv2.LINE_AA)
    print(overall)  
    print("Stages:{}",stage) 
    """
    if sum(overall)==len(y) :
        image = cv2.putText(image, "Perfect".format(str(stage)), (30,170), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    if sum(overall)>len(y)*2:
        image = cv2.putText(image, "Perfect".format(str(stage)), (30,170), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)    
    """
    image = cv2.putText(image, "Stage {}".format(str(stage)), (30,170), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    image = cv2.putText(image, "Overall Score:"+str(sum(overall)), (30,110), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255), 2, cv2.LINE_AA)
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

    #mp_drawing.draw_landmarks(
    #    image,
    #    results.pose_landmarks,
    #    mp_pose.POSE_CONNECTIONS,
    #    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imshow('MediaPipe Pose', image)
    key = cv2.waitKey(5)
    if key in [27]:
      break
cap.release()