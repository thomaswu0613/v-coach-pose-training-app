import os
import numpy
import yaml
class StageManager():
    def __init__(self,execise_file_dir,judge_threshold=0.7):
        self.execise_files_dir = execise_file_dir
        self.current_stage = 0
        self.threshold = judge_threshold
    def judge_stage(self,sample_array,user_array,max_none):
        none_count = 0
        similarities = []
        for i in range(17):
            if sample_array[i] is None or user_array is None:
                none_count+=1
                continue
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
    def file_helper(self,dir,fileformatending):
        target_files = []
        for file in os.listdir(dir,):
            if file.endswith(fileformatending):
                target_files.append(file)
        return target_files
