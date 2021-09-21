import yaml
import os

with open(r"./exceises/test_exceise/stage1.yaml") as f:
    y = yaml.load(f,Loader=yaml.FullLoader)
"""
elbow_left = 0
elbow_right = 0
knee_left = 0
points = {"elbow_left":elbow_left,"elbow_right":elbow_right,"knee_left":knee_left}



for i in range(0,len(y)):
    print(y[i])
    print(y[i]["Angle_Name"])
"""

for i in range(0,len(y)-1):
    print(y[i])
