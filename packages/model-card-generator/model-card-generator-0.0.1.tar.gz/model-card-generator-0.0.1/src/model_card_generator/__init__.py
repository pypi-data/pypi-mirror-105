#!/usr/bin/env python3

import os
from model_card import ModelCard

env_dict = {
    # Model card envs
    'name': 'MODEL_NAME',
    'date': 'MODEL_DATE',
    'version': 'MODEL_VERSION'
    # ...
}

def get_env(name):
    return os.environ[env_dict[name]]

mc = ModelCard(
    get_env('name'), 
    get_env('date'), 
    get_env('version')
)

print("Model name is", mc.name)
print("Model date is", mc.date)
print("Model version is", mc.version)