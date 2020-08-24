__author__ = 'Administrator'
import cx_Oracle
import time
import random
import sys
import os
from ftplib import FTP
import urllib.request
from app.common.common import getStepById, crID, db, local_host
from app.main.functions import getStepParamByUser
from werkzeug.security import check_password_hash


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

def getTestResult():
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


def makeLinuxResult():
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

    test_result = getTestResult()
    # print(test_result)
    for i in test_result:
        print_color(i)
        for case in i['children']:
            print_color(case)
            for step in case['children']:
                print_color(step)


def makeHtmlResult():
    test_result = getTestResult()
    return test_result


def checkUser(user_id, password):
    sql = "select user_id, user_password from user where user_id=:user_id"
    res = db.execute(sql, [user_id, ]).fetchone()
    if len(res) == 0:
        return False, "user id is not exists!"
    if check_password_hash(res[1], password):
        setVariable(getStepParamByUser(user_id, "All")[0])
        return True, "authentication success!"
    return False, "authentication failed!"


class TestResult:
    def __init__(self, cls, parent_id, is_run=1):
        self.cls = cls
        self.parent_id = parent_id
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
        print('sfd', self.runCaseId)
        if self.runCaseId:
            sql = "update runTestCaseLog set nowItemCount=nowItemCount+1, endTime=datetime(CURRENT_TIMESTAMP,'localtime') where runCaseId=:v1"
            db.execute(sql, [self.runCaseId, ])
            db.commit()


allTestResult = []
allTestParam = []


class param:
    def __init__(self, name, type, value=""):
        self.name = name
        self.type = type
        self.value = value

    def __repr__(self):
        return self.value


def setVariable(variables):
    for i in variables:
        allTestParam.append(param(i[1], i[2], i[3]))


def getVariable(variable):
    try:
        for i in allTestParam:
            if i.name == variable:
                return i
    except:
        return ""


def replaceVariable(text):
    if '$(' in text:
        for i in allTestParam:
            partA = '$(' + i.name + ')'
            partB = ""
            if type(i.value) == str:
                partB = i.value
            elif type(i.value) == list:
                partB = ""
                for j in i.value:
                    partB += ','.join(str(s) for s in j)
                    partB += '\n'
            else:
                print(type(i.type), 'not replaceVariable')
            text = text.replace(partA, partB)
    return text


class TestSuites:
    def __init__(self, user_id, suite_name='', suite_id=0, runCaseId=0):
        self.user_id = user_id
        self.suite_name = suite_name
        self.suite_id = suite_id
        self.runCaseId = runCaseId
        self.name = self.suite_name
        self.type = 'testSuite'
        self.result_code = 0
        self.result_desc = ""

    def checkUserSuites(self):
        sql = "select * from testSuites where user_id=:user_id and suite_description=:suite_name"
        res = db.execute(sql, [self.user_id, self.suite_name]).fetchone()
        if not res:
            return False
        else:
            return res[0]

    def __getTestCases(self):
        sql = "select * from testCases where suite_id=:suite_id ORDER BY position"
        res = db.execute(sql, [self.suite_id, ]).fetchall()
        return res


    def run(self, is_run):
        if not self.suite_id:
            self.suite_id = self.checkUserSuites()
        if not self.suite_id:
            self.result_code = 1
            self.result_desc = "do not get suite_id!"
            return [TestResult(self, ''), ]
        allTestCases = self.__getTestCases()
        allTestResult.extend([TestResult(TestCases(case[0], self.runCaseId), self.suite_id) for case in allTestCases])


    def start(self):
        allTestResult.append(TestResult(self, 'autoTest'))


