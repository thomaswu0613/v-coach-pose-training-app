import cv2
import mediapipe as mp
import numpy as np
import traceback
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture("/dev/video2")

# Curl counter variables
counter = 0 
stage = None

required = ["right_elbow"]
body_angle = {"right_shoulder":[24,12,14],"left_shoulder":[23,11,13],"right_knee":[28,26,24],"left_knee":[28,25,23],"left_elbow":[11,13,15],"right_elbow":[12,14,16]}

#Get angle function by name func
def get_angle_by_name(keypoints,body_part):
    print("hello")
    global body_angle
    point_nums = body_angle[str(body_part)]
    a = keypoints[point_nums[0]]
    b = keypoints[point_nums[1]]
    c = keypoints[point_nums[2]]
    print(point_nums)
    angle = round(calculate_angle(a,b,c))
    return angle
    
    
#Curl counter func
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
"""
def check_body_points(requited_body_angles,keypoints):
    global body_angle
    for body in requited_body_angles:
        i = body_angle[body]
        for j in i:
            if j < len(keypoints)+1:
                print("skipped")
                continue
"""

def fencing_judge(requited_body_points,key_points):
    pass

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get keypoints
            keypoints = []

            for data_point in results.pose_landmarks.landmark:
                keypoints.append([
                         data_point.x,data_point.y])\

            check_body_points(required,keypoints)
        

        except AttributeError:
            print("No body detected")    
        except:
            traceback.print_exc()
            pass
        angle = get_angle_by_name(keypoints,"right_elbow")
        # Setup status box
        cv2.rectangle(image, (0,0), (225,300), (245,117,16), -1)
        print(angle)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)
        cv2.moveWindow('Mediapipe Feed', 20,20);

        
        if cv2.waitKey(10) in [27,32]:
            break

    cap.release()
    cv2.destroyAllWindows()