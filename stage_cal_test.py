from stageman import StageManager
import tools

sm = StageManager("./execises/test")
# n1 = [float(i) for i in input().split(",")]
# n2 = [float(i) for i in input().split(",")]
# print(sm.stage_cal(n1[0],n1[1],n2[0],n2[1]))
# pprint.pprint(sm.stage_landmarks[0])
print(sm.stage_landmarks[0])
print("----------------")
print(sm.stage_landmarks[0][0],sm.stage_landmarks[0][1])
print(sm.stage_cal(sm.stage_landmarks[0][0],sm.stage_landmarks[0][1],sm.stage_landmarks[0][0],sm.stage_landmarks[0][1]))
print("----------------")

