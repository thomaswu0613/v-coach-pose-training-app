import os
import cv2
import sys
sys.path.insert(1, './scoring_lib')
from calculations import get_Score
class ScoringManager():
    def __init__(self,execise_name):
        self.video_name = ""
        self.current_rep = 0
        self.video_path = "./tmp"
        self.action = execise_name
        self.video_list = []
        self.counted = False
    def save_video(self,rep_number,frame):
        print(rep_number,self.current_rep,rep_number == self.current_rep,rep_number == 0,self.counted)
        if ((rep_number >= self.current_rep) or (rep_number == 0)) and self.counted == False:
            self.counted = False
        if self.counted is False:
            print("-------new video!------------")
            self.current_rep += 1
            self.counted = True
            self.video_name = "{}/rep{}.mp4".format(self.video_path, rep_number)
            self.fourcc = cv2.VideoWriter_fourcc('F','M','P','4')
            self.video_writer = cv2.VideoWriter(self.video_name, self.fourcc, 15.0,(640,480),True)
            self.video_writer.release()
            self.counted = True
        self.video_writer.write(frame)
    def file_helper(self,dir,fileformatending):
        target_files = []
        for file in os.listdir(dir,):
            if file.endswith(fileformatending):
                target_files.append(file)
    def scoring_final(self):
        to_be_scored = self.file_helper(self.video_path,".mp4")
        for file in to_be_scored:
            final_score,score_list = calculate_Score(file,self.action)