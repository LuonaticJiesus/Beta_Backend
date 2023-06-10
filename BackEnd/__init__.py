import os

import pymysql
import yaml

pymysql.install_as_MySQLdb()

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../config.yaml')
global_config = None
with open(config_path, 'r', encoding='utf-8') as f:
    global_config = yaml.load(f, Loader=yaml.FullLoader)
