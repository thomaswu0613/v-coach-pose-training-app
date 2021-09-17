import yaml

with open(r"./exceises/test.yaml") as f:
    y = yaml.load(f,Loader=yaml.FullLoader)


for i in range(0,len(y)):
    print(y[i])
    print(y[i]["Stage"])