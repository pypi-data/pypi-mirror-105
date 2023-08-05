from os.path import dirname, abspath
import sys
from importlib import import_module

CURRENT_DIR = dirname(abspath(__file__)) + '/'
sys.path.append(CURRENT_DIR)
PKG = 'hestia_earth.models.site'


def run(model: str, data):
    run = getattr(import_module(f".{model}", package=PKG), 'run')
    return run(data)
