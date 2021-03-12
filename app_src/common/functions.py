__author__ = 'Administrator'
import cx_Oracle
import pymysql
import time
import random
import base64
import hashlib
import sys
import re
import os
import xmltodict
import paramiko
import app_src.lib.cx_gmdb as cx_gmdb
import requests
import pygal
import urllib.request
from selenium import webdriver
from conf import resultPostMessage, resultPostPic, robot_url, is_commit, is_debug, LocalSystem
from app_src.common.common import getStepById, crID, db, local_host, local_url, getAllItemCount
from app_src.main.functions import getStepParamByUser
from werkzeug.security import check_password_hash
from flask import json, render_template
from collections import OrderedDict
# from multiprocessing import Process, freeze_support # 多进程不好打包....
import threading
import subprocess

if LocalSystem == 'win':
    from app_src.common.sikuli_func import *


def getSysdate():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def print_green(*args):
    print("\033[1;32;40m", *args, "\033[0m")


def print_red(*args):
    print("\033[1;31;40m", *args, "\033[0m")


# def get_yaml_data(file_name, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
# current_path = os.path.abspath(".")
# yaml_file = os.path.join(current_path, "testCaseCategory/%s.yml" % file_name)
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

# {#  type, Name, Index, testResult, len(child), len(child_pass), len(child_failed), len(child_error)   #}
# {#  type, Name, Index, testResult, testStepDetail#}

def getTestResult(allTestResult):
    step_list = []
    case_list = []
    suite_list = []
    case_index = 0
    step_index = 0

    len_pass = 0
    len_fail = 0
    len_error = 0

    state_case = 0
    state_case_all = 0
    state_suite = 0
    state_suite_all = 0
    for i in allTestResult:
        if i.type == 'testStep':
            if i.result_code == 0:
                len_pass += 1
            elif i.result_code == 1:
                len_fail += 1
            elif i.result_code == 2:
                len_error += 1
            state_case += i.result_code
            state_case_all += 1
            step_index += 1
            step_list.append({"name": i.name, "Index": step_index, "type": "testStep", "testResult": i.result_code,
                              "detail": i.result_reason, "details": [i.elapse, 1, i.result_code, i.result_reason]})
        elif i.type == 'testCase':
            state_suite += state_case
            state_suite_all += state_case_all
            case_index += 1
            case_list.append({"name": i.name, "Index": case_index, "type": "testCase", "testResult": state_case,
                              "len_child": state_case_all, "len_child_pass": len_pass, "len_child_fail": len_fail,
                              "len_child_error": len_error, "children": step_list,
                              "details": [i.elapse, state_case_all, i.result_code, i.result_reason]})
            state_case = 0
            state_case_all = 0
            step_index = 0
            len_pass = 0
            len_fail = 0
            len_error = 0
            step_list = []
        elif i.type == 'testSuite':
            suite_list.append({"name": i.name, "type": "testSuite",
                               "details": [i.elapse, state_suite_all, state_suite, i.result_reason],
                               "children": case_list})
            state_suite = 0
            state_suite_all = 0
            case_index = 0
            case_list = []
    return suite_list


def makeLinuxResult(allTestResult):
    def print_color(kwargs):
        if kwargs['type'] == 'testSuite':
            if kwargs['details'][2] == 0:
                print_green(kwargs['name'], '(elapse[%.2f],failed[%d],pass[%d])' % (
                    kwargs['details'][0], kwargs['details'][2], kwargs['details'][1] - kwargs['details'][2]), ':')
            else:
                print_red(kwargs['name'], '(elapse[%.2f],failed[%d],pass[%d])' % (
                    kwargs['details'][0], kwargs['details'][2], kwargs['details'][1] - kwargs['details'][2]), ':')
        elif kwargs['type'] == 'testCase':
            if kwargs['details'][2] == 0:
                print_green('       ', kwargs['name'], '(elapse[%.2f],failed[%d],pass[%d])' % (
                    kwargs['details'][0], kwargs['details'][2], kwargs['details'][1] - kwargs['details'][2]), ':')
            else:
                print_red('       ', kwargs['name'], '(elapse[%.2f],failed[%d],pass[%d])' % (
                    kwargs['details'][0], kwargs['details'][2], kwargs['details'][1] - kwargs['details'][2]), ':')
        elif kwargs['type'] == 'testStep':
            if kwargs['details'][2] == 0:
                print_green('              ', kwargs['name'], '(elapse[%.2f])' % kwargs['details'][0], ':',
                            kwargs['details'][3])
            else:
                print_red('              ', kwargs['name'], '(elapse[%.2f])' % kwargs['details'][0], ':',
                          kwargs['details'][3])

    test_result = getTestResult(allTestResult)
    # print(test_result)
    for i in test_result:
        print_color(i)
        for case in i['children']:
            print_color(case)
            for step in case['children']:
                print_color(step)


def makeHtmlResult(allTestResult):
    test_result = getTestResult(allTestResult)
    return test_result


def checkUser(user_id, password):
    sql = "select user_id, user_password from user where user_id=:user_id"
    res = db.execute(sql, [user_id, ]).fetchone()
    if len(res) == 0:
        return False, "user id is not exists!"
    if check_password_hash(res[1], password):
        return True, "authentication success!"
    return False, "authentication failed!"


