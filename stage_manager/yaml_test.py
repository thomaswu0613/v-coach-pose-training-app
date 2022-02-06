import yaml
from yaml import CLoader as Loader

with open("./test.yaml","r") as f:
    print(yaml.load(f,Loader=Loader))