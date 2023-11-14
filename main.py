import openai

import requests
import urllib.parse
from datetime import datetime

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import numpy as np
import json

import yaml

with open('API_config.yaml', 'r') as config_file:
    config_data = yaml.safe_load(config_file)

# Access the API keys as needed
openai.api_key = config_data['openai']['api_key']
GOOGLE_API_KEY = config_data['google']['api_key']

print(GOOGLE_API_KEY)