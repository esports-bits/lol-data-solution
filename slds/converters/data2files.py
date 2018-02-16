import json


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
