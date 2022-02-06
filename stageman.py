import os
import numpy
import yaml
from yaml import CLoader as Loader
class StageManager():
    def __init__(self,execise_file_dir,judge_threshold=0.7):
        self.execise_files_dir = execise_file_dir
        self.current_stage = 0
        self.threshold = judge_threshold
    def judge_stage(self,user_array,current_stage,max_none_time):
        none_count = 0
        similarities = []
        sample_array = self.stage_landmarks[int(current_stage)]
        for i in range(17):
            if sample_array[i] is None or user_array is None:
                none_count+=1
                continue
            if none_count == max_none_time:
                return None
            similarities.append(self.stage_cal(sample_array[0],sample_array[1],user_array[0],user_array[1]))
        for i in similarities:
            if similarities[i] is None:
                similarities[i] = 0
        result = sum(similarities)/len(similarities)
        if result > self.threshold:
            return (self.current_stage += 1)
        else:
            return self.current_stage
    def stage_cal(self,x1,y1,x2,y2):
        p1 = numpy.array([x1,y1])
        p2 = numpy.array([x2,y2])
        p1l = numpy.linalg.norm(p1)
        p2l = numpy.linalg.norm(p2)
        return numpy.dot(p1,p2)/numpy.dot(p2l,p2l)
    def rep_count(self):
        config = yaml.load(self.execise_files_dir+"/config.yaml")
        max_stages = config["max_stages"]
        if self.current_stage == max_stages:
            self.rep_count+=1
        return self.rep_count
    def file_helper(self,dir,fileformatending):
        target_files = []
        for file in os.listdir(dir,):
            if file.endswith(fileformatending):
                target_files.append(file)
        return target_files
    def read_stages(self):
        with open(self.execise_files_dir+"/stages.yaml","r") as f:
            self.stage_landmarks = yaml.load(f,Loader=Loader).keys()
