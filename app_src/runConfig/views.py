__author__ = 'Administrator'

from flask import render_template, flash, request, redirect, url_for, json, jsonify, session
from . import runConfig
from app_src.common.common import *
from app_src.main.functions import cmd_translate


@runConfig.route('/functionConfig', methods=['GET', 'POST'])
@check_login
def functionConfig():
    return render_template('runConfig/index.html')


@runConfig.route('/functionData', methods=['GET', 'POST'])
@check_login
def functionData():
    user_id = getUserId()
    res_ability = db.execute("select ability_id, ability_type from testAbility").fetchall()
    all_ability = {key: val for key, val in res_ability}
    func_list = db.execute(
        "select function_id, function_name, position, user_id "
        "from testFunction where user_id=:v1", [user_id, ]).fetchall()
    tree_data = {i[0]: {'name': i[1], 'position': i[2]} for i in func_list}
    for i in func_list:
        detail = db.execute("select * from testFunctionDetail where function_id=:v1", [i[0]]).fetchall()
        tree_data[i[0]]['detail'] = detail

    tree_list = []
    for j in tree_data.keys():
        tree_list.append(({"text": tree_data[j]['name'], "id": j, "type": "function",
                           "children": [{"text": k[2], "id": k[0], "children": False, "type": all_ability[k[4]],
                                         "a_attr": {"step_param1": k[5], "step_param2": k[6], "step_param3": k[7],
                                         "step_param4": k[8], "step_param5": k[9]}} for k in tree_data[j]['detail']]}))

    if not user_id:
        tree_list.append({'id': 'a1', 'type': 'other', 'text': '1', 'children': False})
    print(f"{tree_list=}")
    return jsonify({'resultCode': 200,
                    'result': [{'id': 'root', 'type': 'root', 'text': 'functionConfig', 'children': tree_list}]})


@runConfig.route('/synchronizeConfig', methods=['GET', 'POST'])
@check_login
def synchronizeConfig():
    data = json.loads(request.get_data())
    user_id = getUserId()
    saveRunConfig(data, user_id)
    return jsonify({'resultCode': 200, 'result': ""})


def saveRunConfig(data, user_id):
    # print("data:", data, "----")
    parents = [i for i in data if i['type'] == 'function']
    children = [i for i in data if i['parent'] in [j['id'] for j in parents]]
    print(f"{parents=} \n {children=}")
    sql_clean_func = "delete from testFunction where user_id=:v1"
    sql_insert_func = "insert into testFunction (function_id, function_name, position, user_id) " \
                 "values (:v1, :v2, :v3, :v4)"
    db.execute(sql_clean_func, [user_id])
    position = 0
    for i in parents:
        db.execute(sql_insert_func, [i['id'], i['text'], position, user_id])
        position += 1

    sql_clean_detail = "delete from testFunctionDetail where function_id=:v1"
    sql_insert_detail = "insert into testFunctionDetail (detail_id, function_id, detail_name, position, ability_id, " \
                        "ability_param_1, ability_param_2, ability_param_3, ability_param_4, ability_param_5) " \
                      "values (:detail_id, :function_id, :detail_name, :position, :ability_id, " \
                        ":ability_param_1, :ability_param_2, :ability_param_3, :ability_param_4, :ability_param_5)"
    db.executemany(sql_clean_detail, [[i['id']] for i in parents])
    order_list = {}
    for j in children:
        print(f"jjjjj={j}")
        if j['parent'] not in order_list.keys():
            order_list[j['parent']] = 0
        else:
            order_list[j['parent']] = order_list[j['parent']] + 1
        db.execute(sql_insert_detail, [j['id'], j['parent'], j['text'], order_list[j['parent']], j['type'],
                                       j.get('step_param1', ''), j.get('step_param2', ''), j.get('step_param3', ''),
                                       j.get('step_param4', ''), j.get('step_param5', '')])
    db.commit()


@runConfig.route('/addNode', methods=['GET', 'POST'])
@check_login
def configAddNode():
    data = json.loads(request.get_data())
    user_id = getUserId()
    addNode(data, user_id)
    return jsonify({'resultCode': 200, 'result': ""})


def addNode(data, user_id):
    id = data['id']
    parent = data['parent']
    print(f"add node!{data=}")
    if data['type'][:8] == 'testStep':
        sql_po = "select max(position) from testFunctionDetail where function_id=:parent"
        position = db.execute(sql_po, [parent, ]).fetchone()
        sql = "insert into testFunctionDetail VALUES (:detail_id, :function_id, :detail_name, :position, :ability_id, " \
              ":ability_param_1, :ability_param_2, :ability_param_3, :ability_param_4, :ability_param_5)"
        db.execute(sql, [id, parent, 'new ability', position[0] + 1 if position[0] else 0, data['type'], '', '', '', '', ''])
    elif data['type'] == 'function':
        sql_po = "select max(position) from testFunction where user_id=:v1"
        position = db.execute(sql_po, [user_id, ]).fetchone()
        sql = "insert into testFunction VALUES (:function_id, :function_name, :position, :user_id)"
        db.execute(sql,
                   [id, 'new function', position[0] + 1 if position[0] else 0, user_id])
    db.commit()


