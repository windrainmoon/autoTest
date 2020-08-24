__author__ = 'Administrator'
from app.common.common import db, crID, setTestSuite, setTestCase, setTestStep, getStepById, getTestCaseById, getTestSuiteById
import urllib.parse


def copyChildren(childrenMaps, idMaps):
    for oldValue in childrenMaps.keys():
        existsSuite = getTestSuiteById(oldValue)
        if existsSuite:
            newValue = [idMaps[existsSuite[0]], existsSuite[1], existsSuite[2], existsSuite[3]]
            sql = "insert into testSuites VALUES (:suite_id, :suite_description, :user_id, :POSITION)"
            db.execute(sql, newValue)
            continue
        existsCase = getTestCaseById(oldValue)
        if existsCase:
            newValue = [idMaps[existsCase[0]], idMaps[existsCase[1]], existsCase[2], existsCase[3]]
            sql = "insert into testCases VALUES (:case_id, :suite_id, :case_description, :POSITION)"
            db.execute(sql, newValue)
            continue
        existsStep = getStepById(oldValue)
        if existsStep:
            print(existsStep)
            newValue = [idMaps[existsStep[0]], existsStep[1], existsStep[2], existsStep[3], existsStep[4], existsStep[5], existsStep[6], idMaps[existsStep[7]], existsStep[8], existsStep[9]]
            sql = "insert into testSteps VALUES (:step_id, :step_type, :step_param1, :step_param2, " \
              ":step_param3, :step_param4, :step_param5, :case_id, :step_name, :POSITION )"
            print(sql, newValue)
            db.execute(sql, newValue)
            continue
    db.commit()


def copyNode(data, user_id):
    print(data)
    old_children = data['oriChildren']
    ori_parent = data['oriParent']
    new_children = data['newChildren']
    new_position = data['position']
    new_parent = data['newParent']
    new_id = data['newId']
    ori_id = data['oriId']
    childrenMaps = dict(zip(old_children, new_children))
    idMaps = childrenMaps.copy()
    idMaps[ori_id] = new_id
    idMaps[ori_parent] = new_parent
    if type == 'testSuite':
        sql_1 = "update testSuites set POSITION = POSITION + 1 where POSITION >= :v1 and -1!=:v2"
        sql_2 = "insert into testSuites select :suite_id, suite_description, " \
                ":user_id, :position from testSuites where suite_id =:v1"
        new_parent = user_id
    elif data['type'] == 'testCase':
        sql_1 = "update testCases set POSITION = POSITION + 1 where POSITION >= :v1 and suite_id=:v2"
        sql_2 = "insert into testCases select :case_id, :suite_id, case_description, :position " \
                "from testCases where case_id=:old_case_id"

    elif data['type'][:8] == 'testStep':
        sql_1 = "update testSteps set POSITION = POSITION + 1 where POSITION >= :v1 and case_id=:v2"
        sql_2 = "insert into testSteps select :step_id, step_type, step_param1, step_param2, step_param3," \
                "step_param4, step_param5, :case_id, step_name, :POSITION " \
                "from testSteps where step_id =:old_step_id"
    else:
        return
    # print(sql_1, [new_position, new_parent])
    # print(sql_2, [new_id, new_parent, new_position, ori_id])
    db.execute(sql_1, [new_position, new_parent])
    db.execute(sql_2, [new_id, new_parent, new_position, ori_id])
    copyChildren(childrenMaps, idMaps)
    db.commit()



