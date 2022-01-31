
from re import A


class Body():
    def __init__(self,results,mp_pose):
        if not results:
            return
        self.results = results
        self.lm = self.results.pose_landmarks.landmark
        self.mp_pose = mp_pose
    def nose(self):
        a = [self.lm[self.mp_pose.PoseLandmark.NOSE.value].x, self.lm[self.mp_pose.PoseLandmark.NOSE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_eye_inner(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_INNER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_INNER.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_eye(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_EYE.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EYE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_eye_outer(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_OUTER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_OUTER.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_eye_inner(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE_INNER.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE_INNER.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_eye(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_eye_outer(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE_INNER.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value].y]
        if all(i <= 1 for i in a): return a
        else: return
    def left_eye_inner(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_INNER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_INNER.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_ear(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_EAR.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EAR.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_ear(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_EAR.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_EAR.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_mouth(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.MOUTH_LEFT.value].x, self.lm[self.mp_pose.PoseLandmark.MOUTH_LEFT.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_mouth(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_LEFT.value].x, self.lm[self.mp_pose.PoseLandmark.MOUTH_RIGHT.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_shoulder(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        if all(i <= 1 for i in a): return a
        else: return
    def right_shoulder(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        if all(i <= 1 for i in a): return a
        else: return
    def left_elbow(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_elbow(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_wrist(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_wrist(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_pinky(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_PICKY.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_PICKY.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_pinky(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_PICKY.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_PICKY.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_index(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_INDEX.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_INDEX.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_thumb(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_THUMB.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_THUMB.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_thumb(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_THUMB.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_THUMB.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_hip(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_HIP.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_hip(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_knee(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_knee(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_heel(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_HEEL.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def rigth_heel(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_HEEL.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_foot_index(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_foot_index(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    



class Pose(object):
    def getpoints(results):

        '''
        keypoints = []
        for data_point in results.pose_landmarks.landmark:
            keypoints.append({
                         'X': data_point.x,
                         'Y': data_point.y,
                         'Z': data_point.z,
                         'Visibility': data_point.visibility,
                         })
        print(keypoints)
        '''

        keypoints = []
        for data_point in results.pose_landmarks.landmark:
            keypoints.append([
                         data_point.x,
                         data_point.y,
                         # 'Z': data_point.z,
                         # 'Visibility': data_point.visibility,
            ])
        return keypoints
