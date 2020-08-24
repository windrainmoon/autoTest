__author__ = 'Administrator'
from flask import render_template, flash, request, redirect, url_for, json, jsonify, session
from . import run
from app.common.common import *
from .runFunc import *


@run.route('/index', methods=['GET', 'POST'])
@check_login
def index():
    csrf_token = session['csrf_token']
    res = getRunLogByUser(csrf_token)
    # caseId, suiteName, endTime, percent
    return render_template('run/index.html', runDatas=res)


@run.route('/runTestSuite', methods=['GET', 'POST'])
@check_login
def runTestSuite():
    task_id = crID(11)
    suite_id = request.args['suite_id']
    csrf_token = session['csrf_token']
    user_id = session['user_id']
    all_item_count = getAllItemCount(suite_id)
    setNewTask(csrf_token, suite_id, user_id, all_item_count, 0, task_id, '')
    if 1:
        result = jsonify({'resultCode': 200, 'result': [task_id, getTestSuiteById(suite_id)[1]]})
    else:
        result = jsonify({'resultCode': 0, 'result': ""})
    return result


@run.route("/refreshProgress", methods=['GET', 'POST'])
@check_login
def refreshProgress():
    csrf_token = session['csrf_token']
    res = getRunLogByUser(csrf_token)
    if res:
        result = jsonify({'resultCode': 200, 'result': res})
    else:
        result = jsonify({'resultCode': 0, 'result': ""})
    return result


@run.route("/showResult", methods=['GET', 'POST'])
@check_login
def showResult():
    runCaseId = request.args['runCaseId']
    sql = "select runResult from runTestCaseLog where runCaseId=:v1"
    res = db.execute(sql, [runCaseId]).fetchone()
    if res:
        print(res[0])
        data = json.loads(res[0])
        return render_template("run/testResult.html", items=data[0]['children'])
    else:
        return render_template("run/testResult.html")