__author__ = 'Administrator'
from flask import Blueprint
import sys


sys.path.append("../..")

dataExtract = Blueprint('dataExtract', __name__)
dataExtract.config = {}

from app_src.dataExtract import views