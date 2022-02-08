import yaml
from yaml import CLoader as Loader

with open("./execises/test/stages.yaml", "r") as f:
    stages = list(yaml.load(f,Loader=Loader).values())
    for i in stages:print(i)