def html2pic(url):
    localPath = 'tempFile/'
    driver = webdriver.PhantomJS()
    # url = "http://127.0.0.1:2345/run/showResult?runCaseId=yGTknDzvbPt"
    driver.get(url)
    pic_name = localPath + crID(15) + '.png'
    # driver.maximize_window()
    driver.set_window_size(800, 20)
    driver.save_screenshot(pic_name)
    with open(pic_name, 'rb') as file:  # 转换图片成base64格式
        data = file.read()
        encodestr = base64.b64encode(data)
        image_data = str(encodestr, 'utf-8')
    with open(pic_name, 'rb') as file:  # 图片的MD5值
        md = hashlib.md5()
        md.update(file.read())
        image_md5 = md.hexdigest()
    os.remove(pic_name)
    return image_data, image_md5


def sendRobotMessage(url, pic, picmd5):
    message = resultPostMessage
    message['markdown']['content'] = message['markdown']['content'] % (url, url)
    picture = resultPostPic
    picture['image']['base64'] = pic
    picture['image']['md5'] = picmd5

    r1 = requests.post(robot_url, data=json.dumps(message))
    # print(robot_url, json.dumps(message))
    print(r1.text)

    r2 = requests.post(robot_url, data=json.dumps(picture))
    # print(robot_url, json.dumps(picture))
    print(r2.text)


def sendOutTestResult(sendMethod, runCaseId):
    if sendMethod == 'robot':
        resultLink = '%s/run/showResult?runCaseId=' % local_url + runCaseId
    elif sendMethod == 'report':
        resultLink = "%s/run/report?runCaseId=" % local_url + runCaseId
    else:
        return
    pic, picmd5 = html2pic(resultLink)
    sendRobotMessage(resultLink, pic, picmd5)


def runServer(user_id, testSuiteId, runCaseId, isSendOut=0):
    allTestResult = []
    allTestParam = setVariable(getStepParamByUser(user_id, testSuiteId, "All")[0])
    user_suites = TestSuites(user_id, suite_id=testSuiteId, runCaseId=runCaseId, allTestParam=allTestParam,
                             allTestResult=allTestResult)
    user_suites.start()
    runResult = makeHtmlResult(allTestResult)
    sql1 = "update runTestCaseLog set runResult=:v1, endTime=datetime(CURRENT_TIMESTAMP,'localtime') where runCaseId=:v2"
    db.execute(sql1, [json.dumps(runResult), runCaseId])
    db.commit()
    if isSendOut == 1:
        sendOutTestResult('robot', runCaseId)
    if isSendOut == 2:
        if runResult[0].get('details', [-1, -1, -1])[2] != 0:
            sendOutTestResult('robot', runCaseId)


def setNewTask(csrf_token, testSuiteId, user_id, runCaseId, isSendOut=0):
    sql = "insert into runTestCaseLog VALUES (:csrf_token, :testSuiteId, datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime'), :user_id, :allItemCount, 0, :runCaseId, '')"
    allItemCount = getAllItemCount(testSuiteId)
    db.execute(sql, [csrf_token, testSuiteId, user_id, allItemCount, runCaseId])
    db.commit()
    print("new task start!!")
    # 多线程windows不好打包......
    # p1 = Process(target=runServer, args=(user_id, testSuiteId, runCaseId, isSendOut))
    p1 = threading.Thread(target=runServer, args=(user_id, testSuiteId, runCaseId, isSendOut))
    p1.start()


class TestResult:
    def __init__(self, cls, is_run=1):
        self.cls = cls
        self.is_run = is_run
        self.runCaseId = self.cls.runCaseId or 0
        self.name = 'test result'
        self.type = 'test result'
        self.elapse = 0
        self.run()

    def run(self):
        start_time = time.time()
        self.cls.run(self.is_run)
        end_time = time.time()
        self.elapse = end_time - start_time
        self.name = self.cls.name
        self.type = self.cls.type
        self.result_code = self.cls.result_code
        self.result_reason = self.cls.result_desc
        if self.cls.type == 'testCase':
            self.uid = self.cls.case_id
        elif self.cls.type == 'testStep':
            self.uid = self.cls.step_id
        elif self.cls.type == 'testSuite':
            self.uid = self.cls.suite_id
        if self.runCaseId:
            sql = "update runTestCaseLog set nowItemCount=nowItemCount+1, endTime=datetime(CURRENT_TIMESTAMP,'localtime') where runCaseId=:v1"
            db.execute(sql, [self.runCaseId, ])
            db.commit()


class param:
    def __init__(self, name, type, value=""):
        self.name = name
        self.type = type
        self.value = value

    def __repr__(self):
        return self.value


def setVariable(variables):
    allTestParam = []
    for i in variables:
        allTestParam.append(param(i[1], i[2], i[3]))
    return allTestParam


def getVariable(allTestParam, variable):
    try:
        for i in allTestParam:
            if i.name == variable:
                return i
        return param('', '', '')
    except:
        return param('', '', '')


def replaceVariable(allTestParam, text):
    if '$(' in text:
        for i in allTestParam:
            partA = '$(' + i.name + ')'
            partB = ""
            if type(i.value) == str:
                partB = i.value
            elif type(i.value) == list:
                partB = ""
                length_value = len(i.value)
                line_no = 0
                for j in i.value:
                    partB += ','.join(str(s) for s in j)
                    line_no += 1
                    if line_no != length_value:
                        partB += '\n'
            else:
                print(type(i.type), 'not replaceVariable')
            text = text.replace(partA, partB)
        text = text.replace("$(random)", crID(8))
        text = text.replace("$(sysdate)", getSysdate())
    return text