class TestCases:
    def __init__(self, case_id, runCaseId=0):
        self.case_id = case_id
        self.runCaseId = runCaseId
        self.type = 'testCase'
        self.result_code = 0
        self.result_desc = ""

    def __getCaseName(self):
        sql = "select case_description from testCases where case_id=:v1"
        res = db.execute(sql, [self.case_id, ]).fetchone()
        self.name = res[0]
        return self.name

    def __getTestSteps(self):
        sql = "select * from testSteps WHERE case_id=:case_id ORDER BY position"
        res = db.execute(sql, [self.case_id, ]).fetchall()
        return res

    @staticmethod
    def __getStepClass(step_data, runCaseId):
        if step_data[1] == 'testStepOracleExecute':
            return TestStepOracleExecute(step_data[0], runCaseId)
        elif step_data[1] == 'testStepFile':
            return TestStepFile(step_data[0], runCaseId)
        elif step_data[1] == 'testStepOracleCheck':
            return TestStepOracleCheck(step_data[0], runCaseId)
        elif step_data[1] == 'testStepWebInterface':
            return TestStepWebInterface(step_data[0], runCaseId)

    def run(self, is_run):
        self.case_name = self.__getCaseName()
        allTestStep = self.__getTestSteps()
        step_flag = 1
        for step in allTestStep:
            # print(step_flag)
            if step_flag == 1:
                step_result = TestResult(self.__getStepClass(step, self.runCaseId), self.case_id)
                if step_result.result_code != 0:
                    step_flag = 0
                else:
                    step_flag = 1
            else:
                step_result = TestResult(self.__getStepClass(step, self.runCaseId), self.case_id, is_run=0)
            allTestResult.append(step_result)


class TestStep:
    def __init__(self, step_id, runCaseId):
        self.step_id = step_id
        self.runCaseId = runCaseId
        self.type = 'testStep'
        self.result_code = 0
        self.result_desc = "success!"
        self.name = self.__getStepName()

    def __getStepName(self):
        sql = "select step_name from testSteps where step_id=:v1"
        res = db.execute(sql, [self.step_id, ]).fetchone()
        self.name = res[0]
        return self.name

    def getStepDetail(self):
        self.details = getStepById(self.step_id)

    def setError(self, desc, code=2):
        self.result_code = code
        self.result_desc = str(desc).replace('\n', '')

    def run(self, is_run):
        pass


class TestStepOracleExecute(TestStep):
    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = getVariable(self.details[2])
        self.param2 = getVariable(self.details[3])
        self.param3 = self.details[4]

        print("start oracle execute!")
        try:
            connect = cx_Oracle.connect(str(self.param1))
            cursor = connect.cursor()
        except Exception as e:
            self.setError(e)
            return
        # print(allTestParam)
        temp_variable = self.param2

        all_sqls = self.param3.split(';')
        for sql in all_sqls:
            if len(sql.strip()) != 0:
                # print(replaceVariable(sql))
                try:
                    cursor.execute(replaceVariable(sql))
                except Exception as e:
                    self.setError(e)
                    return
                if temp_variable:
                    # print(temp_variable.name)
                    temp_variable.value = cursor.fetchmany(1000)
        # print(temp_variable.value)
        connect.close()


class TestStepOracleCheck(TestStep):
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
        self.param1 = getVariable(self.details[2])
        self.param2 = self.details[3]
        self.param3 = self.details[4]
        result = ""

        print("start oracle check!")
        try:
            connect = cx_Oracle.connect(str(self.param1))
            cursor = connect.cursor()
        except Exception as e:
            self.setError(e)
            return

        all_sqls = self.param3.split(';')
        for sql in all_sqls:
            if len(sql.strip()) != 0:
                # print(replaceVariable(sql))
                try:
                    cursor.execute(replaceVariable(sql))
                except Exception as e:
                    self.setError(e)
                    return
                result = cursor.fetchmany(1000)

        if self.param2.strip() != self.oraRes2str(result).strip():
            self.setError("assert Error:<br/>expect result is[%s]<br/>actual result is[%s]" % (
            self.param2.strip(), self.oraRes2str(result).strip()))
            return
        connect.close()


