__author__ = 'Administrator'
from app_src.common.common import db, ORACLE_CHECK_REPEAT_TIME, setTestHome, setTestSuite, setTestCase, setTestStep, \
    getStepById, getTestCaseById, getTestSuiteById, getTestHomeById
import urllib.parse
import re


param_partner = '\$\(.*?\)'
templateInput = "<div class='bc_field_label'>%s</div><input id='%s' class='bc_field_input' type='input' onchange='combineValue(%d)'>"
templateTextarea = "<div class='bc_field_label'>%s</div><textarea id='%s' class='bc_field_input' type='input' onchange='combineValue(%d)'></textarea>"


def copyChildren(childrenMaps, idMaps):
    for oldValue in childrenMaps.keys():
        existsHome = getTestHomeById(oldValue)
        if existsHome:
            newValue = [idMaps[existsHome[0]], existsHome[1], existsHome[2], existsHome[3]]
            sql = "insert into testHome VALUES (:suite_id, :suite_description, :user_id, :POSITION)"
            db.execute(sql, newValue)
            continue
        existsSuite = getTestSuiteById(oldValue)
        if existsSuite:
            newValue = [idMaps[existsSuite[0]], existsSuite[1], existsSuite[2], existsSuite[3], idMaps[existsSuite[4]]]
            sql = "insert into testSuites VALUES (:suite_id, :suite_description, :user_id, :POSITION, :home_id)"
            db.execute(sql, newValue)
            continue
        existsCase = getTestCaseById(oldValue)
        if existsCase:
            newValue = [idMaps[existsCase[0]], idMaps[existsCase[1]], existsCase[2], existsCase[3], existsCase[4]]
            sql = "insert into testCases VALUES (:case_id, :suite_id, :case_description, :POSITION, :repeat)"
            db.execute(sql, newValue)
            continue
        existsStep = getStepById(oldValue)
        if existsStep:
            newValue = [idMaps[existsStep[0]], existsStep[1], existsStep[2], existsStep[3], existsStep[4], existsStep[5], existsStep[6], idMaps[existsStep[7]], existsStep[8], existsStep[9]]
            sql = "insert into testSteps VALUES (:step_id, :step_type, :step_param1, :step_param2, " \
              ":step_param3, :step_param4, :step_param5, :case_id, :step_name, :POSITION )"
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
    if data['type'] == 'testHome':
        sql_1 = "update testHome set POSITION = POSITION + 1 where POSITION >= :v1 and user_id=:v2"
        sql_2 = "insert into testHome select :home_id, :user_id, home_description, " \
                ":position from testHome where home_id =:v1"
        # 有可能多用户合并展示，需要将用户id分离
        if len(new_parent) > 4 and new_parent[:4] == 'root':
            new_parent = new_parent[4:]
        else:
            new_parent = user_id
    elif data['type'] == 'testSuite':
        sql_1 = "update testSuites set POSITION = POSITION + 1 where POSITION >= :v1 and home_id=:v2"
        db.execute(sql_1, [new_position, new_parent])
        sql_2 = "insert into testSuites select :suite_id, suite_description, " \
                ":user_id, :position, :home_id from testSuites where suite_id =:v1"
        db.execute(sql_2, [new_id, user_id, new_position, new_parent, ori_id])
    # 新增复制suite上的参数配置
        sql_3 = "insert into user_params " \
              "select user_id, param_name, param_type, param_value, :v1 from user_params " \
              "where param_tree_id=:V2"
        db.execute(sql_3, [new_id, ori_id])
    # 新增复制testSchedule
        sql_4 = "insert into runSchedule " \
              "select :v1, isRun, isSend, min, hour, day, month, week from runSchedule " \
              "where testSuiteId=:V2"
        db.execute(sql_4, [new_id, ori_id])
    elif data['type'] == 'testCase':
        sql_1 = "update testCases set POSITION = POSITION + 1 where POSITION >= :v1 and suite_id=:v2"
        sql_2 = "insert into testCases select :case_id, :suite_id, case_description, :position, repeat " \
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

    if data['type'] != 'testSuite': # sql不大一样
        db.execute(sql_1, [new_position, new_parent])
        db.execute(sql_2, [new_id, new_parent, new_position, ori_id])
    copyChildren(childrenMaps, idMaps)
    db.commit()



