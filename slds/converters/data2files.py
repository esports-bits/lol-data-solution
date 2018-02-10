import json


def write_json(data, save_dir, file_name):
    with open('{dir}/{name}.json'.format(dir=save_dir, name=file_name), 'w') as fp:
        json.dump(data, fp)


def read_json(save_dir, file_name):
    with open('{dir}/{name}.json'.format(dir=save_dir, name=file_name), 'r') as fp:
        return json.load(fp)
