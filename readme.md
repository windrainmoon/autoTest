## 目录
- [项目说明](#项目说明)
	- [目录规划](#目录规划)
	- [主要代码](#主要代码)
- [部署办法](#部署办法)
	- [软件要求](#软件要求)
    - [代码部署](#代码部署)
    - [数据库部署](#数据库部署)
- [参数设置](#参数设置)
	- [主机环境设置](#主机环境设置)
	- [脚本参数设置](#脚本参数设置)
- [程序启动](#程序启动)
	- [启动前台](#启动前台界面)
	- [使用命令模式](#启动命令执行操作)
	- [查看程序状态](#查看程序状态)
	- [停止所有进程](#停止所有进程)
- [上线相关](#上线相关)
- [其他说明](#其他说明)


## 项目说明
autoTest自动化测试系统。系统根据测试组件，按照测试套件、测试用例、测试步骤的结构配置，测试步骤又分为数据库命令执行、文件生成、数据库结果断言、webservice接口等模块。执行用例时仅按照测试套件进行执行。系统采用flask实现，目前没有做前后端分离，计划将前端分离为VUE实现。

### 目录规划
`/app `前端系统目录    
`/app/sqliteDB `数据库目录  
`/tempFile `临时文件目录，生成文件时使用  
`mainApp.py `前台系统入口


### 主要代码
* mainApp.py：前台系统入口  
* autoTest.py：后台命令系统入口  
* conf.py：部分系统配置  

## 部署办法
### 软件要求
- cx-Oracle==5.3
- Flask==0.12.2
- Flask-Login==0.2.11
- Flask-WTF==0.14.2
- Jinja2==2.10

### 代码部署
上传代码至主机，即可。  

### 数据库部署
数据库涉及的相关表如下：  
执行日志表：
```
create table runTestCaseLog
(
	csrf_token TEXT not null,
	testSuiteId TEXT not null,
	startTime TEXT not null,
	endTime TEXT not null,
	user_id TEXT not null,
	allItemCount INTEGER default 0 not null,
	nowItemCount INTEGER default 0 not null,
	runCaseId TEXT
		primary key,
	runResult TEXT
);
```
测试用例表：
```
create table testCases
(
	case_id TEXT
		primary key,
	suite_id text not null,
	case_description TEXT,
	position INT default -1 not null
);
```
测试步骤表：
```
create table testSteps
(
	step_id TEXT not null,
	step_type TEXT not null,
	step_param1 TEXT,
	step_param2 TEXT,
	step_param3 TEXT,
	step_param4 TEXT,
	step_param5 TEXT,
	case_id TEXT not null,
	step_name TEXT default step not null,
	position INT default -1 not null
);
```
测试套件表：
```
create table testSuites
(
	suite_id text
		primary key,
	suite_description TEXT,
	user_id TEXT,
	position INT default -1 not null
);
```
用户表：
```
create table user
(
	user_id text
		primary key,
	user_name text,
	user_password text,
	user_head text,
	others text
);
```
用户参数表：
```
create table user_params
(
	user_id TEXT not null,
	param_name TEXT not null,
	param_type TEXT not null,
	param_value TEXT not null
);
```

## 参数设置

### 主机环境设置
Oracle客户端需要和服务器端字符集保持一致，否则中文会出现乱码  
```bash
export NLS_LANG="SIMPLIFIED CHINESE_CHINA.ZHS16GBK"
export LANG="zh_CN.UTF-8"
```
**注：**设置需要新增在**`.profile`**文件中，之后需要重新连接，终端也需要设置为UTF-8  

### 脚本参数设置
脚本参数需要在启动之前设置OK，设置方式是修改配置文件**conf.py**(代码目录下)  


## 程序启动
### 启动前台
* 启动命令: 
```
nohup python3 mainApp.py > runlog.log &
```

### 使用命令模式
* 使用说明
```
python3 autoTest.py -u user_id -p password -s suite_name
```
* -u表示执行测试流程的用户
* -p表示执行测试流程的用户密码
* -s表示执行测试流程的测试套件，只能以测试套件为集合执行测试

### 查看程序状态
这里主要查看程序的运行情况(是否挂掉，占用内存等)  
```bash
ps -eo 'pid,pcpu,size,state,cmd'|grep -v grep|grep mainApp.py
```

### 停止所有进程
使用如下命令停止相关进程  
```
ps -ef|grep mainApp.py|awk '{print $2}'|xargs kill
```
## 其他说明
代码设计请移步[这里](#docs/code_design.md)  
### 相关知识点
cx_Oracle: http://cx-oracle.readthedocs.org/en/latest/  
jstree:https://www.jstree.com.cn/

### FAQ
针对程序的任何疑问和问题请联系liyang27@chinasoftinc.com