# Project Journal

### Daily Logs:

###### 2022-2-9

- New version of scoring manager v2.0 (in-progress)
- Added webcam support (90% finish)

###### 2022-2-6

- Working on a bunch of things (Ahhhhhhhhh!)
  - StageManager
  - Scoring Library support

###### 2022-2-3

- Ported scoring lib to main program (In testing stage - still in progass)

- Stage counter with simularty from different frames in sample video <mark>(Not yet started !)</mark>

###### 2022-1-31

- Implementation of Mediapipe keypoints (Finished)

- Work on normalize function (In-progress)

###### 2022-1-30

- Implementation of Mediapipe keypoints (In-progress)

- Start working on Pose Scoring API (In-progress)

### Todos:

- [ ] Research and work on L2 normalization with cord -> (x,y) (??)

- [ ] <mark>UI !!!!!!</mark>

- [ ] <mark>Config file for each execise (???)</mark>
  
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

- [ ] Process results with [Cosine Similarity  Formula](https://zh.wikipedia.org/wiki/%E4%BD%99%E5%BC%A6%E7%9B%B8%E4%BC%BC%E6%80%A7)

- [ ] Work on human body bounding box

- [ ] Finish Scoring API with following functions
  
  - L2 normalization
  
  - bounding box
  
  - comparison between standard and user's pose
  
  - keypoints implementation

- [ ] Save execise standard with [Pickle]((https://docs.python.org/zh-cn/3/library/pickle.html)) or Yaml or Json (??)

- [ ] Opimize speed, live scoring : 

### Roadmap:

Execise Scoring System

Comment and statics report System

Stage Counter with Mediapipe

Person Profile System and Personizle

### Notes:

- Unit Ventor
