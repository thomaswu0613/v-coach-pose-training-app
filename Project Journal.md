# Project Journal



### Daily Logs:

###### 2022-1-30

- Implementation of Mediapipe keypoints (In-progress)

- Start working on Pose Scoring API (In-progress)



### Todos:

- [ ]  Research and work on L2 normalization with cord -> (x,y) (??)

- [ ]  <mark>Config file for each execise (???)</mark>
  
  ```py
  ap = argparse.ArgumentParser()
  ap.add_argument("-a", "--activity", required=True,
  	help="activity to be scored")
  ap.add_argument("-v", "--video", required=True,
  	help="video file to be scored against")
  ap.add_argument("-l", "--lookup", default="lookup_test.pickle",
  	help="The pickle file containing the lookup table")
  args = vars(ap.parse_args())
  ```

- [ ]  Process results with [Cosine Similarity  Formula](https://zh.wikipedia.org/wiki/%E4%BD%99%E5%BC%A6%E7%9B%B8%E4%BC%BC%E6%80%A7)

- [ ]  Work on human body bounding box

- [ ]  Finish Scoring API with following functions
  
  - L2 normalization
  
  - bounding box
  
  - comparison between standard and user's pose
  
  - keypoints implementation

- [ ]  Save execise standard with [Pickle]((https://docs.python.org/zh-cn/3/library/pickle.html)) or Yaml or Json (??)



### Roadmap:

Execise Scoring System

Comment and statics report System

Stage Counter with Mediapipe





