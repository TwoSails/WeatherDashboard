import yaml


def get_config():
    DIR = "weatherapp/util/config.yml"
    configfile = open(DIR, 'r')
    config = yaml.safe_load(configfile.read())
    return config
