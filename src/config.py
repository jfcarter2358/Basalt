import json

config = {}

def read_config():
    with open('data/config.json') as f:
        config = json.load(f)