__author__ = 'Administrator'
from . import main
from flask import render_template, flash, request, redirect, url_for, json, jsonify, session
from app_src.common.common import *
from .functions import *
from .roleFunc import *
from conf import __version__ as version

@main.route('/index', methods=['GET', 'POST'])
@check_login
def index():
    user_name = session['user_name']
    user_head = session['user_head']
    user_id = getUserId()
    user_role = getUserRole(user_id)
    print("session:", session)
    print("user_role:", user_role)
    return render_template('main/cssmoban.html', user_name=user_name, user_head=user_head,
                           user_role=user_role, version=version)


@main.route('/indexTestCase', methods=['GET', 'POST'])
@check_login
def indexTestCase():
    user_id = getUserId()
    user_role = getUserRole(user_id)
    return render_template('main/index.html', user_id=user_id, user_role=user_role)


@main.route('/updateLog', methods=['GET', 'POST'])
@check_login
def updateLog():
    return render_template('main/updateLog.html')


@main.route('/how2use', methods=['GET', 'POST'])
@check_login
def how2use():
    return render_template('main/how2use.html')


@main.route('/queryUserParam', methods=['GET', 'POST'])
@check_login
def queryUserParam():
    param_tree_id = request.args.get("param_tree_id", None)
    # print('queryUserParam', param_tree_id)
    if param_tree_id:
        user_id = getUserId()
        lines = makeParamTableHtml(user_id, param_tree_id)
        result = jsonify({'resultCode': 200, 'result': lines})
    else:
        result = jsonify({'resultCode': 0, 'result': ""})
    return result


@main.route('/queryGUIParam', methods=['GET', 'POST'])
@check_login
def queryGUIParam():
    param_tree_id = request.args.get("param_tree_id", None)
    # print('queryGUIParam:', param_tree_id)
    if param_tree_id:
        lines = makeGUItable(param_tree_id)
        result = jsonify({'resultCode': 200, 'result': lines})
    else:
        result = jsonify({'resultCode': 0, 'result': "get GUI data failed!"})
    return result


@main.route('/queryUserRole', methods=['GET', 'POST'])
@check_login
def queryUserRole():
    authority_type = request.args['authority_type']
    user_id = getUserId()
    if authority_type and user_id:
        user_authority = getUserRole(user_id)
        if authority_type in user_authority:
            result = jsonify({'resultCode': 200, 'result': 1})
        else:
            result = jsonify({'resultCode': 200, 'result': 0})
    else:
        result = jsonify({'resultCode': 0, 'result': 0})
    return result


@main.route('/queryStepParam', methods=['GET', 'POST'])
@check_login
def queryStepParam():
    stepType = request.args.get("stepType")
    param_tree_id = request.args.get("param_tree_id")
    user_id = getUserId()
    res = getStepParamByUser(user_id, param_tree_id, stepType)
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
    try:
        if item_type == "testCase":
            dropTestCaseById(item_id)
        elif item_type == "testSuite":
            dropTestSuiteById(item_id)
        elif item_type[:8] == "testStep" or item_type == 'function':
            dropTestStepById(item_id)
        elif item_type[:8] == "testHome":
            dropTestHomeById(item_id)
        else:
            return jsonify({'resultCode': 0, 'result': "item type not prepared!"})
    except Exception as e:
        print('delete item error, ', e)
        return jsonify({'resultCode': 0, 'result': "delete failed!"})
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/synGUIParam', methods=['GET', 'POST'])
@check_login
def synGUIParam():
    param_tree_id = request.args.get("param_tree_id")
    data = request.get_data()
    # print(param_tree_id, data)
    res = saveGUIParam(param_tree_id, data)
    if not data or res:
        return jsonify({'resultCode': 0, 'result': res or 'failed'})
    else:
        return jsonify({'resultCode': 200, 'result': ""})


@main.route('/synchronizeParam', methods=['GET', 'POST'])
@check_login
def synchronizeParam():
    user_id = getUserId()
    param_tree_id = request.args.get("param_tree_id")
    data = request.get_data()
    if param_tree_id == "function":
        res = saveUserFuncParam(user_id, data)
    else:
        res = saveUserParam(user_id, param_tree_id, data)
    if res:  # data为空表示清除所有参数;res不为0表示有错误
        return jsonify({'resultCode': 0, 'result': res or 'failed'})
    else:
        return jsonify({'resultCode': 200, 'result': ""})


@main.route('/synchronizeTestSuite', methods=['GET', 'POST'])
@check_login
def synchronizeTestSuite():
    data = json.loads(request.get_data())
    user_id = getUserId()
    saveUserTree(data, user_id)
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/copyNode', methods=['GET', 'POST'])
@check_login
def viewCopyNode():
    data = json.loads(request.get_data())
    # print('copy node,', data)
    user_id = getUserId()
    copyNode(data, user_id)
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/moveNode', methods=['GET', 'POST'])
@check_login
def viewMoveNode():
    data = json.loads(request.get_data())
    user_id = getUserId()
    moveNode(data, user_id)
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/addNode', methods=['GET', 'POST'])
@check_login
def viewAddNode():
    data = json.loads(request.get_data())
    user_id = getUserId()
    addNode(data, user_id)
    return jsonify({'resultCode': 200, 'result': ""})


@main.route('/root.json', methods=['GET', 'POST'])
@check_login
def getTreeData():
    user_id = getUserId()
    user_role = getUserRole(user_id)
    id = request.args.get("id")
    type = request.args.get("type")
    tree_data = []
    if id == "":
        if 'allUserSuites' not in user_role:
            tree_data.append({'id': 'root', 'type': 'root', 'text': 'autoTestCase', 'children': True})
        else:
            all_user = getAllUser()
            for subUser in all_user:
                tree_data.append({'id': 'root' + subUser[0], 'type': 'root', 'text': subUser[0], 'children': True})
    elif id[:4] == 'root':
        if id != 'root':
            user_id = id[4:]
        all_home = getAllHome(user_id)
        for home in all_home:
            home_id = home[0]
            home_name = home[2]
            tree_data.append({"text": home_name, "id": home_id, "type": "testHome", "children": True})
    elif type == "testHome":
        for suite in getTestSuiteByHome(id):
            suite_id = suite[0]
            suite_name = suite[1]
            tree_data.append({"text": suite_name, "id": suite_id, "type": "testSuite", "children": True})
    elif type == "testSuite":
        for case in getTestCaseBySuite(id):
            case_id = case[0]
            case_name = case[2]
            tree_data.append({"text": case_name, "id": case_id, "type": "testCase", "children": True,
                              "step_param1": case[4]})
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

