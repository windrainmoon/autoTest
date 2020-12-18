__author__ = 'Administrator'
from flask import Blueprint
import sys


sys.path.append("../..")

login = Blueprint('login', __name__)
login.config = {}

from app_src.login import views