import os
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
# Load configuration from config.yaml
_config_path = os.path.join(ROOT_DIR, 'config.yml')
with open(_config_path, 'r', encoding='utf-8') as f:
    config = yaml.load(f)

CONSTANTS_PATH = os.path.join(ROOT_DIR, config['path']['constants'])
with open(CONSTANTS_PATH, 'r', encoding='utf-8') as f:
    constants = yaml.load(f)

LOG_LEVEL = config['log_level']


BSDK = '官服'
QSDK = '渠道服'

CHANNEL_OPTION = [BSDK, QSDK]

DEBUG_LOG = False
ERROR_LOG = True

CACHE_DIR = os.path.join(ROOT_DIR, config['path']['cache'])
RESULT_DIR = os.path.join(ROOT_DIR, config['path']['result'])
DATA_DIR = os.path.join(ROOT_DIR, config['path']['data'])
CONFIG_PATH = os.path.join(CACHE_DIR, config['path']['config'])
OLD_CONFIG_PATH = os.path.join(ROOT_DIR, config['path']['old_config'])
AUTH_KEY = config['auth_key']

DEFAULT_HEADERS = dict(constants['headers']['android'])
IOS_HEADERS = dict(constants['headers']['ios'])

def update_app_ver(version: str = None):
    default_ver = '7.7.2'
    if version is not None:
        with open(CONSTANTS_PATH, 'rw', encoding='utf-8') as f:
            data = yaml.load(f)
            data['headers']['default']['APP-VER'] = version
            yaml.dump(data, f)
            # VERSION = version
    else:
        # try:
        #     with open(os.path.join(CACHE_DIR, 'version.txt'), 'r', encoding='utf-8') as f:
        #         VERSION = f.read()
        # except FileNotFoundError:
        #     update_app_ver(default_ver)
            return

#     DEFAULT_HEADERS['APP-VER'] = VERSION
#     IOS_HEADERS['APP-VER'] = VERSION
#
#
#
# update_app_ver()
