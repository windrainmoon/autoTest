__author__ = 'Administrator'
__version__ = '2.0'
import configparser
import os
import platform

if (platform.system() == 'Windows'):
    print('LocalSystem: Windows系统')
    LocalSystem = "win"
elif (platform.system() == 'Linux'):
    print('LocalSystem: Linux系统')
    LocalSystem = "linux"
else:
    print('LocalSystem: 其他')
    LocalSystem = "other"

configFileName = 'conf.ini'

config = configparser.ConfigParser()

if not os.path.exists(configFileName):
    config['DEFAULT'] = {'PORT': 2345, 'SESSION_EXPIRE_TIME': 10}
    with open(configFileName, 'w') as configfile:
        config.write(configfile)
else:
    config.read(configFileName, encoding="utf-8-sig")

is_serviceLock = 0
try:
    port = int(config['DEFAULT']['PORT']) or 2345  # main app listening port
    SESSION_EXPIRE_TIME = int(
        config['DEFAULT']['SESSION_EXPIRE_TIME']) or 10  # session store time(minutes), re-login after expire
except Exception as e:
    print('config file error: %s' % e)
    port = 2345  # main app listening port
    SESSION_EXPIRE_TIME = 10  # session store time(minutes), re-login after expire

service_host = '127.0.0.1'
VX_ROBOT_ADDR = ''
ORACLE_CHECK_REPEAT_TIME = [1, 5, 10, 20, 100]
LINE_BREAK_LENGTH = 70

is_commit = 1
is_debug = 1

resultPostMessage = {
    "msgtype": "markdown",
    "markdown": {
        "content": "尊敬的用户，您好，凹凸仔向您发来最新的测试结果，请点击链接查看：[%s](%s)"}
}
resultPostPic = {
    "msgtype": "image",
    "image": {
        "base64": "%s",
        "md5": "%s"
    }
}
robot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=497825cd-15c1-44e7-98e8-d467a1ddab3f'

# remote_ip = "cbpadpt@172.18.56.62"
# remote_port = 4567
# scan_file = "/opt/offcdr/offcdr_nfs/cbpadpt129/input/cbs/voice/scan_file/"
# error_file = "/opt/offcdr/offcdr_nfs/cbpadpt129/input/cbs/voice/error_file/"
# backup_file = "/opt/offcdr/offcdr_nfs/cbpadpt129/input/cbs/voice/backup_file/"
#
#
# conn_bmpdb = "admin/Admin_01@bmpdb"
# conn_billdb = "BILL_125/Bill_001@billdb125"
