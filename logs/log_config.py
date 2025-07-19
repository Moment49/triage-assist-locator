#!/usr/bin/env python3

# importing module
import logging
import os

full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'triage.log'))


# Create and configure logger
logging.basicConfig(filename=full_path,
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)