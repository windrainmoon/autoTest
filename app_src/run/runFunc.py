__author__ = 'Administrator'
from app_src.common.common import *
from app_src.common.functions import *


def lineBreak(line, length):
    NoBreakPatten = "<a.*?</a>"
    def breakOne(data):
        AllNoBreakList = re.findall(NoBreakPatten, data)
        NoBreakDict = {i: j for i, j in enumerate(AllNoBreakList)}
        for i in NoBreakDict.values():
            data = data.replace(i, "\t", 1)
        len_data = len(data)
        flag = 0
        res = ""
        while 1:
            if '\n' in data[flag: flag + length] and flag < len_data:
                start = flag
                flag += data[flag: flag + length].find('\n') + 1
                res += data[start: flag]
                continue
            res += data[flag: flag + length] + '\n'
            flag += length
            if flag >= len_data:
                break
        for i in NoBreakDict.values():
            res = res.replace("\t", i, 1)
        return res
    line = line.replace("<br>", "\n")
    len_line = len(line)
    if len_line <= length:
        return line.replace("\n", '<br>')
    else:
        temp = ""
        for i in line.split("\n"):
            temp += breakOne(i)
        return temp.replace("\n", '<br>')


def getRunLogByToken(csrf_token):
    sql = "select a.runCaseId, b.suite_description,a.endTime,(case when round(a.nowItemCount*1.0/a.allItemCount*100) > 100 then 100 when round(a.nowItemCount*1.0/a.allItemCount*100) < 0 then 0 else round(a.nowItemCount*1.0/a.allItemCount*100) end)" \
          "from runTestCaseLog a,testSuites b " \
          "where a.testSuiteId = b.suite_id and csrf_token=:v1"
    res = db.execute(sql, [csrf_token, ]).fetchall()
    return res


def getRunLogByUserSuite(suite_id):
    sql = "select a.runCaseId, b.suite_description,a.endTime,(case when round(a.nowItemCount*1.0/a.allItemCount*100) > 100 then 100 when round(a.nowItemCount*1.0/a.allItemCount*100) < 0 then 0 else round(a.nowItemCount*1.0/a.allItemCount*100) end)" \
          "from runTestCaseLog a,testSuites b " \
          "where a.testSuiteId = b.suite_id and a.csrf_token = a.testSuiteId and " \
          "a.endTime > datetime('now', '+8 hour', '-4320 minute') and a.testSuiteId=:v1 "
    res = db.execute(sql, [suite_id, ]).fetchall()
    return res


def getRunSchedule(suite_id):
    sql = "select isRun, isSend, min, hour, day, month, week from runSchedule where testSuiteId=:v1"
    res = db.execute(sql, [suite_id, ]).fetchone()
    return res


def updateRunSchedule(suite_id, datas):
    sql = "update runSchedule set isRun=:isRun, isSend=:isSend, min=:min, hour=:hour, day=:day, month=:month, week=:week " \
          "where testSuiteId=:suite_id"
    db.execute(sql, [datas['isRun'], datas['isSend'], datas['min'], datas['hour'], datas['day'],
                     datas['month'], datas['week'], suite_id, ])
    db.commit()