class TestSuites:
    def __init__(self, user_id='', suite_name='', suite_id=0, runCaseId=0, allTestParam=[], allTestResult=[]):
        self.user_id = user_id
        self.suite_name = suite_name
        self.suite_id = suite_id
        self.runCaseId = runCaseId
        self.name = self.suite_name
        self.type = 'testSuite'
        self.result_code = 0
        self.result_desc = ""
        self.allTestParam = allTestParam
        self.allTestResult = allTestResult

    def checkUserSuites(self):
        sql = "select suite_id from testSuites where user_id=:user_id and suite_description=:suite_name"
        res = db.execute(sql, [self.user_id, self.suite_name]).fetchone()
        if not res:
            return False
        else:
            return res[0]

    def __getTestCases(self):
        sql = "select * from testCases where suite_id=:suite_id ORDER BY position"
        res = db.execute(sql, [self.suite_id, ]).fetchall()
        if res:
            repeat_list = []
            for i in res:
                for j in range(i[4]):
                    repeat_list.append((i[0], j + 1))
            return repeat_list
        return res

    def run(self, is_run=1):
        if not self.suite_id:
            self.suite_id = self.checkUserSuites()
        if not self.suite_id:
            self.result_code = 1
            self.result_desc = "do not get suite_id!"
            return [TestResult(self), ]
        allTestCases = self.__getTestCases()
        for case in allTestCases:
            self.allTestResult.append(
                TestResult(TestCases(case[0], self.runCaseId, case[1], self.allTestParam, self.allTestResult)))

    def start(self):
        self.allTestResult.append(TestResult(self))


class TestCases:
    def __init__(self, case_id, runCaseId=0, repeat_time=0, allTestParam=[], allTestResult=[]):
        self.case_id = case_id
        self.runCaseId = runCaseId
        self.repeat_time = repeat_time
        self.type = 'testCase'
        self.result_code = 0
        self.result_desc = ""
        self.allTestParam = allTestParam
        self.allTestResult = allTestResult

    def __getCaseName(self):
        sql = "select case_description from testCases where case_id=:v1"
        res = db.execute(sql, [self.case_id, ]).fetchone()
        self.name = "(%d)" % int(self.repeat_time) + res[0]
        return self.name

    def __getTestSteps(self):
        sql = "select * from testSteps WHERE case_id=:case_id ORDER BY position"
        res = db.execute(sql, [self.case_id, ]).fetchall()
        return res

    @staticmethod
    def getStepClass(step_data, runCaseId, allTestParam):
        if step_data[1] == 'testStepDbExecute':
            return TestStepDbExecute(step_data[0], runCaseId, allTestParam)
        elif step_data[1] == 'testStepFile':
            return TestStepFile(step_data[0], runCaseId, allTestParam)
        elif step_data[1] == 'testStepDbCheck':
            return TestStepDbCheck(step_data[0], runCaseId, allTestParam)
        elif step_data[1] == 'testStepWebInterface':
            return TestStepWebInterface(step_data[0], runCaseId, allTestParam)
        elif step_data[1] == 'testStepCmd':
            return TestStepCmd(step_data[0], runCaseId, allTestParam)
        elif step_data[1] == 'testStepReport':
            return TestStepReport(step_data[0], runCaseId, allTestParam)
        elif step_data[1] == 'testStepGui':
            return TestStepGui(step_data[0], runCaseId, allTestParam)
        elif step_data[1] == 'function':
            return TestStepFunction(step_data[0], runCaseId, allTestParam)
        else:
            return

    def run(self, is_run=1):
        self.case_name = self.__getCaseName()
        allTestStep = self.__getTestSteps()
        step_flag = 1  # if before steps failed, remains will be cancel
        for step in allTestStep:
            # print(step_flag)
            if step_flag == 1:
                step_result = TestResult(self.getStepClass(step, self.runCaseId, self.allTestParam))
                if step_result.result_code != 0:
                    step_flag = 0
                else:
                    step_flag = 1
            else:
                step_result = TestResult(self.getStepClass(step, self.runCaseId, self.allTestParam), is_run=0)
            self.allTestResult.append(step_result)


