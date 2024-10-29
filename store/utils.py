import json
import os.path

from django.conf import settings


def load_json_data(file_name):
    file_path = os.path.join(settings.BASE_DIR, 'static', file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f'The file {file_path} does not exist.')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data