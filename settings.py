import pathlib
import yaml
import logging


BASE_DIR = pathlib.Path(__file__).parent
config_path = BASE_DIR / 'config' / 'chat.yaml'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config

config = get_config(config_path)

log = logging.getLogger('app')
log.setLevel(logging.DEBUG)

SECRET_KEY = 'SECRET_KEY'

f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)