class TestStep:
    def __init__(self, step_id, runCaseId, allTestParam):
        self.step_id = step_id
        self.runCaseId = runCaseId
        self.type = 'testStep'
        self.result_code = 0
        self.result_desc = "success!"
        self.allTestParam = allTestParam
        self.name = self.__getStepName()
        self.localPath = 'tempFile/'
        self.details = None
        # TestStepGui需要的全局变量
        if not hasattr(self, 'GUI'):
            self.GUI = {}
        if not hasattr(self, 'tempFileList'):
            self.tempFileList = []

    def __getStepName(self):
        sql = "select step_name from testSteps where step_id=:v1"
        res = db.execute(sql, [self.step_id, ]).fetchone()
        if res:
            self.name = res[0]
        else:
            return ""
        return self.name

    def getStepDetail(self):
        if not self.details:
            self.details = getStepById(self.step_id)

    def setError(self, desc, code=2, type=None):
        self.result_code = code
        if type == 'append':
            self.result_desc += '\n' + str(desc).replace('\n', '')
        else:
            self.result_desc = str(desc).replace('\n', '')

    def getHostInfo(self, hostInfo):
        try:
            symbol = "[/@:]+"
            result = re.split(symbol, hostInfo)
            return [x for x in result if x]
            #     z = hostInfo.split('@')
            #     a = z[0].split('/')
            #     b = z[1].split('/')
            #     c = b[0].split(':')
            #     return c[0], a[0], a[1], b[1], c[1]
            # else:
            #     b = hostInfo.split('/')
            #     c = b[1].split('@')
            #     return b[0], c[0], c[1]
        except Exception as e:
            print('hostInfo analysis error: %s' % hostInfo)
            print(e)
            return -1

    def getDbConnect(self, db_type, db_entry):
        if db_type == 'db_oracle':
            try:
                connect = cx_Oracle.connect(db_entry)
                return 0, connect
            except Exception as e:
                print('oracle connect error: %s' % db_entry)
                print(e)
                return -1, e
        elif db_type == 'db_gmdb':
            try:
                hostInfo = self.getHostInfo(db_entry)
                if len(hostInfo) != 3:
                    return -1, 'connect str analysis error: %s' % db_entry
                gmdb_connect = cx_gmdb.connect(hostInfo[0], hostInfo[1], hostInfo[2])
                if gmdb_connect.conn == 0:
                    self.setError('gmdb not connect...' + '<br>')
                    return -1, 'gmdb connect error'
                else:
                    return 0, gmdb_connect
            except Exception as e:
                print('gmdb connect error: %s' % db_entry)
                print(e)
                return -1, e
        elif db_type == 'db_mysql':
            try:
                hostInfo = self.getHostInfo(db_entry)
                if len(hostInfo) != 5:
                    return -1, 'connect str analysis error: %s' % db_entry
                # admin/Admin_01@172.31.69.142:3310/admin
                # conn = pymysql.connect(host=“你的数据库地址”, user=“用户名”,password=“密码”,database=“数据库名”,charset=“utf8”)
                mysql_connect = pymysql.connect(hostInfo[2], hostInfo[0], hostInfo[1], hostInfo[4], int(hostInfo[3]))
                return 0, mysql_connect
            except Exception as e:
                print('mysql connect error: %s' % db_entry)
                print(e)
                return -1, e
        else:
            return -1, 'this db_type is not prepared!'

    def run(self, is_run):
        pass


class TestStepSingle(TestStep):
    # 要考虑threading, 单例
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(TestStepSingle, "_instance"):
            with TestStepSingle._instance_lock:
                if not hasattr(TestStepSingle, "_instance"):
                    TestStepSingle._instance = super().__new__(cls)
        return TestStepSingle._instance


class TestStepFunction(TestStep):
    def getFuncDetail(self):
        sql = "select function_id, detail_name, position, ability_id, ability_param_1, ability_param_2, ability_param_3, " \
              "ability_param_4, ability_param_5 from testFunctionDetail where function_id = :v1 order by position"
        res = db.execute(sql, [self.step_id[:16]]).fetchall()
        return res

    def run(self, is_run):
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        funcDetail = self.getFuncDetail()
        for i in funcDetail:
            subFunc = TestCases.getStepClass([i[0], i[3]], self.runCaseId, self.allTestParam)
            subFunc.details = [i[0], i[3], i[4], i[5], i[6], i[7], i[8], 0, i[1], i[2]]
            subFunc.run(is_run)
            if subFunc.result_code != 0:
                self.setError(subFunc.result_desc, subFunc.result_code)
                return


class TestStepDbExecute(TestStep):
    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = getVariable(self.allTestParam, self.details[2]).value
        self.db_type = getVariable(self.allTestParam, self.details[2]).type
        self.param2 = getVariable(self.allTestParam, self.details[3])
        self.param3 = self.details[4].replace("；", ";")

        print("start db execute!")
        # print(self.db_type, self.param1)
        connect_flag, connect = self.getDbConnect(self.db_type, self.param1)
        if connect_flag == -1:
            self.setError(str(connect))
            return
        cursor = connect.cursor()

        # print(allTestParam)
        temp_variable = self.param2

        all_sqls = self.param3.split(';')
        for sql in all_sqls:
            if len(sql.strip()) != 0:
                if "$(sleep" in sql:
                    sleep_time = sql.strip()[7:-1]
                    try:
                        sleep_seconds = int(sleep_time)
                        if 0 < sleep_seconds < 30:
                            time.sleep(sleep_seconds)
                    except Exception as e:
                        print('sleep error', e)
                    continue
                # print(replaceVariable(sql))
                try:
                    cursor.execute(replaceVariable(self.allTestParam, sql))
                    if is_commit:
                        connect.commit()
                except Exception as e:
                    self.setError(
                        str(e) + "<br>original sql is:<br>" + sql + "<br>trans sql is:<br>" + replaceVariable(
                            self.allTestParam, sql))
                    return
                if temp_variable:
                    try:
                        temp_variable.value = cursor.fetchmany(20)
                    except Exception as e:
                        print(e)
                if is_debug:
                    self.result_desc += '<br>......<br>' + TestStepDbCheck.oraRes2str(temp_variable.value)

        # print(temp_variable.value)
        connect.close()


