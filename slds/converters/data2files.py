import json
from config.constants import STATIC_DATA_DIR, DD_LANGUAGE, DD_RUNES_REFORGED, DATA_DRAGON_URL
import requests


def write_json(data, save_dir, file_name):
    if '.json' in file_name:
        with open('{dir}/{name}'.format(dir=save_dir, name=file_name), 'w') as fp:
            json.dump(data, fp)
    else:
        with open('{dir}/{name}.json'.format(dir=save_dir, name=file_name), 'w') as fp:
            json.dump(data, fp)


def read_json(save_dir, file_name):
    if '.json' in file_name:
        with open('{dir}/{name}'.format(dir=save_dir, name=file_name), 'r') as fp:
            return json.load(fp)
    else:
        with open('{dir}/{name}.json'.format(dir=save_dir, name=file_name), 'r') as fp:
            return json.load(fp)


def get_runes_reforged_json(versions):
    version = versions['versions'][0]
    url = DATA_DRAGON_URL.format(version=version, language=DD_LANGUAGE, endpoint=DD_RUNES_REFORGED)
    r = requests.get(url)
    return r.json()


def save_runes_reforged_json():
    write_json(get_runes_reforged_json(), save_dir=STATIC_DATA_DIR, file_name='runes_reforged')
