from tkinter.messagebox import NO
import yaml
from yaml import CLoader as Loader
import numpy
from scipy import spatial

class ScoringManager():
    def __init__(self,execise_path,judge_threshold=0.95):
        self.name = execise_path.split("/")[-1]
        self.execise_path = execise_path
        self.threshold = judge_threshold
        self.load_stage_landmarks()
    def score(self,stage_num,frames_to_score):
        self.current_stage = stage_num
        self.current_stage_landmarks = self.stage_landmarks[self.current_stage-1]
        self.similarities = []
        # print("current_stage_landmarks:",self.current_stage_landmarks)
        for frame in frames_to_score:
            for i in range(len(frame)):
                print("frame:",frame[i])
                if self.current_stage_landmarks[i] is None or frame[i] is None:
                    self.similarities.append(0.0)  # 0.0 means no landmarks
                    continue
                if len(self.current_stage_landmarks[i]) == 0 or len(frame[i]) == 0:
                    self.similarities.append(0.0)  # 0.0 means no landmarks
                    continue
                self.similarities.append(self.cosine_sim_cal(float(self.current_stage_landmarks[i][0]),float(self.current_stage_landmarks[i][1]),float(frame[i][0]),float(frame[i][1])))
        return sum(self.similarities)/len(self.similarities)
    def load_stage_landmarks(self):
        with open(self.execise_path+"/stages.yaml","r") as f:
            self.stage_landmarks = list(yaml.load(f,Loader=Loader).values())
        print("stage_landmarks_length:",len(self.stage_landmarks))
            
    def cosine_sim_cal(self,x1,y1,x2,y2):
        p1 = numpy.array([x1,y1])
        p2 = numpy.array([x2,y2])
        return 1-spatial.distance.cosine(p1,p2)

            
        