__author__ = 'Administrator'
from flask import render_template, flash, request, redirect, url_for, json, jsonify, session
from . import run
from app_src.common.common import *
from .runFunc import *
from conf import LINE_BREAK_LENGTH


@run.route('/index', methods=['GET', 'POST'])
@check_login
def index():
    csrf_token = session['csrf_token']
    res = getRunLogByToken(csrf_token)
    # caseId, suiteName, endTime, percent
    return render_template('run/index.html', runDatas=res)


@run.route('/schedule', methods=['GET', 'POST'])
@check_login
def schedule():
    # user_id = session['user_id'] or session['_user_id']
    suite_id = request.args.get('suite_id')
    res = getRunLogByUserSuite(suite_id)
    scheduleParams = getRunSchedule(suite_id)
    if scheduleParams and len(scheduleParams) > 0:
        return render_template('run/schedule.html', runDatas=res, isRun=scheduleParams[0], isSend=scheduleParams[1],
                               min=scheduleParams[2], hour=scheduleParams[3], day=scheduleParams[4], month=scheduleParams[5],
                               week=scheduleParams[6] )
    else:
        return render_template('run/schedule.html', runDatas=res, min=-1, hour=-1, day=-1, month=-1, week=-1, isRun=0, isSend=0)


@run.route('/synchronizeSchedule', methods=['GET', 'POST'])
@check_login
def synchronizeSchedule():
    suite_id = request.args.get('suite_id')
    data = request.form
    updateRunSchedule(suite_id, data)
    return jsonify({'resultCode': 200, 'result': ''})


@run.route('/getSchedule', methods=['GET', 'POST'])
@check_login
def getSchedule():
    suite_id = request.args.get('suite_id')
    res = getRunSchedule(suite_id)
    if not res or len(res) == 0:
        return jsonify({'resultCode': 0, 'result': "not get data!"})
    else:
        return jsonify({'resultCode': 200, 'result': res})


@run.route('/getRunLog', methods=['GET', 'POST'])
@check_login
def getRunLog():
    suite_id = request.args.get('suite_id')
    res = getRunLogByUserSuite(suite_id)
    return jsonify({'resultCode': 200, 'result': res})


@run.route('/runTestSuite', methods=['GET', 'POST'])
@check_login
def runTestSuite():
    try:
        task_id = crID(11)
        suite_id = request.args['suite_id']
        csrf_token = session['csrf_token']
        user_id = getUserId()
        setNewTask(csrf_token, suite_id, user_id, task_id)
        result = jsonify({'resultCode': 200, 'result': [task_id, getTestSuiteById(suite_id)[1]]})
    except Exception as e:
        result = jsonify({'resultCode': 0, 'result': e})
    return result


@run.route("/refreshProgress", methods=['GET', 'POST'])
@check_login
def refreshProgress():
    csrf_token = session['csrf_token']
    res = getRunLogByToken(csrf_token)
    if res:
        result = jsonify({'resultCode': 200, 'result': res})
    else:
        result = jsonify({'resultCode': 0, 'result': ""})
    return result


@run.route("/cleanLog", methods=['GET', 'POST'])
@check_login
def cleanLog():
    runCaseId = request.args.get('runCaseId')
    csrf_token = session['csrf_token']
    cleanRunLog(runCaseId, csrf_token)
    result = jsonify({'resultCode': 200, 'result': ""})
    return result


@run.route("/showResult", methods=['GET', 'POST'])
# @check_login
def showResult():
    runCaseId = request.args['runCaseId']
    sql = "select runResult from runTestCaseLog where runCaseId=:v1"
    res = db.execute(sql, [runCaseId]).fetchone()
    if res:
        data = json.loads(res[0])
        return render_template("run/testResult.html", items=data[0]['children'], LINE_BREAK_LENGTH=LINE_BREAK_LENGTH)
    else:
        return render_template("run/testResult.html")


@run.route("/report", methods=['GET', 'POST'])
# @check_login
def report():
    runCaseId = request.args['runCaseId']
    sql = "select runResult from testReports where runCaseId=:v1"
    res = db.execute(sql, [runCaseId]).fetchone()
    if res:
        return md2html(res[0])
    else:
        return "report not exists !"


@run.route("/test", methods=['GET', 'POST'])
# @check_login
def test():
    return render_template("marcos/Marcos.html", aa="123", bb=12)