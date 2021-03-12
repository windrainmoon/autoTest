from app_src.common.common import getUserBySuite
import datetime
import time


def getAllSchedule():
    sql = "select * from runSchedule"
    res = db.execute(sql).fetchall()
    return res


def sleep2end():
    now_time = datetime.datetime.now()
    time.sleep(61 - now_time.second)


def startTestSuite(suite_id):
    user_suites = TestSuites(suite_id=suite_id, runCaseId=suite_id)   #  runCaseId=suite_id  flag of auto process
    setVariable(getStepParamByUser(getUserBySuite(suite_id), suite_id, "All")[0])
    user_suites.start()


def checkSchedule(params):
    now_time = datetime.datetime.now()
    isRun = params[1]
    # isSend = params[2]
    min = params[3]
    hour = params[4]
    day = params[5]
    month = params[6]
    week = params[7]
    try:
        if isRun != 'yes':
            return []
        if min != '*' and int(now_time.minute) != int(min):
            return []
        if hour != '*'and int(now_time.hour) != int(hour):
            return []
        if month != '*' and int(now_time.month) != int(month):
            return []
        if day != '*' and int(now_time.day) != int(day):
            return []
        if week != '*' and int(now_time.weekday()) + 1 != int(week):
            return []
    except Exception as e:
        print("check schedual error! ", e)
        return []
    return [*params]


def startSchedule():
    allSchedule = getAllSchedule()
    run_list = []
    for task in allSchedule:
        res = checkSchedule(task)
        if len(res) > 0:
            run_list.append(res)
    # print(run_list)
    for i in run_list:
        isSendOut = 0 if i[2] == 'no' else 2 if i[2] == 'sendWhenError' else 1
        setNewTask(i[0], i[0], getUserBySuite(i[0]), crID(12), isSendOut)


if __name__ == "__main__":
    from app_src.common.functions import *

    while 1:
        sleep2end()
        startSchedule()



















