__author__ = 'Administrator'
from . import main
from flask import render_template, flash, request, redirect, url_for, json, jsonify, session
from app.common.common import *
from .functions import *


@main.route('/index', methods=['GET', 'POST'])
@check_login
def index():
    user_name = session['user_name']
    user_head = session['user_head']
    return render_template('main/cssmoban.html', user_name=user_name, user_head=user_head)


@main.route('/indexTestCase', methods=['GET', 'POST'])
@check_login
def indexTestCase():
    user_id = session['user_id']
    return render_template('main/index.html', user_id=user_id)


@main.route('/queryUserParam', methods=['GET', 'POST'])
@check_login
def queryUserParam():
    param_type = request.args.get("type", None)
    if param_type == 'root':
        user_id = session['user_id']
        print(user_id, 'get params!')
        lines = makeTableHtml(user_id)
        result = jsonify({'resultCode': 200, 'result': lines})
    else:
        result = jsonify({'resultCode': 0, 'result': ""})
    return result


@main.route('/queryStepParam', methods=['GET', 'POST'])
@check_login
def queryStepParam():
    stepType = request.args.get("stepType")
    user_id = session['user_id']
    res = getStepParamByUser(user_id, stepType)
    if res:
        result = jsonify({'resultCode': 200, 'result': res})
    else:
        result = jsonify({'resultCode': 0, 'result': ""})
    return result


@main.route('/delete', methods=['GET', 'POST'])
@check_login
def dropTestItem():
    item_id = request.args.get("item_id")
    item_type = request.args.get("item_type")
    if item_type == "testCase":
        dropTestCaseById(item_id)
    elif item_type == "testSuite":
        dropTestSuiteById(item_id)
    elif item_type[:8] == "testStep":
        dropTestStepById(item_id)
    else:
        return jsonify({'resultCode': 0, 'result': "item type not prepared!"})
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/synchronizeParam', methods=['GET', 'POST'])
@check_login
def synchronizeParam():
    user_id = session['user_id']
    data = request.get_data()
    res = saveUserParam(user_id, data)
    if not data or res:
        return jsonify({'resultCode': 0, 'result': res or 'failed'})
    else:
        return jsonify({'resultCode': 200, 'result': ""})




@main.route('/synchronizeTestSuite', methods=['GET', 'POST'])
@check_login
def synchronizeTestSuite():
    data = json.loads(request.get_data())
    # print(data)
    saveUserTree(data, session['user_id'])
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/copyNode', methods=['GET', 'POST'])
@check_login
def viewCopyNode():
    data = json.loads(request.get_data())
    copyNode(data, session['user_id'])
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/moveNode', methods=['GET', 'POST'])
@check_login
def viewMoveNode():
    data = json.loads(request.get_data())
    moveNode(data, session['user_id'])
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/addNode', methods=['GET', 'POST'])
@check_login
def viewAddNode():
    data = json.loads(request.get_data())
    addNode(data, session['user_id'])
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/root.json', methods=['GET', 'POST'])
@check_login
def getTreeData():
    user_id = session['user_id']
    id = request.args.get("id")
    type = request.args.get("type")
    tree_data = []
    if id == "":
        tree_data.append({'id': 'root', 'type': 'root', 'text': 'autoTestCase', 'children': True})
    elif id == 'root':
        all_suites = getAllSuite(user_id)
        for suite in all_suites:
            suite_id = suite[0]
            suite_name = suite[1]
            tree_data.append({"text": suite_name, "id": suite_id, "type": "testSuite", "children": True})
    elif type == "testSuite":
        for case in getTestCaseBySuite(id):
            case_id = case[0]
            case_name = case[2]
            tree_data.append({"text": case_name, "id": case_id, "type": "testCase", "children": True})
    elif type == "testCase":
        for step in getTestStepByCase(id):
            step_id = step[0]
            step_type = step[1]
            step_param1 = step[2]
            step_param2 = step[3]
            step_param3 = step[4]
            step_param4 = step[5]
            step_param5 = step[6]
            step_name = step[8]
            tree_data.append(
                {"text": step_name, "id": step_id, "children": False, "type": step_type,
                 "step_param1": step_param1, "step_param2": step_param2, "step_param3": step_param3,
                 "step_param4": step_param4, "step_param5": step_param5, })
    else:
        tree_data.append({'id': 'a1', 'type': 'other', 'text': '1', 'children': False})
    return jsonify({'resultCode': 200, 'result': tree_data})

