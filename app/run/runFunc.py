__author__ = 'Administrator'
from app.common.common import *
from flask import json
from app.common.functions import *
from multiprocessing import Process


def lineBreak(line, length):
    len_line = len(line)
    if len_line <= length:
        return line
    flag = 0
    res = ""
    while 1:
        res += line[flag: flag + length] + '<br/>'
        flag += length
        if flag >= len_line:
            break
    return res


def getAllItemCount(suite_id):
    length = 1
    all_case = getTestCaseBySuite(suite_id)
    length += len(all_case)
    for case in all_case:
        steps = getTestStepByCase(case[0])
        length += len(steps)
    return length


def getRunLogByUser(csrf_token):
    sql = "select a.runCaseId, b.suite_description,a.endTime,(case when round(a.nowItemCount*1.0/a.allItemCount*100) > 100 then 100 when round(a.nowItemCount*1.0/a.allItemCount*100) < 0 then 0 else round(a.nowItemCount*1.0/a.allItemCount*100) end)" \
          "from runTestCaseLog a,testSuites b " \
          "where a.testSuiteId = b.suite_id and csrf_token=:v1"
    res = db.execute(sql, [csrf_token, ]).fetchall()
    return res


def runServer(user_id, testSuiteId, runCaseId):
    setVariable(getStepParamByUser(user_id, "All")[0])
    user_suites = TestSuites(user_id, suite_id=testSuiteId, runCaseId=runCaseId)
    user_suites.start()
    runResult = makeHtmlResult()
    sql1 = "update runTestCaseLog set runResult=:v1, endTime=datetime(CURRENT_TIMESTAMP,'localtime') where runCaseId=:v2"
    db.execute(sql1, [json.dumps(runResult), runCaseId])
    db.commit()


def setNewTask(csrf_token, testSuiteId, user_id, allItemCount, nowItemCount, runCaseId, runResult):
    sql = "insert into runTestCaseLog VALUES (:csrf_token, :testSuiteId, datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime'), :user_id, :allItemCount, :nowItemCount, :runCaseId, :runResult)"
    db.execute(sql, [csrf_token, testSuiteId, user_id, allItemCount, nowItemCount, runCaseId, runResult])
    db.commit()
    print("new task start!")
    p1 = Process(target=runServer, args=(user_id, testSuiteId, runCaseId))
    p1.start()
