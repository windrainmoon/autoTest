__author__ = 'Administrator'
import getopt



def usage():
    print("missing parameters! ")
    print("usage: python3 autoTest.py -u user_id -p password -s suite_name ")
    sys.exit(-1)


if __name__ == "__main__":
    from app_src.common.functions import *

    args = sys.argv
    opts, args = getopt.getopt(sys.argv[1:], 'u:p:s:', ['user_id', 'password', 'suite'])
    if len(opts) < 3:
        usage()
    user_id = ""
    password = ""
    suite_name = ""
    for opt_name, opt_value in opts:
        if opt_name == '-u':
            user_id = opt_value
        elif opt_name == '-p':
            password = opt_value
        elif opt_name == '-s':
            suite_name = opt_value
        else:
            usage()
    checkFlag, checkResult = checkUser(user_id, password)
    if not checkFlag:
        # print(checkResult)
        sys.exit(-1)
    user_suites = TestSuites(user_id=user_id, suite_name=suite_name)
    suite_exists = user_suites.checkUserSuites()
    if not suite_exists:
        print("input suite name[%s] not exists!" % suite_name)
        sys.exit(-1)
    print('start autotest!')
    setVariable(getStepParamByUser(user_id, suite_exists, "All")[0])
    user_suites.start()
    makeLinuxResult()