def moveNode(data, user_id):
    id = data['id']
    old_position = data['old_position']
    # old_parent = data['old_parent']
    new_position = data['new_position']
    new_parent = data['new_parent']
    type = data['type']

    if type == 'testHome':
        sql_0 = "select user_id from testHome where home_id = :v1"
        sql_1 = "update testHome set position=-2 where home_id = :v1"
        sql_2 = "update testHome set position = POSITION -1 where POSITION >:v1 and user_id =:v2"
        sql_3 = "update testHome set position = POSITION +1 where POSITION >=:v1 and user_id =:v2"
        sql_4 = "update testHome set position = :v1, user_id= :v2 where  home_id=:v3"
        # 有可能多用户合并展示，需要将用户id分离
        if len(new_parent) > 4 and new_parent[:4] == 'root':
            new_parent = new_parent[4:]
        else:
            new_parent = user_id
    elif type == 'testSuite':
        sql_0 = "select home_id from testSuites where suite_id = :v1"
        sql_1 = "update testSuites set position=-2 where suite_id = :v1"
        sql_2 = "update testSuites set position = POSITION -1 where POSITION >:v1 and home_id =:v2"
        sql_3 = "update testSuites set position = POSITION +1 where POSITION >=:v1 and home_id =:v2"
        sql_4 = "update testSuites set position = :v1, home_id= :v2 where suite_id=:v3"
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
    db.execute(sql_3, [new_position, new_parent])
    db.execute(sql_4, [new_position, new_parent, id])
    db.commit()


def addNode(data, user_id):
    id = data['id']
    parent = data['parent']
    if data['type'] == 'testHome':
        if len(parent) > 4 and parent[:4] == 'root':
            parent = parent[4:]
        else:
            parent = user_id
        sql_po = "select count(1) from testHome where user_id=:user_id"
        position = db.execute(sql_po, [parent, ]).fetchone()
        sql = "insert into testHome VALUES (:home_id, :user_id, :home_description, :POSITION)"
        db.execute(sql, [id, parent, 'new testHome', position[0]])
    elif data['type'] == 'testSuite':
        sql_po = "select count(1) from testSuites where home_id=:home_id"
        position = db.execute(sql_po, [parent, ]).fetchone()
        sql = "insert into testSuites VALUES (:suite_id, :suite_description, :user_id, :POSITION, :home_id)"
        db.execute(sql, [id, 'new testSuite', user_id, position[0], parent])
        # 增加了执行计划，因此需要同时增加数据
        sql_1 = "insert into runSchedule values (:suite_id, 'no', 'no', -1, -1, -1, -1, -1)"
        db.execute(sql_1, [id, ])
    elif data['type'] == 'testCase':
        sql_po = "select count(1) from testCases where suite_id=:suite_id"
        position = db.execute(sql_po, [parent, ]).fetchone()
        sql = "insert into testCases VALUES (:case_id, :suite_id, :case_description, :POSITION, :repeat)"
        db.execute(sql, [id, parent, 'new testCase', position[0], 1])
    elif data['type'][:8] == 'testStep':
        sql_po = "select count(1) from testSteps where case_id=:case_id"
        position = db.execute(sql_po, [parent, ]).fetchone()
        sql = "insert into testSteps VALUES (:step_id, :step_type, :step_param1, :step_param2, " \
              ":step_param3, :step_param4, :step_param5, :case_id, :step_name, :POSITION )"
        db.execute(sql, [id, data['type'], '', '', '', '', '', parent, 'new testStep', position[0]])
    db.commit()


def getParamTypes(selected, type=0):
    defaultParamTypes = ['string', 'db_oracle', 'db_gmdb', 'db_mysql', 'linux', 'sql_result', 'cmd']
    GUIParamTypes = ['openApp', 'wait', 'input', 'click', 'closeApp']
    # GUIParamTypes = ['environment', 'openApp', 'wait', 'input', 'click', 'closeApp']
    if type == 0:
        paramTypes = defaultParamTypes
    else:
        paramTypes = GUIParamTypes
    result = '<select name="param_type">'
    for i in paramTypes:
        if i == selected:
            result += '<option value =' + i + ' selected>' + i + '</option>'
        else:
            result += '<option value ="' + i + '">' + i + '</option>'
    result += '</select>'
    return result


