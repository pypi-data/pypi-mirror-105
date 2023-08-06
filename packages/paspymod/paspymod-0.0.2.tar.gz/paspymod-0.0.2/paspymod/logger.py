import logging
from utility import f_check as f

logging.basicConfig(level = f().loaded['debug_level'], datefmt='%Y-%m-%d %H:%M:%S', \
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s')