def moveNode(data, user_id):
    # print(data)
    id = data['id']
    old_position = data['old_position']
    # old_parent = data['old_parent']
    new_position = data['new_position']
    new_parent = data['new_parent']
    type = data['type']

    if type == 'testSuite':
        sql_0 = "select user_id from testSuites where suite_id = :v1"
        sql_1 = "update testSuites set position=-2 where suite_id = :v1"
        sql_2 = "update testSuites set position = POSITION -1 where POSITION >:v1 and user_id =:v2"
        sql_3 = "update testSuites set position = POSITION +1 where POSITION >=:v1 and user_id =:v2"
        sql_4 = "update testSuites set position = :v1 where :v2!= -1 and suite_id=:v3"
    elif data['type'] == 'testCase':
        sql_0 = "select suite_id from testCases where case_id = :v1"
        sql_1 = "update testCases set position=-2 where case_id = :v1"
        sql_2 = "update testCases set position = POSITION -1 where POSITION >:v1 and suite_id =:v2"
        sql_3 = "update testCases set position = POSITION +1 where POSITION >=:v1 and suite_id =:v2"
        sql_4 = "update testCases set position = :v1,suite_id=:v2 where case_id=:v3"
    elif data['type'][:8] == 'testStep':
        sql_0 = "select case_id from testSteps where step_id = :v1"
        sql_1 = "update testSteps set position=-2 where step_id = :v1"
        sql_2 = "update testSteps set position = POSITION -1 where POSITION >:v1 and case_id =:v2"
        sql_3 = "update testSteps set position = POSITION +1 where POSITION >=:v1 and case_id =:v2"
        sql_4 = "update testSteps set position = :v1,case_id=:v2 where step_id=:v3"
    else:
        return
    parent = db.execute(sql_0, [id, ]).fetchone()
    db.execute(sql_1, [id, ])
    db.execute(sql_2, [old_position, parent[0]])
    db.execute(sql_3, [new_position, parent[0]])
    db.execute(sql_4, [new_position, new_parent, id])
    db.commit()


def addNode(data, user_id):
    if data['type'] == 'testSuite':
        sql_po = "select count(1) from testSuites where user_id=:user_id"
        position = db.execute(sql_po, [user_id, ]).fetchone()
        sql = "insert into testSuites VALUES (:suite_id, :suite_description, :user_id, :POSITION)"
        db.execute(sql, [data['id'], 'new testSuite', user_id, position[0]])
    elif data['type'] == 'testCase':
        sql_po = "select count(1) from testCases where suite_id=:suite_id"
        position = db.execute(sql_po, [data['parent'], ]).fetchone()
        sql = "insert into testCases VALUES (:case_id, :suite_id, :case_description, :POSITION)"
        db.execute(sql, [data['id'], data['parent'], 'new testCase', position[0]])
    elif data['type'][:8] == 'testStep':
        sql_po = "select count(1) from testSteps where case_id=:case_id"
        position = db.execute(sql_po, [data['parent'], ]).fetchone()
        sql = "insert into testSteps VALUES (:step_id, :step_type, :step_param1, :step_param2, " \
              ":step_param3, :step_param4, :step_param5, :case_id, :step_name, :POSITION )"
        db.execute(sql, [data['id'], data['type'], '', '', '', '', '', data['parent'], 'new testStep', position[0]])
    db.commit()


def getParamTypes(select):
    defaultParamTypes = ['string', 'oracle', 'linux', 'oracle_result']
    result = '<select name="param_type">'
    for i in defaultParamTypes:
        if i == select:
            result += '<option value =' + i + ' selected>' + i + '</option>'
        else:
            result += '<option value ="' + i + '">' + i + '</option>'
    result += '</select>'
    return result


def getStepParamByUser(user_id, stepType):
    result = []
    if stepType == 'testStepOracleExecute':
        sql_1 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type='oracle'"
        sql_2 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type='oracle_result'"
        res1 = db.execute(sql_1, [user_id, ]).fetchall()
        res2 = db.execute(sql_2, [user_id, ]).fetchall()
        result.append(res1)
        result.append(res2)
    elif stepType == 'testStepFile':
        sql_1 = "select * from user_params WHERE user_id=:v1 and param_type='linux'"
        res1 = db.execute(sql_1, [user_id, ]).fetchall()
        result.append(res1)
    elif stepType == 'testStepOracleCheck':
        sql_1 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type='oracle'"
        res1 = db.execute(sql_1, [user_id, ]).fetchall()
        result.append(res1)
    elif stepType == 'testStepWebInterface':
        "nothing to select, nothing to return"
    elif stepType == 'All':
        sql_1 = "select * from user_params WHERE user_id=:v1 "
        res1 = db.execute(sql_1, [user_id, ]).fetchall()
        result.append(res1)
    return result





