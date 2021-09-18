import cv2
import yaml
import mediapipe as mp
import traceback
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
camera_index = 2
same = False
y = 1


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
    return len([name for name in os.listdir('.') if os.path.isfile(name)])

stage = 1
#loop = int(input("How many cycles ? :"))

cap = cv2.VideoCapture(camera_index)

#load exceise standard yaml


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
        knee_left = calculate_angle(right_hip, right_knee, right_ankle)
        points = {"elbow_left":elbow_left,"elbow_right":elbow_right,"knee_left":knee_left}
        #armpit_left = calculate_angle(left_hip,left_shoulder,left_elbow)
        #knee_left_inner = calculate_angle(left_hip,left_knee,left_ankle)
        #knee_right_inner = calculate_angle(right_hip,right_knee,right_ankle)
        print("angles:",elbow_right,elbow_left)
        image.flags.writeable = True
        image = cv2.putText(image, "Left elbow:"+str(elbow_left), (30,20), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "Right elbow:"+str(elbow_right), (30,50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 2, cv2.LINE_AA)
        image = cv2.putText(image, "Right knee:"+str(knee_left), (30,80), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 2, cv2.LINE_AA)
        print(y)
        #judge

        f = open(r"./exceises/test_exceise/stage{}.yaml".format(stage),"r")
        y = yaml.load(f,Loader=yaml.FullLoader)

        for i in range(0,len(y)):
            print("hi!")
            
            print(y[i]["Standards"])
            if y[i]["Standards"]["Perfect"]["min"] < points[str(y[i]["Angle_Name"])] < y[i]["Standards"]["Perfect"]["max"]:
                print("---------------")
                print("Perfect!")
                image = cv2.putText(image, "Perfect!", (30,110), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 2, cv2.LINE_AA)
            if y[i]["Standards"]["Good"]["min"] < points[str(y[i]["Angle_Name"])] < y[i]["Standards"]["Good"]["max"]:
                print("---------------")
                print("Good!")
                image = cv2.putText(image, "Good!", (30,110), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 2, cv2.LINE_AA)
                print("---------------")
            if y[i]["Standards"]["Add-oil"]["min"] < points[str(y[i]["Angle_Name"])] < y[i]["Standards"]["Add-oil"]["max"]:
                print("---------------")
                print("Add oil!")
                image = cv2.putText(image, "Add oil!", (30,110), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 2, cv2.LINE_AA)
                print("---------------")
    except AttributeError:
        pass
    
    
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
    if cv2.waitKey(5) in [27]:
      break
cap.release()