import yaml
from ruamel.yaml import YAML as objYAML

from .items import change_item

DIR = "weatherapp/util/config.yml"


def get_config():
    global DIR
    configfile = open('weatherapp/util/config.yml', 'r')
    config = yaml.safe_load(configfile.read())
    return config


def save_config(config_dict: dict):
    global DIR
    deleteme = []
    for key in config_dict.keys():
        if config_dict[key] is '' or config_dict[key] is False:
            deleteme.append(key)
    for a in deleteme:
        del config_dict[a]

    config = get_config()
    yaml = objYAML()
    file = open(DIR, 'w')
    for x in config_dict.keys():
        path = x.split('/')
        config = change_item(config, path, config_dict[x])

    yaml.dump(config, file)
    file.close()


def reset_config():
    pass
