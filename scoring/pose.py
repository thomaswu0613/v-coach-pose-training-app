
class Body():
    def __init__(self,results,mp_pose):
        if not results:
            print("No results")
            return
        self.results = results
        self.lm = self.results.pose_landmarks.landmark
        self.mp_pose = mp_pose
        print("hello")
    def nose(self):
        print("nose")
        return [self.lm[self.mp_pose.PoseLandmark.NOSE.value].x, self.lm[self.mp_pose.PoseLandmark.NOSE.value].y]


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
