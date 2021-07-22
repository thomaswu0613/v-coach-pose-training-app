import cv2
import mediapipe as mp
import numpy as np
import traceback
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture("/dev/video2")


skip = False


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
"""
def get_body_angle_by_name(landmarks,angle_name):
    body_angle_points = {
                    "armpit_left":[mp_pose.PoseLandmark.LEFT_ELBOW.value,mp_pose.PoseLandmark.LEFT_SHOULDER.value,mp_pose.PoseLandmark.LEFT_WRIST.value],
                    "armpit_right":[mp_pose.PoseLandmark.RIGHT_ELBOW.value,mp_pose.PoseLandmark.RIGHT_SHOULDER.value,mp_pose.PoseLandmark.RIGHT_WRIST.value],
                    "elbow_left":[mp_pose.PoseLandmark.LEFT_SHOULDER.value,mp_pose.PoseLandmark.LEFT_ELBOW.value,mp_pose.PoseLandmark.LEFT_WRIST.value],
                    "elbow_right":[mp_pose.PoseLandmark.RIGHT_SHOULDER.value,mp_pose.PoseLandmark.RIGHT_ELBOW.value,mp_pose.PoseLandmark.RIGHT_WRIST.value],
                    "knee_left_inner":[mp_pose.PoseLandmark.LEFT_HIP.value,mp_pose.PoseLandmark.LFET_KNEE.value,mp_pose.PoseLandmark.LEFT_ANKLE.value],
                    "knee_right_inner":[mp_pose.PoseLandmark.RIGHT_HIP.value,mp_pose.PoseLandmark.RIGHT_KNEE.value,mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                    }
    if angle_name not in body_angle_points.keys():
        return None
    tmp = []
    tmp = body_angle_points[str(angle_name)]
    return calculate_angle([landmarks[tmp[0]].x,landmarks[tmp[0]].y],[landmarks[tmp[1]].x,landmarks[tmp[1]].y],[landmarks[tmp[2]].x,landmarks[tmp[2]].y])
"""
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        #frame = cv2.imread("./test/pose.jpg")
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)

        if results is None:
            continue
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark           
            # Get coordinates
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

            elbow_left = shoulder_left = calculate_angle(left_shoulder, left_elbow, left_wrist)
            armpit_left = calculate_angle(left_hip,left_shoulder,left_elbow)
            knee_left_inner = calculate_angle(left_hip,left_knee,left_ankle)
            knee_right_inner = calculate_angle(right_hip,right_knee,right_ankle)

            points = [elbow_left,armpit_left,knee_left_inner,knee_right_inner]

            if None in points:
                print("Not enough points to score")
                skip = True

            #print(left_shoulder,left_elbow,left_wrist)
            print(elbow_left,armpit_left,knee_left_inner,knee_right_inner)

            if not skip:
                if 140 < elbow_left < 155 and 40 < armpit_left < 55 and 170 < knee_left_inner < 185 and 90 < knee_right_inner < 105:
                    print("perfect!")
        except AttributeError:
            pass
        except:
            traceback.print_exc()
            pass
        
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        if skip and points.count(None)<4:
            cv2.putText(image, 'No body points', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        elif skip:
            cv2.putText(image, 'Not enough body points', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Feed', image)
        cv2.moveWindow("Feed",10,10)

        if cv2.waitKey(10) in [27,32]:
            break

    cap.release()
    cv2.destroyAllWindows()