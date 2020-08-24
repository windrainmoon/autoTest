__author__ = 'Administrator'
import random
import os
import sqlite3
from flask import session, redirect, url_for, flash, request, jsonify
from conf import SESSION_EXPIRE_TIME
import socket



db = sqlite3.connect('app/sqliteDB/base.db', check_same_thread=False, )


def get_host_ip():
    return socket.gethostbyname(socket.gethostname())


local_host = get_host_ip()


def crID(len):
    raw = ""
    range1 = range(48, 65)  # between 0~9 and :~@
    range2 = range(91, 97)  # between [~`

    i = 0
    while i < len:
        seed = random.randint(48, 122)
        if ((seed in range1) or (seed in range2)):
            continue
        raw += chr(seed)
        i += 1
    return raw


def walkFile(file):
    all_files = []
    for root, dirs, files in os.walk(file):
        for f in files:
            all_files.append(os.path.join(root, f))
    return all_files


# def testConfig2json(file):
# test_file = open(file, "r")
#     # 先将yaml转换为dict格式
#     generate_dict = yaml.load(test_file, Loader=yaml.Loader)
#     # generate_json = json.dumps(generate_dict,sort_keys=False,indent=4,separators=(',',': '))
#     # print(generate_json)
#     jsTree_list = []
#     root_id = crID(12)
#     jsTree_list.append({'id': root_id, 'parent': 'root', 'type': 'testSuite', 'text': file.replace('testCaseCategory\\', '').replace('.yml', ''), })
#     for key, value in generate_dict.items():
#         father_id = crID(12)
#         jsTree_list.append({'id': father_id, 'parent': root_id, 'type': 'testCase', 'text': key})
#         for sub_key, sub_value in value.items():
#             jsTree_list.append({'id': crID(12), 'parent': father_id, 'type': 'testCondition', 'text': sub_key,
#                                 'test_type': sub_value['test_type'], 'test_object': sub_value['test_object']})
#     return jsTree_list


# def get_yaml_data(file_name, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
#     current_path = os.path.abspath(".")
#     yaml_file = os.path.join(current_path, "testCaseCategory/%s.yml" % file_name)
#
#     # print("***获取yaml文件数据***")
#     class OrderedLoader(Loader):
#         pass
#
#     def construct_mapping(loader, node):
#         loader.flatten_mapping(node)
#         return object_pairs_hook(loader.construct_pairs(node))
#
#     OrderedLoader.add_constructor(
#         yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
#         construct_mapping)
#     with open(yaml_file) as stream:
#         return yaml.load(stream, OrderedLoader)


# def set_yaml_data(data, file_name, Dumper=yaml.SafeDumper, **kwds):
#     current_path = os.path.abspath(".")
#     yaml_file = os.path.join(current_path, "testCaseCategory/%s.yml" % file_name)
#
#     class OrderedDumper(Dumper):
#         pass
#
#     def _dict_representer(dumper, data):
#         return dumper.represent_mapping(
#             yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
#             data.items())
#
#     OrderedDumper.add_representer(OrderedDict, _dict_representer)
#     with open(yaml_file, 'w') as stream:
#         return yaml.dump(data, stream, OrderedDumper, **kwds)


def getStepById(step_id):
    # print(step_id)
    sql = "select * from testSteps where step_id=:v1"
    result = db.execute(sql, [step_id, ]).fetchone()
    return result


def getTestCaseById(case_id):
    sql = "select * from testCases where case_id=:v1"
    result = db.execute(sql, [case_id]).fetchone()
    return result


def getTestSuiteById(suite_id):
    sql = "select * from testSuites where suite_id=:v1"
    result = db.execute(sql, [suite_id]).fetchone()
    return result


def getTestStepByCase(case_id):
    sql = "select * from testSteps where case_id=:v1 order by position"
    result = db.execute(sql, [case_id]).fetchall()
    return result


def getTestCaseBySuite(suite_id):
    sql = "select * from testCases where suite_id=:v1 order by position"
    result = db.execute(sql, [suite_id]).fetchall()
    return result


def getAllSuite(user_id):
    sql = "select * from testSuites where user_id=:v1 order by position"
    result = db.execute(sql, [user_id]).fetchall()
    return result


def setTestCase(case_id, suite_id, case_name):
    exist = getTestCaseById(case_id)
    if exist:
        sql = "update testCases set case_description=:case_name, suite_id=:suite_id " \
              " where case_id=:case_id "
        db.execute(sql, [case_name, suite_id, case_id])
    else:
        sql = "insert into testCases VALUES (:case_id, :suite_id, :case_name, :POSITION )"
        db.execute(sql, [case_id, suite_id, case_name, -1])
    db.commit()


