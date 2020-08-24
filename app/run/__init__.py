__author__ = 'Administrator'
from flask import Blueprint
import sys

sys.path.append("../..")

run = Blueprint('run', __name__)

from app.run import views