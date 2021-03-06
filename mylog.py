import logging
import sys
import os
import config

log = logging.getLogger("dnr")
log.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(levelname)s] %(message)s")

file_handler = logging.FileHandler(os.path.join(config.log_path, "debug.log"), "wt")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)