def getStepParamByUser(user_id, testSuiteId, stepType):
    def distinct(res):
        temp_list = []
        res_list = []
        for i in res:
            if i[1] in temp_list and (i[4][-3:] == 'sys' or i[4][:4] == 'root'):
                pass
            else:
                temp_list.append(i[1])
                res_list.append(i)
        return res_list

    result = []
    if stepType == 'testStepDbExecute':
        sql_1 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type in('db_oracle', 'db_gmdb', 'db_mysql') and (param_tree_id like 'root%' or param_tree_id = :v2)"
        sql_2 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type='sql_result' and (param_tree_id like 'root%' or param_tree_id = :v2)"
        res1 = db.execute(sql_1, [user_id, testSuiteId]).fetchall()
        res2 = db.execute(sql_2, [user_id, testSuiteId]).fetchall()
        result.append(distinct(res1))
        result.append(distinct(res2))
    elif stepType == 'testStepFile':
        sql_1 = "select * from user_params WHERE user_id=:v1 and param_type='linux' and (param_tree_id like 'root%' or param_tree_id = :v2)"
        res1 = db.execute(sql_1, [user_id, testSuiteId]).fetchall()
        result.append(distinct(res1))
    elif stepType == 'testStepDbCheck':
        sql_1 = "SELECT * FROM user_params WHERE user_id=:v1 and param_type in('db_oracle', 'db_gmdb', 'db_mysql') and (param_tree_id like 'root%' or param_tree_id = :v2)"
        res1 = db.execute(sql_1, [user_id, testSuiteId]).fetchall()
        result.append(distinct(res1))
        result.append([ORACLE_CHECK_REPEAT_TIME])   # 增加check的执行循环次数
    elif stepType == 'testStepWebInterface':
        "nothing to select, nothing to return"
    elif stepType == 'testStepCmd':
        sql_1 = "select * from user_params WHERE user_id=:v1 and param_type='linux' and (param_tree_id like 'root%' or param_tree_id = :v2)"
        sql_2 = "select * from user_params WHERE user_id=:v1 and param_type='cmd' and (param_tree_id like 'root%' or param_tree_id = :v2)" \
                "union select * from user_params WHERE param_type='cmd' and param_tree_id like 'sys%' "
        res1 = db.execute(sql_1, [user_id, testSuiteId]).fetchall()
        res2 = db.execute(sql_2, [user_id, testSuiteId]).fetchall()
        result.append(distinct(res1))
        dis_res2 = distinct(res2)
        result.append(dis_res2)
        dis_res3 = []
        for i in distinct(dis_res2):
            dis_res3.append(cmd_translate(i[3]))
        result.append(dis_res3)
        result.append([ORACLE_CHECK_REPEAT_TIME])  # 增加check的执行循环次数
    # 专门查询用户参数并且转换成html, 此处id为参数名称
    # elif stepType == 'CmdParam':
    #     sql_1 = "select * from user_params where user_id=:v1 and param_type='cmd' and param_name=:v2"
    #     res1 = db.execute(sql_1, [user_id, testSuiteId]).fetchall()
    #     result.append(cmdParam2html(distinct(res1)))
    elif stepType == 'All':
        sql_1 = "select * from user_params WHERE user_id=:v1 and param_tree_id in('root', :v2) " \
                "union select * from user_params WHERE param_type='cmd' and param_tree_id='sys' "
        res1 = db.execute(sql_1, [user_id, testSuiteId]).fetchall()
        result.append(distinct(res1))
    return result


def cmd_translate(ori_cmd):
    cmdDetails = ""
    res = re.findall(param_partner, ori_cmd)
    for i in range(len(res)):
        item_name = "占位符" if res[i][2:-1] == '' else res[i][2:-1] if res[i][2:-1] != "output" else "期望的输出"
        item_id = 'cmd_' + str(i)
        cmdDetails += templateInput % (item_name, item_id, len(res)) if res[i][2:-1] != "output" else templateTextarea % (item_name, item_id, len(res))
    return cmdDetails