# def makeTableHtml(user_id):
#     tableData = ""
#     results = db.execute("SELECT * FROM user_params WHERE user_id=:v1", [user_id, ]).fetchall()
#     if len(results) == 0:
#         return ""
#
#     for result in results:
#         id = crID(10)
#         tableData += "<tr id='" + id + "' align='center'>" \
#                                        "<td>" + getParamTypes(result[2]) + "</td>" \
#                                                                            "<td><input type='text' name='param_name' value=" + \
#                      result[1] + "></td>" \
#                                  "<td><input type='text' name='param_value' value=" + result[3] + "></td> \
#                   <td><input class='button round' type='button' onclick='deleteParam(" + id + ")' value='删除'/></td>"
#     return tableData + "</table>"

def makeTableHtml(user_id):
    tableData = ""
    rowId = 0
    results = db.execute("SELECT * FROM user_params WHERE user_id=:v1", [user_id, ]).fetchall()
    print(results)
    if len(results) == 0:
        return ""
    for result in results:
        rowId += 1
        tableData += "<tr id='line" + str(rowId) + "' align='center'>" \
           "<td class='td_Num'>" + str(rowId) + "</td>" \
           "<td class='td_Item'>" + getParamTypes(result[2]) + "</td>" \
           "<td class='td_Item'><input name='param_name' type='text' value=" + result[1] + "></td>" \
           "<td class='td_Item'><input name='param_value'type='text' value=" + result[3] + "></td> \
          <td class='td_Oper'>" \
                  '''<span onclick='up_exchange_line($(this).parent().parent().find("td:first-child").html());'> 上移 </span>''' \
                  '''<span onclick='down_exchange_line($(this).parent().parent().find("td:first-child").html());'> 下移 </span>''' \
                  '''<span onclick='insert_onTheLine($(this).parent().parent().find("td:first-child").html());'> 上插 </span> ''' \
                  "<span onclick='remove_line(this);'> 删除 </span>" \
                  "</td>"
    return tableData + "</table>"


def saveUserParam(user_id, params):
    params = urllib.parse.unquote(params.decode())
    params2list = params.split('&')
    trans_results = [i.replace('param_type=', '').replace('param_name=', '').replace('param_value=', '') for i in
                     params2list]
    results = [trans_results[i:i + 3] for i in range(0, len(trans_results), 3)]
    try:
        sql_delete = "delete from user_params where user_id=:v1"
        db.execute(sql_delete, [user_id, ])
        sql = "insert into user_params(user_id, param_type, param_name, param_value) values ('%s', :param_type, :param_name, :param_value)" % user_id
        db.executemany(sql, results)
        sql_delete_empty = "delete from user_params where user_id=:v1 and param_name =''  "
        db.execute(sql_delete_empty, [user_id, ])
    except Exception as e:
        db.rollback()
        return e
    else:
        db.commit()
        return 0


def saveUserTree(datas, user_id):
    case_list = []
    id = 0
    type = ''
    for data in datas:
        if len(data) == 2:
            id = data['clickedId']
            type = data['clickedType']
            datas.remove(data)   # 只能移除一次！
            break
    if type == 'root':
        for data in datas:
            if data['type'] == 'testSuite':
                setTestSuite(data['id'], data['text'], user_id)
            elif data['type'] == 'testCase':
                setTestCase(data['id'], data['parent'], data['text'])
            elif data['type'][:8] == 'testStep':
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])
    elif type == 'testSuite':
        for data in datas:
            if data['type'] == 'testSuite' and data['id'] == id:
                setTestSuite(data['id'], data['text'], user_id)
        for data in datas:
            if data['type'] == 'testCase' and data['parent'] == id:
                case_list.append(data['id'])
                setTestCase(data['id'], data['parent'], data['text'])
        for data in datas:
            if data['type'][:8] == 'testStep' and data['parent'] in case_list:
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])
    elif type == 'testCase':
        for data in datas:
            if data['type'] == 'testCase' and data['id'] == id:
                case_list.append(data['id'])
                setTestCase(data['id'], data['parent'], data['text'])
        for data in datas:
            if data['type'][:8] == 'testStep' and data['parent'] == id :
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])
    elif type[:8] == 'testStep':
        for data in datas:
            if data['type'][:8] == 'testStep' and data['id'] == id :
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])