#!/usr/bin/env python

import logging
import logging.handlers
import os

# Logging to file
dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=dir_path + "/test.log", format='%(asctime)s - %(message)s', level=logging.INFO, filemode='w')

# Logging messages to the console
console = logging.StreamHandler() 
logger = logging.getLogger()
logger.addHandler(console)

# Logging test
logging.info("** Testing **")