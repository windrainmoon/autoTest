__author__ = 'Administrator'
from flask import Blueprint
import sys

sys.path.append("../..")

main = Blueprint('main', __name__)

from app.main import views