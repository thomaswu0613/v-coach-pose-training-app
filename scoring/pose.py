

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
