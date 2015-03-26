__author__ = 'Daniel Myers'
import logging

logging.getLogger("requests").setLevel(logging.WARNING)

from flask import Flask
app = Flask(__name__)

import steamcheck.views