class TestStepDbCheck(TestStep):
    @staticmethod
    def oraRes2str(data):
        res = ""
        for j in data:
            res += ','.join(str(s) for s in j)
            res += '\n'
        return res

    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = getVariable(self.allTestParam, self.details[2]).value
        self.db_type = getVariable(self.allTestParam, self.details[2]).type
        self.param2 = replaceVariable(self.allTestParam, self.details[3])
        self.param3 = self.details[4]
        self.param4 = int(self.details[5]) or 1
        result = ""
        print("start db check!")

        connect_flag, connect = self.getDbConnect(self.db_type, self.param1)
        if connect_flag == -1:
            self.setError(str(connect))
            return
        cursor = connect.cursor()

        maxRepeatTime = 0
        all_sqls = self.param3.split(';')
        while maxRepeatTime < self.param4:
            for sql in all_sqls:
                if len(sql.strip()) != 0:
                    try:
                        cursor.execute(replaceVariable(self.allTestParam, sql))
                    except Exception as e:
                        self.setError(e)
                        return
                    result = cursor.fetchmany(1000)
            if self.param2.strip() == self.oraRes2str(result).strip():
                connect.close()
                if is_debug:
                    self.result_desc += '<br>......<br>' + TestStepDbCheck.oraRes2str(result)
                return
            maxRepeatTime += 1
            print("finish check for %d times" % maxRepeatTime)
            time.sleep(3)
        if self.param2.strip() != self.oraRes2str(result).strip():
            self.setError("assert Error:<br>expect result is[%s]<br>actual result is[%s]" % (
                self.param2.strip().replace('\n', '<br>'), self.oraRes2str(result).strip().replace('\n', '<br>')))
            connect.close()
            return


class TestStepFile(TestStep):
    def __init__(self, step_id, runCaseId, allTestParam):
        super().__init__(step_id, runCaseId, allTestParam)

    @staticmethod
    def TransFile(fileName, localpath, remotepath, ip, user, password, port=22):
        # ftp貌似有些主机不能用。。。。。。。
        # ftp = FTP()  # 设置变量
        # ftp.set_debuglevel(0)  # 打开调试级别2，显示详细信息
        # ftp.connect(ip, port)  # 连接的ftp sever和端口
        # ftp.login(user, password)  # 连接的用户名，密码
        #
        # ftp.cwd(remotepath)  # 更改远程目录
        # # print(fileName)
        # ftp.storbinary('STOR ' + fileName, open(localpath + fileName, 'rb'))  # 上生产需要改路径
        # os.remove(localpath + fileName)  # 上生产需要改路径
        # ftp.quit()
        try:
            # print(ip, port, remotepath, localpath, fileName)
            transport = paramiko.Transport((ip, port))
            transport.connect(username=user, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)  # 如果连接需要密钥，则要加上一个参数，hostkey="密钥"
            if remotepath[-1] != "/":
                remotepath = remotepath + '/'
            sftp.put(localpath + fileName, remotepath + fileName)
            transport.close()  # 关闭连接
        except Exception as e:
            raise e
        finally:
            os.remove(localpath + fileName)

    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = getVariable(self.allTestParam, self.details[2]).value
        self.param2 = replaceVariable(self.allTestParam, self.details[3])
        self.param3 = replaceVariable(self.allTestParam, self.details[4])
        self.param4 = replaceVariable(self.allTestParam, self.details[5])

        print("start file server")
        if self.param1 == "":
            self.setError("host detail not configured! ")
            return

        if self.param2 == "":
            self.param2 = 'temp' + crID(8)
        if len(self.param3) > 0 and self.param3[-1] != '/':
            self.param3 = self.param3 + '/'

        if self.param1 in ('127.0.0.1', 'localhost'):
            if not os.path.exists(self.param3):
                os.makedirs(self.param3)
            with open(self.param3 + self.param2, 'w', encoding='utf-8') as f:
                f.write(self.param4)

        else:
            hostInfo = self.getHostInfo(self.param1)
            if len(hostInfo) == 1:
                self.setError("host not configured! [user/password@host_ip] is required, but got [%s]" % self.param1)
                return
            if len(hostInfo) == 3:
                user, password, ip = hostInfo
                port = 0
            elif len(hostInfo) == 4:
                user, password, ip, port = hostInfo
            else:
                self.setError("not enough param for login...%s" % str(hostInfo))
                return
            if ip == local_host:
                try:
                    with open(self.param3 + self.param2, 'w', encoding='utf-8') as f:
                        f.write(self.param4)
                    return
                except Exception as e:
                    self.setError("create file error! %s" % str(e))
                    return

            try:
                with open(self.localPath + self.param2, 'w', encoding='utf-8') as f:
                    f.write(self.param4)
                print('create local temp file OK')
            except Exception as e:
                self.setError("create file error! %s" % str(e))
                return

            try:
                if port == 0:
                    self.TransFile(self.param2, self.localPath, self.param3, ip, user, password)
                else:
                    self.TransFile(self.param2, self.localPath, self.param3, ip, user, password, int(port))
            except Exception as e:
                self.setError("trans file error! %s" % str(e))
                return