def setTestSuite(suite_id, suite_description, user_id):
    exist = getTestSuiteById(suite_id)
    if exist:
        sql = "update testSuites set suite_description=:suite_description, user_id=:user_id " \
              "WHERE suite_id=:suite_id"
        db.execute(sql, [suite_description, user_id, suite_id])
    else:
        sql = "insert into testSuites VALUES (:suite_id, :suite_description, :user_id, :POSITION )"
        db.execute(sql, [suite_id, suite_description, user_id, -1])
    db.commit()


def setTestStep(step_id, step_type, step_param1, step_param2, step_param3, step_param4, step_param5, case_id, step_name):
    exist = getStepById(step_id)
    if exist:
        sql = "update testSteps set step_type=:step_type, step_param1=:step_param1," \
              "step_param2=:step_param2, step_param3=:step_param3, step_param4=:step_param4, " \
              "step_param5=:step_param5, case_id=:case_id, step_name=:step_name " \
              "WHERE step_id=:step_id"
        db.execute(sql, [step_type, step_param1, step_param2, step_param3, step_param4, step_param5, case_id, step_name, step_id])
    else:
        sql = "insert into testSteps VALUES (:step_id, :step_type, :step_param1, :step_param2, " \
              ":step_param3, :step_param4, :step_param5, :case_id, :step_name, :POSITION )"
        db.execute(sql, [step_id, step_type, step_param1, step_param2, step_param3, step_param4, step_param5,
                         case_id, step_name, -1])
    db.commit()




def dropTestStepById(step_id):
    exist = getStepById(step_id)
    if exist:
        print(exist)
        sql = "delete from testSteps where step_id=:step_id"
        sql_1 = "update testSteps set position =(select count(*) from testSteps b  where testSteps.position > b.position and case_id=:parent_id) where case_id=:parent_id"
        db.execute(sql, [step_id, ])
        db.execute(sql_1, [exist[7], ])
        db.commit()


def dropTestCaseById(case_id):
    exist = getTestCaseById(case_id)
    print(exist)
    if exist:
        dropTestStepByCase(case_id)
        sql = "delete from testCases where case_id=:case_id"
        sql_1 = "update testCases set position =(select count(*) from testCases b  where testCases.position > b.position and suite_id=:parent_id) where suite_id=:parent_id"
        db.execute(sql, [case_id, ])
        db.execute(sql_1, [exist[1]])
        db.commit()


def dropTestSuiteById(suite_id):
    exist = getTestSuiteById(suite_id)
    if exist:
        dropTestCaseBySuite(suite_id)
        sql = "delete from testSuites where suite_id=:suite_id"
        sql_1 = "update testSuites set position =(select count(*) from testSuites b  where testSuites.position > b.position and user_id=:parent_id) where user_id=:parent_id"
        db.execute(sql, [suite_id, ])
        db.execute(sql_1, [exist[2], ])
        db.commit()


def dropTestStepByCase(case_id):
    exist = getTestStepByCase(case_id)
    if exist:
        sql = "delete from testSteps where case_id=:case_id"
        db.execute(sql, [case_id, ])
        db.commit()


def dropTestCaseBySuite(suite_id):
    exist = getTestCaseBySuite(suite_id)
    if exist:
        for i in exist:
            dropTestStepByCase(i[0])
        sql = "delete from testCases where suite_id=:suite_id"
        db.execute(sql, [suite_id, ])
        db.commit()



# 直接返回所有节点，不再使用
# def test_treeItems():
#     tree_items = [{"text": "autoTestCase", "id": "root", "state": True, "parent": "#", "type": "root"}]
#     all_category = getAllCategory()
#     for category in all_category:
#         category_id = category[0]
#         category_name = category[1]
#         tree_items.append({"text": category_name, "id": category_id, "parent": "root", "type": "testSuite"})
#         for suite in getTestSuiteByCategory(category_id):
#             suite_id = suite[0]
#             suite_name = suite[2]
#             tree_items.append({"text": suite_name, "id": suite_id, "parent": category_id, "type": "testCase"})
#             for case in getTestCaseBySuite(suite_id):
#                 case_id = case[0]
#                 case_name = case[2]
#                 case_type = case[3]
#                 case_limit = case[4]
#                 case_limit_value = case[5]
#                 case_object = case[6]
#                 tree_items.append({"text": case_name, "id": case_id, "parent": suite_id, "type": "testCondition", "test_type": case_type,
#                                    "test_limit": case_limit, "test_limit_value": case_limit_value, "test_object": case_object})
#     return tree_items


def check_login(func=None):
    def deco(func):
        def wrapper(*args, **kwargs):
            if "user_name" in session and ("user_id" in session or "_user_id" in session):
                return func(*args,**kwargs)
            else:
                ajax_flag = request.headers.get('X-Requested-With', False)
                if '_flashes' not in session or len(session['_flashes']) == 0:
                    flash("您的登录已过期，请重新登录！")
                if ajax_flag:
                    return jsonify({'resultCode': 302, 'result': url_for("login._login")})
                return redirect(url_for("login._login"))
        wrapper.__name__ = func.__name__
        return wrapper
    return deco if not func else deco(func)