def makeParamTableHtml(user_id, param_tree_id):
    tableData = ""
    rowId = 0
    results = db.execute("SELECT * FROM user_params "
                         "WHERE user_id=:v1 and param_tree_id=:v2 "
                         "order by param_type, ROWID", [user_id, param_tree_id]).fetchall()
    if len(results) == 0:
        return ""
    for result in results:
        rowId += 1
        tableData += "<tr id='line" + str(rowId) + "' align='center'>" \
           "<td class='td_Num'>" + str(rowId) + "</td>" \
           "<td class='td_Item'>" + getParamTypes(result[2]) + "</td>" \
           "<td class='td_Item'><input name='param_name' type='text' value='" + result[1] + "'></td>" \
           "<td class='td_Item'><input name='param_value'type='text' value='" + result[3] + "'></td> \
          <td class='td_Oper'>" \
                  '''<span onclick='up_exchange_line($(this).parent().parent().find("td:first-child").html());'> 上移 </span>''' \
                  '''<span onclick='down_exchange_line($(this).parent().parent().find("td:first-child").html());'> 下移 </span>''' \
                  '''<span onclick='insert_onTheLine($(this).parent().parent().find("td:first-child").html());'> 上插 </span> ''' \
                  "<span onclick='remove_line(this);'> 删除 </span>" \
                  "</td>"
    return tableData + "</table>"


def makeGUItable(param_tree_id):
    tableData = ""
    rowId = 0
    results = db.execute("SELECT * FROM test_GUI WHERE step_id= :v1 order by line_index", [param_tree_id]).fetchall()
    if len(results) == 0:
        return ""
    for result in results:
        rowId += 1
        if len(result[8]) > 0:
            image = "<img src='" + result[8] + "'><div class='marker' style='left: " + str(result[4]) + "px; top: " + str(result[5]) + "px; padding: 0px;'></div>"
        else:
            image = ""

        if result[10] == 0:
            is_pass = "<select type='text' name='is_pass'><option value='0' selected>no</option><option value='1'>yes</option></select>"
        else:
            is_pass = "<select type='text' name='is_pass'><option value='0'>no</option><option value='1' selected>yes</option></select>"

        tableData += "<tr id='line" + str(rowId) + "'>" \
        "<td class='td_Num'>" + str(rowId) + "</td>" \
        "<td class='td_Item'>" + getParamTypes(result[2], 1) + "</td>" \
        "<td class='td_Item' style='text-align: left;'><input type='text' onchange='changeInputValue(this)' name='pasteInput' placeholder='截屏后粘贴到输入框中' size='17' value='" + result[3] + "'/></div>" \
        "<div class='img' style='padding: 0px;'>" + image + "</div>" \
        "<input name='x' hidden='hidden' value='" + str(result[4]) + "'/>" \
        "<input name='y' hidden='hidden' value='" + str(result[5]) + "'/>" \
        "<input name='xo' hidden='hidden' value='" + str(result[6]) + "'/>" \
        "<input name='yo' hidden='hidden' value='" + str(result[7]) + "'/>" \
        "<input name='picSrc' hidden='hidden' value='" + result[8] + "'/>" \
        "</td>" \
        "<td class='td_Item'><input type='text' onchange='changeInputValue(this)' name='param_value' value='" + result[9] + "'></td>" \
        "<td class='td_Item'>" + is_pass + "</td>" \
        "<td class='td_Oper'>" \
        "<span onclick=\"gui_up_exchange_line($(this).parent().parent().find('td:first-child').html());\"> 上移 </span> " \
        "<span onclick=\"gui_down_exchange_line($(this).parent().parent().find('td:first-child').html());\"> 下移 </span> " \
        "<span onclick=\"gui_insert_onTheLine($(this).parent().parent().find('td:first-child').html());\"> 上插 </span> " \
        "<span onclick='gui_remove_line(this);'> 删除 </span> " \
        "</td>" \
        "</tr>"
    return tableData + "</table>"