class TestStepWebInterface(TestStep):
    # @staticmethod
    # def parse(data, element_name):
    #     result = []
    #     temp = data.split(element_name)
    #     if len(temp) == 1:
    #         return ""
    #     if '<' + element_name + '>' not in data:
    #         return ""
    #     for i in range(1, 10, 2):
    #         if i <= len(temp) - 1:
    #             result.append(temp[i][1:-2])
    #     return result[0]

    @staticmethod
    def getRandomSeq():
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        subfix = str(random.randint(0, 1000))
        return now_time + subfix

    @staticmethod
    def CallWebInterface(texturl, postcontent):
        postcontent = postcontent.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        postcontent = postcontent.replace(
            '${=(new java.text.SimpleDateFormat("yyyyMMddHHmmss")).format(new Date())}${=(int)(Math.random()*1000)}',
            TestStepWebInterface.getRandomSeq())
        req = urllib.request.Request(texturl, data=postcontent.encode('utf-8'),
                                     headers={'Content-Type': 'text/xml;charset=UTF-8'})
        print('---------------------', texturl, '---------------------')
        print('---------------------', postcontent, '---------------------')
        msg = urllib.request.urlopen(req)
        lines = msg.read()
        lines = lines.decode('utf-8')
        print(lines)
        return lines

    def json2list(self, li, dic):
        if type(dic) == dict or type(dic) == OrderedDict:
            for key, value in dic.items():
                # print(key, value)
                li.append({key: value})
                self.json2list(li, value)
        if type(dic) == list:
            for i in dic:
                # print(i)
                self.json2list(li, i)

    def _checkAssert(self, data, predict):
        try:
            if predict[:6] == 'haskey':
                temp_list = []
                temp = predict[7:-1].split(',')
                # print(temp)
                key = temp[0]
                value = temp[1]
                self.json2list(temp_list, data)
                if {key: value} in temp_list:
                    return True
                else:
                    return False

            partner = '\[.*?\]'
            prefix = ""
            suffix = ""
            split_flag = ''
            split_flags = ['=', '<', '>', '>=', '<=', '!=']
            for split_flag in split_flags:
                temp = predict.split(split_flag)
                if len(temp) == 2:
                    prefix = temp[0].strip()
                    suffix = temp[1].strip()
                    break
            if not split_flag:
                return False
            if prefix:
                # print(prefix, split_flag, suffix)
                res = re.findall(partner, prefix)
                for i in res:
                    try:
                        i = int(i.replace('[', '').replace(']', ''))
                    except:
                        i = i.replace('[', '').replace(']', '')
                    finally:
                        data = data[i]
                if split_flag == '=':
                    return data == suffix
                elif split_flag == '!=':
                    return data != suffix
                elif split_flag == '<':
                    return data < suffix
                elif split_flag == '>':
                    return data > suffix
                elif split_flag == '<=':
                    return data <= suffix
                elif split_flag == '>=':
                    return data >= suffix
            return False
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!", e, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = replaceVariable(self.allTestParam, self.details[2])
        self.param2 = replaceVariable(self.allTestParam, self.details[3])
        self.param3 = replaceVariable(self.allTestParam, self.details[4])

        print("start web interface!")

        if self.param1 == "" or self.param2 == "":
            self.setError("web url or message body is null")
            return
        try:
            result = self.CallWebInterface(self.param1, self.param2)
            self.allTestParam.append(param('sys_post_url', "string", self.param1))
            self.allTestParam.append(param('sys_post_body', "string", self.param2))
            self.allTestParam.append(param('sys_post_result', "string", result))
            callResult = xmltodict.parse(result.replace("<?xml version='1.0' encoding='UTF-8'?>", ''))
            self.allTestParam.append(param('sys_post_result_dict', "string", callResult))
            if len(self.param3) > 0:
                for i in self.param3.split('\n'):
                    if i.strip() != '':
                        try:
                            assert self._checkAssert(callResult, i.strip())
                        except Exception as e:
                            print('assert error: ', e)
                            self.setError("assert Error!<br>assert:%s<br>return code:[%s]" % (
                                i.strip(), str(json.dumps(callResult))))
                            return
        except Exception as e:
            self.setError("call web interface error:[%s]" % e)
            return


class TestStepCmd(TestStep):
    def __init__(self, step_id, runCaseId, allTestParam):
        super().__init__(step_id, runCaseId, allTestParam)
        self.partner = '\$\(.*?\)'

    def cmdTrans(self, actual_cmd, param_cmd):
        expect_result = ""
        res = re.findall(self.partner, actual_cmd)
        param_value_list = param_cmd.split("==")
        for i in range(len(res)):
            if res[i] == '$(output)':
                expect_result = param_value_list[i]
                actual_cmd = actual_cmd.replace("$(output)", "")
            else:
                actual_cmd = actual_cmd.replace(res[i], param_value_list[i])
        return actual_cmd, expect_result

    def _connect(self):
        client = paramiko.SSHClient()

        hostInfo = self.getHostInfo(self.param1)
        if len(hostInfo) == 1:
            return -1, "host not configured! [user/password@host_ip] is required, but got [%s]" % self.param1
        if len(hostInfo) == 3:
            user, password, ip = hostInfo
            port = 22
        elif len(hostInfo) == 4:
            user, password, ip, port = hostInfo
        else:
            return -1, "param not enough! [%s]" % self.param1

        try:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, int(port), username=user, password=password, timeout=20)
        except Exception as e:
            print(e)
            return -1, "host connect error! %s" % str(e)
        return 0, client

    def exec_command(self, client, cmd):
        try:
            stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
            res = ""
            results = stdout.readlines()

            for line in results:
                res += line
            try:
                err = stderr.readlines()
                for line in err:
                    res += line
            except Exception as e:
                return -1, str(e)
            return 0, res.replace("\r\n", "\n")
        except Exception as e:
            return -1, str(e)

    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = getVariable(self.allTestParam, self.details[2]).value
        self.param2 = getVariable(self.allTestParam, self.details[3]).value
        self.param3 = replaceVariable(self.allTestParam, self.details[4])
        self.param4 = self.details[5]
        print("start cmd execute")
        if self.param1 == "":
            self.setError("host detail not configured! ")
            return
        cmd, expect = self.cmdTrans(self.param2, self.param3)
        print('---------------', cmd, '----->', expect, '---------------')
        repeat_time = 0
        result_desc = ""
        connect_code, client = self._connect()
        if connect_code != 0:
            self.setError(client)
            return
        while repeat_time < int(self.param4):
            try:
                result_code, result_desc = self.exec_command(client, cmd)
            except Exception as e:
                self.setError(e)
                return
            if result_code != 0:
                self.setError("execute cmd Error:[%s]" % result_desc)
                return
            if len(expect) == 0:
                return
            elif len(expect) > 0 and result_desc.strip() == expect.strip():
                return
            else:
                repeat_time += 1
                print("finish %d" % repeat_time)
                time.sleep(3)
                continue
        client.close()
        if len(expect) > 0 and result_desc.strip() != expect.strip():
            self.setError("assert Error:<br>expect result is[%s]<br>actual result is[%s]" % (
                expect.strip().replace('\n', '<br>'), result_desc.strip().replace('\n', '<br>')))
            return


