__author__ = 'Daniel Myers'
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
from logging import StreamHandler

from flask import Flask
app = Flask(__name__)

import steamcheck.views

file_handler = StreamHandler()
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)