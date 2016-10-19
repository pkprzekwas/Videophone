import json
import os
from pathlib import Path

project_root = str(Path(__file__).resolve().parents[1])
config_path = os.path.join(project_root, 'config.json')

with open(config_path) as config_json:
    data = config_json.read()
    configuration = json.loads(data)

API_KEY = configuration['API_KEY']
PERSON_GROUP_ID = configuration['PERSON_GROUP_ID']


json_headers = {'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': API_KEY}


bin_headers = {'Content-Type': 'application/octet-stream',
               'Ocp-Apim-Subscription-Key': API_KEY}

face_ids = {'mark1': '2e9c2cd2-56fa-4d66-bdb8-2c262132a724'}