class TestStepFile(TestStep):
    def __init__(self, step_id, runCaseId):
        super().__init__(step_id, runCaseId)
        self.localPath = 'tempFile/'

    @staticmethod
    def getHostInfo(hostInfo):
        b = hostInfo.split('/')
        c = b[1].split('@')
        return b[0], c[0], c[1]

    @staticmethod
    def TransFile(fileName, localpath, remotepath, ip, user, password, port=21):
        ftp = FTP()  # 设置变量
        ftp.set_debuglevel(0)  # 打开调试级别2，显示详细信息
        ftp.connect(ip, port)  # 连接的ftp sever和端口
        ftp.login(user, password)  # 连接的用户名，密码

        ftp.cwd(remotepath)  # 更改远程目录
        # print(fileName)
        ftp.storbinary('STOR ' + fileName, open(localpath + fileName, 'rb'))  # 上生产需要改路径
        os.remove(localpath + fileName)  # 上生产需要改路径
        ftp.quit()

    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = getVariable(self.details[2])
        self.param2 = self.details[3]
        self.param3 = self.details[4]
        self.param4 = self.details[5]

        # print(replaceVariable(self.param4))
        print("start file server")
        if self.param1 == "":
            self.setError("host detail not configured! ")
            return

        if self.param2 == "":
            self.param2 = 'temp' + crID(8)
        if len(self.param3) > 0 and self.param3[-1] != '/':
            self.param3 = self.param3 + '/'

        if self.param1.value in ('127.0.0.1', 'localhost'):
            with open(self.param3 + self.param2, 'w', encoding='utf-8') as f:
                f.write(replaceVariable(self.param4))

        else:
            try:
                user, password, ip = self.getHostInfo(self.param1.value)
            except Exception as e:
                self.setError("host not configured! [user/password@host_ip] is required, but got [%s]" % self.param1)
                return

            if ip == local_host:
                try:
                    with open(self.param3 + self.param2, 'w', encoding='utf-8') as f:
                        f.write(replaceVariable(self.param4))
                    return
                except Exception as e:
                    self.setError("create file error! %s" % str(e))
                    return

            with open(self.localPath + self.param2, 'w', encoding='utf-8') as f:
                f.write(replaceVariable(self.param4))

            try:
                self.TransFile(self.param2, self.localPath, self.param3, ip, user, password)
            except Exception as e:
                self.setError("trans file error! %s" % str(e))
                return


class TestStepWebInterface(TestStep):
    @staticmethod
    def parse(data, element_name):
        result = []
        temp = data.split(element_name)
        if len(temp) == 1:
            return ""
        if '<' + element_name + '>' not in data:
            return ""
        for i in range(1, 10, 2):
            if i <= len(temp) - 1:
                result.append(temp[i][1:-2])
        return result[0]

    @staticmethod
    def getRandomSeq():
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        subfix = str(random.randint(0, 1000))
        return now_time + subfix


    @staticmethod
    def CallWebInterface(texturl, postcontent):
        postcontent = postcontent.replace('${=(new java.text.SimpleDateFormat("yyyyMMddHHmmss")).format(new Date())}${=(int)(Math.random()*1000)}', TestStepWebInterface.getRandomSeq())
        req = urllib.request.Request(texturl, data=postcontent.encode('utf-8'),
                                     headers={'Content-Type': 'text/xml;charset=UTF-8'})
        print('---------------------', req, '---------------------')
        msg = urllib.request.urlopen(req)
        lines = msg.read()
        lines = lines.decode('utf-8')
        print(lines)
        cbs_ResultCode = TestStepWebInterface.parse(lines, 'cbs:ResultCode')
        cbs_ResultDesc = TestStepWebInterface.parse(lines, 'cbs:ResultDesc')
        return [cbs_ResultCode, cbs_ResultDesc]

    def run(self, is_run):
        self.getStepDetail()
        if not is_run:
            self.setError("before step got Error!", 1)
            return
        self.param1 = replaceVariable(self.details[2])
        self.param2 = replaceVariable(self.details[3])

        print("start web interface!")

        if self.param1 == "" or self.param2 == "":
            self.setError("web url or message body is null")
            return
        try:
            result = self.CallWebInterface(self.param1, self.param2)
            if int(result[0]) != 0:
                self.setError("error code:[%s], error desc:[%s]" % (result[0], result[1]))
                return
        except Exception as e:
            self.setError("call web interface error:[%s]" % e)
            return

