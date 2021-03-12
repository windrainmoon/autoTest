__author__ = 'Administrator'
from flask import Blueprint
import sys

sys.path.append("../..")

runConfig = Blueprint('runConfig', __name__)

from app_src.runConfig import views