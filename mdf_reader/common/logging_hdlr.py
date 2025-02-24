#!/usr/bin/env python3
"""
Created on Wed Apr  3 08:45:03 2019

@author: iregon
"""

import logging


def init_logger(module, level="INFO", fn=None):
    from importlib import reload

    reload(logging)
    level = logging.getLevelName(level)
    logging_params = {
        "level": level,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    }
    if fn is not None:
        logging_params["filename"] = fn
    logging.basicConfig(**logging_params)
    logging.info("init basic configure of logging success")
    return logging.getLogger(module)