def saveGUIParam(param_tree_id, params):
    params = urllib.parse.unquote(params.decode())
    params2list = params.split('&')
    b = [i.split('=', 1)[1] for i in params2list]
    c = [b[i:i + 9] for i in range(0, len(b), 9)] # 字段个数为9
    d = []
    results = []
    for i in c:
        if i[1] == "" and i[6] == "" and i[7] == "" and i[0] != 'closeApp':
            # print(i)
            pass
        else:
            d.append(i)
    for i, j in enumerate(d):
        e = [param_tree_id, i]
        e.extend(j)
        results.append(e)
    try:
        sql_clear = "delete from test_GUI where step_id = :v1"
        db.execute(sql_clear, [param_tree_id])
        sql_insert = "insert into test_GUI(step_id, line_index, param_type, param_name, x, y, xo, yo, picsrc, param_value, is_pass)" \
                     "values (:step_id, :line_index, :param_type, :param_name, :x, :y, :xo, :yo, :picsrc, :param_value, :is_pass)"
        db.executemany(sql_insert, results)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return str(e)
    else:
        db.commit()
        return 0


def saveUserParam(user_id, param_tree_id, params):
    params = urllib.parse.unquote(params.decode())
    params2list = params.split('&')
    trans_results = [i.replace('param_type=', '').replace('param_name=', '').replace('param_value=', '') for i in
                     params2list]
    results = [trans_results[i:i + 3] for i in range(0, len(trans_results), 3)]
    try:
        sql_delete = "delete from user_params where user_id=:v1 and param_tree_id=:v2"
        db.execute(sql_delete, [user_id, param_tree_id])
        sql = "insert into user_params(user_id, param_type, param_name, param_value, param_tree_id) values ('%s', :param_type, :param_name, :param_value, '%s')" % (user_id, param_tree_id)
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
    suite_list = []
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
        print('datas', datas)
        for data in datas:
            if data['type'] == 'testHome':
                setTestHome(data['id'], data['text'], user_id)
            elif data['type'] == 'testSuite':
                setTestSuite(data['id'], data['text'], data['parent'], user_id)
            elif data['type'] == 'testCase':
                setTestCase(data['id'], data['parent'], data['text'], data['step_param1'])
            elif data['type'][:8] == 'testStep':
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])
    elif type == 'testHome':
        for data in datas:
            if data['type'] == 'testHome':
                setTestHome(data['id'], data['text'], user_id)
        for data in datas:
            if data['type'] == 'testSuite' and data['parent'] == id:
                suite_list.append(data['id'])
                setTestSuite(data['id'], data['text'], data['parent'], user_id)
        for data in datas:
            if data['type'] == 'testCase' and data['parent'] in suite_list:
                case_list.append(data['id'])
                setTestCase(data['id'], data['parent'], data['text'], data['step_param1'])
        for data in datas:
            if data['type'][:8] == 'testStep' and data['parent'] in case_list:
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])
    elif type == 'testSuite':
        for data in datas:
            if data['type'] == 'testSuite' and data['id'] == id:
                setTestSuite(data['id'], data['text'], data['parent'], user_id)
        for data in datas:
            if data['type'] == 'testCase' and data['parent'] == id:
                case_list.append(data['id'])
                setTestCase(data['id'], data['parent'], data['text'], data['step_param1'])
        for data in datas:
            if data['type'][:8] == 'testStep' and data['parent'] in case_list:
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])
    elif type == 'testCase':
        for data in datas:
            if data['type'] == 'testCase' and data['id'] == id:
                case_list.append(data['id'])
                setTestCase(data['id'], data['parent'], data['text'], data['step_param1'])
        for data in datas:
            if data['type'][:8] == 'testStep' and data['parent'] == id :
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])
    elif type[:8] == 'testStep':
        for data in datas:
            if data['type'][:8] == 'testStep' and data['id'] == id :
                setTestStep(data['id'], data['type'], data['step_param1'], data['step_param2'], data['step_param3'],
                            data['step_param4'], data['step_param5'], data['parent'], data['text'])