class TestStepReport(TestStep):
    def __init__(self, step_id, runCaseId, allTestParam):
        super().__init__(step_id, runCaseId, allTestParam)
        self.funcList = {'bar': self.ChartBar, 'pie': self.ChartPie, 'text': self.ToText, 'table': self.ToTable}
        self.svg_template = '''<div style="width: 50%%"><embed type="image/svg+xml" src= "%s"/></div>'''
        self.part1 = "!\[[\d\D]*?\]\n?\([\d\D]*?\)"
        self.part2 = "\(?.*="
        self.part3 = "!\[.*?\]\n?\("

    def ToText(self, title="", **kwargs):
        return title

    def ToTable(self, title="", colorLine=-1, head="", datas="", value_formatter="", **kwargs):
        html = ""
        if not datas:
            return "not configure datas..."
        datas = [i.split(',') for i in datas.split('\n') if i != ""]
        table_width = len(datas[0])
        if not head:
            head = [i for i in range(table_width)]
        else:
            head = head.split(",")

        tableColors = {-1: "",
                       0: "white",
                       1: "#64f764",  # green
                       2: "yellow",
                       3: "#f54d4d",  # red
                       4: "#7f7fd2"  # blue
                       }

        if title:
            html += "<h2>%s</h2>" % title
        html += '<table><thead><tr>'

        # print("head", head)
        for i in head:
            html += "<th>%s</th>" % str(i)
        html += '</thead><tbody>'
        for i in datas:
            html += "<tr>"
            if colorLine >= 0:
                color = tableColors.get(i[colorLine], "")
                for td in range(table_width):
                    if td == colorLine:
                        continue
                    html += "<td style='background-color:%s'> %s </td>" % (color, i[td])
            else:
                for td in range(table_width):
                    html += "<td> %s </td>" % i[td]
            html += "</tr>"
        html += "</tbody></table>"
        return html

    def ChartBar(self, title="", head="", datas="", value_formatter="%s", **kwargs):
        if not datas:
            return "not configure datas..."
        datas = [i.split(',') for i in datas.split('\n') if i != ""]
        head = head.split(",")
        bar_chart = pygal.Bar()
        bar_chart.title = title

        # print("datas", datas, "head", head)
        data_len = len(datas[0])
        head_len = len(head)

        if head_len > data_len - 1:
            head_len = data_len - 1
        elif head_len < data_len - 1:
            for i in range(data_len - 1 - head_len):
                head.append(i)
        bar_data = []
        for i in range(data_len):
            line = []
            for j in range(len(datas)):
                line.append(datas[j][i])
            bar_data.append(line)
        x_labels = bar_data[0]
        x_datas = []
        try:
            for i in bar_data[1:]:
                x_datas.append([int(j) for j in i])
        except Exception as e:
            return "x_datas exists non-number! "
        bar_chart.x_labels = x_labels
        chart_data = [[head[i], x_datas[i]] for i in range(head_len)]
        for data in chart_data:
            bar_chart.add(data[0], data[1])
        if value_formatter:
            bar_chart.value_formatter = lambda x: value_formatter % x if x is not None else ' '  # '%.2f%%'
        return self.svg_template % bar_chart.render_data_uri()

    def ChartPie(self, title="", datas="", value_formatter="", **kwargs):
        if not datas:
            return "not configure datas..."
        datas = [i.split(',') for i in datas.split('\n') if i != ""]
        pie_chart = pygal.Pie()
        pie_chart.title = title
        try:
            for data in datas:
                pie_chart.add(data[0], int(data[1]))
            if value_formatter:
                pie_chart.value_formatter = lambda x: value_formatter % x if x is not None else ' '  # '%.2f%%'
            return self.svg_template % pie_chart.render_data_uri()
        except Exception as e:
            return str("[%s]:%s" % (str(data), e))

    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = replaceVariable(self.allTestParam, self.details[2])
        self.param2 = replaceVariable(self.allTestParam, self.details[3])

        md_data = self.param2

        all_svgs = re.findall(self.part1, self.param2.strip())
        for i in all_svgs:
            items = {}
            svg = re.findall(self.part3, i)
            if len(svg) > 0:
                svg_params = i[:-1].replace(svg[0], "").split(';')
                title = svg[0].replace("![", "").replace("]", "").replace("(", "")
            else:
                title = "[%s] configured error!" % i
                md_data = md_data.replace(i, title)
                continue
            for param in svg_params:
                temp = param.split("=")
                if len(temp) == 2:
                    items[temp[0].strip().lower()] = temp[1].strip()
            func = self.funcList[items.get("type", "text")]
            try:
                res = func(title=title, **items)
            except Exception as e:
                print(e)
                res = "<div><font color='red'>section create error! %s</font></div>" % e
            md_data = md_data.replace(i, res)
            print("----------------------")
        runReportId = crID(16)
        db.execute("insert into testReports values (:runCaseId, :robot_url, :sysdate, :runResult)",
                   [runReportId, self.param1, getSysdate(), md_data])
        self.result_desc = "<a href='%s/run/report?runCaseId=%s'>report</a>" % (local_url, runReportId)
        db.commit()


