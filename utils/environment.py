from json import load 

environment = {"Key": "value"}

def loadEnvironment(fileName):
  with open(fileName) as f:
    global environment
    environment = load(f)

def getEnvironment(key):
  return environment.get(key, None)

