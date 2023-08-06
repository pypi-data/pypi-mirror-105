from preprocess.config.config import Regressor

config = Regressor()

VERSION_PATH = config.PACKAGE_ROOT / 'VERSION'


with open(VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()