@runConfig.route('/queryStepParam', methods=['GET', 'POST'])
@check_login
def queryStepParam():
    stepType = request.args.get("stepType")
    user_id = getUserId()
    res = getParamByUser(user_id, stepType)
    if res:
        result = jsonify({'resultCode': 200, 'result': res})
    else:
        result = jsonify({'resultCode': 0, 'result': ""})
    return result


@runConfig.route('/queryFuncParam', methods=['GET', 'POST'])
@check_login
def queryFuncParam():
    func_id = request.args.get("func_id")   # 前16位为function id，后16位为dom id
    user_id = getUserId()
    res = getFuncParam(func_id, user_id)
    if res:
        result = jsonify({'resultCode': 200, 'result': res})
    else:
        result = jsonify({'resultCode': 0, 'result': ""})
    return result


def getFuncParam(step_id, user_id):
    def check_param(params, dest):
        res = []
        for i in params.keys():
            if "$(" + i + ")" in dest:
                res.append(i)
        return res
    func_id = step_id[:16]
    print(func_id, step_id)
    func2suite = "select suite_id from testCases a, testSteps b " \
                 "where a.case_id = b.case_id and b.step_id = :v1"
    suite_id = db.execute(func2suite, [step_id]).fetchone()
    if not suite_id:
        return
    else:
        suite_id = suite_id[0]
    all_params_res = db.execute("select param_name, param_value from user_params where user_id in (:v1, 'sys') and "
                            "param_type in('string') and param_tree_id in ('root', :v2)", [user_id, suite_id]).fetchall()
    all_params = {}
    for i in all_params_res:
        all_params[i[0]] = i[1]

    sql = "select detail_name, ability_param_1, ability_param_2, ability_param_3, ability_param_4, ability_param_5 " \
          "from testFunctionDetail where function_id=:v1"
    res = db.execute(sql, [func_id]).fetchall()
    func_params = []
    for i in res:
        for j in range(1, 6):
            func_params.extend(check_param(all_params, i[j]))
    func_params = list(set(func_params))
    tableData = ""
    rowId = 0
    for result in func_params:
        rowId += 1
        tableData += "<tr id='line" + str(rowId) + "' align='center'>" \
               "<td class='td_Num'>" + str(rowId) + "</td>" \
               "<td class='td_Item'><input readonly='readonly' name='param_name' type='text' value='" + result + "'></td>" \
               "<td class='td_Item'><input name='param_value'type='text' value='" + all_params[result] + "'></td> \
              <td class='td_Oper'></td>"
    return tableData + "</table>"


def getParamByUser(user_id, stepType):
    result = []
    if stepType == 'testStepDbExecute':
        sql_1 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type in('db_oracle', 'db_gmdb', 'db_mysql') and (param_tree_id like 'root%')"
        sql_2 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type='sql_result' and (param_tree_id like 'root%')"
        res1 = db.execute(sql_1, [user_id]).fetchall()
        res2 = db.execute(sql_2, [user_id]).fetchall()
        result.append(res1)
        result.append(res2)
    elif stepType == 'testStepFile':
        sql_1 = "select * from user_params WHERE user_id=:v1 and param_type='linux' and (param_tree_id like 'root%')"
        res1 = db.execute(sql_1, [user_id]).fetchall()
        result.append(res1)
    elif stepType == 'testStepDbCheck':
        sql_1 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type in('db_oracle', 'db_gmdb', 'db_mysql') and (param_tree_id like 'root%')"
        res1 = db.execute(sql_1, [user_id]).fetchall()
        result.append(res1)
        result.append([ORACLE_CHECK_REPEAT_TIME])  # 增加check的执行循环次数
    elif stepType == 'testStepWebInterface':
        "nothing to select, nothing to return"
    elif stepType == 'testStepCmd':
        sql_1 = "select * from user_params WHERE user_id=:v1 and param_type='linux' and (param_tree_id like 'root%')"
        sql_2 = "select * from user_params WHERE user_id=:v1 and param_type='cmd' and (param_tree_id like 'root%')" \
                "union select * from user_params WHERE param_type='cmd' and param_tree_id like 'sys%' "
        res1 = db.execute(sql_1, [user_id]).fetchall()
        res2 = db.execute(sql_2, [user_id]).fetchall()
        result.append(res1)
        dis_res2 = res2
        result.append(dis_res2)
        dis_res3 = []
        for i in dis_res2:
            dis_res3.append(cmd_translate(i[3]))
        result.append(dis_res3)
        result.append([ORACLE_CHECK_REPEAT_TIME])
    elif stepType == 'All':
        sql_1 = "select * from user_params WHERE user_id=:v1 and param_tree_id ='root' " \
                "union select * from user_params WHERE param_type='cmd' and param_tree_id='sys' "
        res1 = db.execute(sql_1, [user_id]).fetchall()
        result.append(res1)
    return result


@runConfig.route('/getSelfFunc', methods=['GET', ])
@check_login
def getSelfFunc():
    res = getUserFunc()
    return jsonify({'resultCode': 200, 'result': res})


def getUserFunc():
    func = []
    user_id = getUserId()
    sql = "select function_id, function_name from testFunction where user_id=:v1"
    res = db.execute(sql, [user_id]).fetchall()
    for i in res:
        func.append({"name": i[0], "label": i[1]})
    return func

