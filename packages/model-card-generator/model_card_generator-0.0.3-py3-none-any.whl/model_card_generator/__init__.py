#!/usr/bin/env python3

import os

env_dict = {
    # Model card envs
    'name': 'MODEL_NAME',
    'date': 'MODEL_DATE',
    'version': 'MODEL_VERSION'
    # ...
}

def get_env(name):
    # Verify if env exists
    return os.environ[env_dict[name]]

class ModelCard:
    """Machine Learning Model Card"""
    
    def __init__(self, name, date, version):
            self.name = name
            self.date = date 
            self.version = version

mc = ModelCard(
    get_env('name'), 
    get_env('date'), 
    get_env('version')
)

print("Model name is", mc.name)
print("Model date is", mc.date)
print("Model version is", mc.version)