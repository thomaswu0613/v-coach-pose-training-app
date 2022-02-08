import os
import numpy
import yaml
from yaml import CLoader as Loader
from scipy import spatial
class StageManager():
    def __init__(self,execise_file_dir,judge_threshold=0.95):
        self.execise_files_dir = execise_file_dir
        self.current_stage = 0
        self.rep_counter = 0
        self.threshold = judge_threshold
        self.counted = False
        self.read_stages()
        self.read_config()
    def judge_stage(self,user_array):
        self.rep_count()
        current_stage = self.current_stage
        if current_stage == self.config["max_stages"]:
            self.current_stage = 0
            return self.current_stage, self.rep_counter
        similarities = []
        stage_sample_array = self.stage_landmarks[int(current_stage)]
        for i in range(17):
            # print(stage_sample_array[i])
            if len(stage_sample_array[i]) == 0 or len(user_array[i]) == 0:
                similarities.append(0.0)
                continue
            # print(type(sample_array[0]))
            # print(type(user_array[0]))
            # print(stage_sample_array[0])
            # print("result:",self.stage_cal(sample_array[0],sample_array[1],user_array[0],user_array[1]))
            # print(user_array[0])
            similarities.append(self.stage_cal(float(stage_sample_array[i][0]),float(stage_sample_array[i][1]),float(user_array[i][0]),float(user_array[i][1])))
        # print("sim_list:",similarities)
        result = sum(similarities)/len(similarities)
        print("result:",result)
        for i in range(len(similarities)):
            if similarities[i] > 1:
                similarities[i] = 1
        if result > self.threshold:
            self.current_stage += 1
            self.counted = False
        # print(type(self.current_stage),type(self.rep_counter))
        return self.current_stage, self.rep_counter
    def stage_cal(self,x1,y1,x2,y2):
        p1 = numpy.array([x1,y1])
        p2 = numpy.array([x2,y2])
        p1l = numpy.linalg.norm(p1)
        p2l = numpy.linalg.norm(p2)
        # return (numpy.dot(p1,p2)/p2l*p2l)
        return 1-spatial.distance.cosine(p1,p2)
    def rep_count(self):
        max_stages = self.config["max_stages"]
        if self.current_stage == max_stages and self.counted is False:
            self.rep_counter+=1
            self.counted = True
    def read_stages(self):
        with open(self.execise_files_dir+"/stages.yaml","r") as f:
            self.stage_landmarks = list(yaml.load(f,Loader=Loader).values())
    def read_config(self):
        with open(self.execise_files_dir+"/config.yaml","r") as f:
            self.config = yaml.load(f,Loader=Loader)