class TestStepGui(TestStepSingle):
    def __init__(self, step_id, runCaseId, allTestParam):
        super().__init__(step_id, runCaseId, allTestParam)
        self.functions = {'environment': self.__funcEnvironment, 'openApp': self.__funcOpenApp,
                          'wait': self.__funcWait, 'input': self.__funcInput, 'click': self.__funcClick,
                          'closeApp': self.__funcCloseApp}
        self.Keys = {'ENTER': Key.ENTER, 'TAB': Key.TAB, 'ESC': Key.ESC, 'BACKSPACE': Key.BACKSPACE,
                     'DELETE': Key.DELETE, 'INSERT': Key.INSERT, 'SPACE': Key.SPACE, 'HOME': Key.HOME,
                     'END': Key.END, 'LEFT': Key.LEFT, 'RIGHT': Key.RIGHT, 'DOWN': Key.DOWN,
                     'UP': Key.UP, 'PAGE_DOWN': Key.PAGE_DOWN, 'PAGE_UP': Key.PAGE_UP
                     }

    def __createTempPic(self, picSrc):
        if ',' not in picSrc:
            self.setError("The image format error!, please contact the administrator!")
            return 1, ""
        picType, picInfo = picSrc.split(',', 1)
        if picType != "data:image/png;base64":
            self.setError("The image format is not Base64, please contact the administrator!")
            return 1, ""
        else:
            picName = crID(10) + '.png'
            picData = base64.b64decode(picInfo)
            with open(pic_path + picName, "wb") as f:
                f.write(picData)
            self.tempFileList.append(picName)
            return 0, picName

    def __dropTempPic(self):
        for file in self.tempFileList:
            # print("os.remove(" + pic_path + file + ")")
            os.remove(pic_path + file)
        self.tempFileList = []

    def __propertyPattern(self, picSrc, x, y):
        res, picName = self.__createTempPic(picSrc)
        if res:
            return 1, ""
        elif x == 0 and y == 0:
            return 0, picName
        else:
            return 0, Pattern(picName).targetOffset(x, y)

    def __funcEnvironment(self, *args):
        try:
            envName = args[0]
            envValue = args[4]
            os.environ[envName] = envValue
            return
        except Exception as e:
            if args[5]:
                return
            else:
                self.setError(e)
                return 1

    def __funcOpenApp(self, *args):
        try:
            self.GUI[args[4]] = App(args[4])
            execCmdPath = re.split(r'(\\|/|\s)', args[4])
            # os.chdir("".join(execCmdPath[:-2]))
            # os.system(args[4])
            subprocess.Popen(args[4], cwd="".join(execCmdPath[:-2]))
            return
        except Exception as e:
            if args[5]:
                return
            else:
                self.setError(e)
                return 1

    def __funcWait(self, *args):
        try:
            if args[4]:
                try:
                    wait_time = float(args[4])
                except:
                    wait_time = 5.0
            else:
                wait_time = 5.0
            if args[3]:
                res, pic_name = self.__createTempPic(args[3])
                if res:
                    return 1
                else:
                    wait(pic_name, wait_time)
                    return
            else:
                wait(wait_time)
                return
        except Exception as e:
            if args[5]:
                return
            else:
                self.setError(e)
                return 1

    def __funcInput(self, *args):
        try:
            if args[3]:
                res, pic_name = self.__propertyPattern(args[3], args[1], args[2])
                type_in(pic_name, "")
                if res:
                    return 1
            if args[4]:
                if "$" in args[4]:
                    templist = args[4].split('$')
                    for i in templist:
                        if i in self.Keys.keys():
                            type_in(self.Keys[i])
                        else:
                            paste(i)
                else:
                    paste(args[4])
            return
        except Exception as e:
            if args[5]:
                return
            else:
                self.setError(e)
                return 1

    def __funcClick(self, *args):
        try:
            if args[3]:
                res, pic_name = self.__propertyPattern(args[3], args[1], args[2])
                if res:
                    return 1
                else:
                    click(pic_name)
                    return
            else:
                self.setError("the click position is not support!")
                return 1
        except Exception as e:
            if args[5]:
                return
            else:
                self.setError(e)
                return 1

    def __funcCloseApp(self, *args):
        try:
            if args[4]:
                self.GUI[args[4]].close()
            else:
                for gui in self.GUI.values():
                    gui.close()
            return
        except Exception as e:
            if args[5]:
                return
            else:
                self.setError(e)
                return 1

    def __getGuiParams(self):
        sql = "select * from test_GUI where step_id = :V1"
        res = db.execute(sql, [self.step_id]).fetchall()
        return res

    def run(self, is_run):
        if LocalSystem != 'win':
            self.setError("当前系统环境不匹配！此功能只能在windows环境执行！")
            return
        if not JAVA_ENV_PASS:
            self.setError("当前系统java环境异常，可能JDK_HOME未找到，建议安装JAVA11！")
            return
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        all_params = self.__getGuiParams()
        start_num = 0
        for i in all_params:
            start_num += 1
            print('start gui %d' % start_num)
            func = self.functions[i[2]]
            param_value = replaceVariable(self.allTestParam, i[9])
            res = func(i[3], i[6], i[7], i[8], param_value, i[10])  # param_name, xo, yo, picsrc, param_value, is_pass
            if res:
                self.setError('error line: %d' % start_num, type='append')
                print("get error, clean temp file!")
                self.__dropTempPic()
                return

        print('execute over!')
        self.__dropTempPic()


