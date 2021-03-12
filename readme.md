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


### 相关知识点
cx_Oracle: http://cx-oracle.readthedocs.org/en/latest/  
jstree:https://www.jstree.com.cn/

### FAQ
针对程序的任何疑问和问题请联系lllygogogo@163.com



# 功能使用说明

---

![title](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/eye_40_60.jpg)

- version=2.0

##1.登录
输入用户密码后，点击登录进入系统。默认10分钟未操作即需要重新登录。

![login](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_login.png)
 
## 2.TestCaseManagement测试用例管理
进入管理界面后如下图所示。在根目录autoTestCase下，可以新增testHome，在testHome下可以新增testSuite。在testSuite下，可以新增testCase。在testCase下，可以新增testStep。testStep包括database命令（sql）操作、远程文件生成、远程shell命令执行、database断言、自定义报告输出、webservice接口及GUI测试操作。

![testCase](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_testCase_1.png)

注意testStep顺序，执行时将按照顺序进行执行。每一步报错后，下一步即会直接跳过不再执行。
每个组件都可以进行拖动以改变执行顺序。按住ctrl键拖动时，可以复制整个组件到新的位置。请记得修改相关文字说明。
修改组件相关信息时，请在各节点按钮上右键，选择synchronize进行同步。不同节点会同步包括此节点及以下的所有配置（不包括参数相关，参数需在当前页面同步）
 
 ![synchronize](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_synchronize.png)

## 2.1 用户参数
单击根目录autoTestCase按钮，展示框会展示用户参数配置界面。autoTestCase根节点为公共参数节点，配置的参数全局可用。各testSuite上配置的参数本testSuite上可用。如果和公共节点有名称冲突，则以testSuite上配置的参数为准。

![param](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_param.png)

参数类型分为5种：

+ sql_result：数据库结果保存参数。在数据库命令执行模块中的结果会保存在此参数上，以供其他模块使用。
+ db_[数据库类型]：数据库连接配置参数。配置后可以在其他模块进行选择。可以支持oracle、mysql和gmdb配置。配置参数形式如：user/password@service。其中service在连接oracle时可以为ip:port/sid、tns名称，或连接gmdb时为ipc、ip:port。由于不确定主机上是否有相关配置，建议修改为ip形式。
+ cmd：远程命令参数。配置后可以在其他模块进行选择。方式为参数说明以$()进行引用，则会在界面单独展示。引用的文字会作为说明展示在界面上。如配置cp $(请输入原文件地址+文件名) $(请输入复制后的地址+文件名)，则界面会生成两个文本框，其说明分别为“请输入原文件地址+文件名”和“请输入复制后的地址+文件名”。
+ linux：主机连接配置参数。配置后可以在其他模块进行选择。
+ string：字符串参数。配置后可以在其他模块作为参数使用。

注意参数名不可为空。配置修改后需点击“同步”按钮进行同步，否则无法保存。

## 2.2 数据库操作模块
数据库操作模块需要选择执行sql的数据库。结果可以不选择进行保存。

![s_oracleExecute](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_oracleExecute.png)
 
参数可以使用$(参数名)进行引用。注意不要在参数名前后增加空格。多个sql可以以分号分隔。如果选择保存执行结果，每次的执行结果都会循环覆盖保存到参数中。

## 2.3 数据库断言模块
数据库断言模块需要选择执行sql的数据库。验证结果如果为多字段时，以逗号分隔。如执行SQL为：select id,name,age from student;那么期待结果可以为：001,王,15

![s_oracleAssert](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_oracleAssert.png)

## 2.4 文件操作模块
选择需要生成文件的主机，及相应的文件名和路径。

![s_file](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_file.png)


## 2.5 webservice接口模块
输入请求的接口地址及入参内容。入参中可以使用参数代替，但不能执行java命令。接口预期结果需要按节点顺序输入，每个节点以中括号引用，重复的节点名称直接使用数字索引，从0开始。判断符合可以为=，<，>，<=，>=，!=。
如:

```
[soapenv:Envelope][soapenv:Body][bcs:ChangeSubOwnershipResultMsg][ResultHeader][cbs:ResultCode]>= 0
```

或者直接输入`haskey(cbs:ResultCode,0)`判断是否有此内容在返回报文中。
多条判断条件以换行分隔。
 
 ![s_interface](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_interface.png)

## 2.6 shell命令模块
使用前需要先配置cmd参数。如下形式：
`mv $(某目录文件A) $(某目录文件B)$(output)`
则界面展示如下图所示。建议参数名称可以体现用途，如此命令名称为：移动“某目录文件A”到“某目录文件B”。
  
  ![s_cmd](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_cmd.png)

如果命令中存在$(output)标记，则此命令需要进行返回值断言，界面上可以输入断言值（在“期望的输出”框中输入断言值）命令转义后不会展示$(output)标记。如果不需要断言，则执行命令成功即为成功。在最大循环次数后，如果断言为假，则返回错误。

## 2.7 report模块
自定义report输出。
输入语法为markdown语法，常用语法如下：

1.标题

```
# 标题一
## 标题二
### 标题三
#### 标题四
##### 标题五
###### 标题六
```

2.加粗

```markdown
**bold**
```

3.链接

```markdown
[这是一个链接](http://www.baidu.com)
```

4.引用

```markdown
> 引用文字
```

仅替换图片语法为自定义格式：

```markdown
![title](type=[bar|pie|table];head=[head];datas=[datas])
```

默认参数如上所示。其中，type是必填项，可选参数有`bar|pie|table`三种。每个参数之间使用分号分隔。

举个栗子：2019及2020年度甲乙丙三人的业绩分别为：

| |2019|2020|
|----|----|----|
|甲|1|2|
|乙|2|3|
|丙|3|4|

`bar`表示柱状图。柱状图中head表示柱状图的数据类型，即为表头。datas表示详细数据。因此应表示为：

```
![这里是title](type=bar;head=2019,2020;datas=甲,1,2
乙,2,3
丙,3,4)
```

数据之间用逗号隔开，每行数据用换行符隔开。默认第一列为横轴节点，其他列为相应值。注意其他列应为数字。如果是sql_result参数，直接写参数替换即可，如$(我是参数)。
结果如下所示：

![report1](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_report1.png)

`pie`表示饼图。饼图中不需要head参数。仅需要N行两列的数据为展示数据，其中，第一列数据作为每个分项的名称，第二列数据应为数字，作为每个分项的值。因此应表示为

```
![这里是title,2019年度](type=bar;datas=甲,1
乙,2
丙,3)
```

![report2](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_report2.png)

`table`表示自定义表格（原有markdown格式表格仍然可以支持）。表格不限制数据类型，可以展示任意字符串。head表示表头，如果不填则以数字默认填写。datas表示详细数据，按行填写。

```
![这里是title](type=table;head=占位符,2019,2020;datas=甲,1,2
乙,2,3
丙,3,4)
```

![report3](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_report3.png)

## 2.8 test Gui模块
test Gui模块采用基于openCV定位，java.awt.Robot模拟操作，以截图匹配代替传统基于dom分析或其他定位方法用以测试（或执行）几乎所有类型的桌面操作。

由于采用了部分java接口，因此需要先安装java11，并且配置JDK_HOME环境变量。

使用路径请不要使用中文！

界面如下所示：

![gui1](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_gui_1.png)

步骤类型共分为5种操作：

+ openApp：打开一个APP应用，如web操作打开Chrome浏览器，需要在“参数值”栏中输入APP的绝对地址。如“C:\Program Files (x86)\Google\Chrome\Application\chrome.exe”。
+ wait：等待一个图像/时间的出现。如果需要等待某个图像出现，需要先使用截图工具进行截图，如“alt + a”（微信）、“Alt + shift + a”（企业微信），截图后直接粘贴到“对象”栏中即可。粘贴后图像正中位置会出现红色“+”符号，可以忽略。“参数值”栏可以输入等待的最大时间。当输入图像时，一旦图像在屏幕中找到，则直接开始进行下一步；当未输入图像，仅输入时间时，则一定会等待到最大时间。当仅有图像未输入最大时间时，默认时间为5秒。
+ input：在某处进行键盘操作。“对象”栏可以粘贴需要进行输入的位置，鼠标在图片上单击后，会在相应位置产生红色“+”号，即为实际进行输入的位置。“参数值”栏输入需要输入的值。为了简便模拟操作，此处仅支持特殊按键操作，其他字符直接输入到相应位置。如果没有粘贴图像时，直接在背景环境输入相应参数，如光标已经在输入栏取得焦点。
  
  特殊字符如“回车”键，输入时如下所示：$ENTER$。如“123$ENTER$”表示在此处输入“123”后按回车键。直接输入特殊按键也可以操作。
  
  目前支持的特殊按键有：
  
 |按键|说明|
|----|----|
|$ENTER$|回车键|
|$TAB$|制表符|
|$ESC$|返回键|
|$BACKSPACE$|退格键|
|$DELETE$|删除键|
|$INSERT$|插入键|
|$SPACE$|空格键|
|$HOME$|HOME键|
|$END$|END键|
|$LEFT$|箭头向左|
|$RIGHT$|箭头向右|
|$UP$|箭头向上|
|$DOWN$|箭头向下|
|$PAGE_UP$|向上翻页|
|$PAGE_DOWN$|向下翻页|

+ click：在某处进行单击。截图后直接粘贴到“对象”栏中即可，如果需要单击的位置不是正中间，可以自行选择。“参数值”栏输入无效。
+ closeApp：触发APP的关闭操作。只是触发关闭操作而不是强制关闭，有时需要按APP的要求进行关闭确认。

连贯的步骤可以分为多个testStep进行。如先打开APP，进行一部分操作后，在中间加入后台的验证，再进行下一个GUI的操作。同一个testSuite中的GUI是统一连贯的。示例如下：

![gui2](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_gui_2.png)

是否可忽略标志表示此操作如果执行失败，是否可以忽略并开始下一步操作。如某些弹窗或操作是有几率出现的，可以在此处配置为“yes”，即可在此步骤未执行或失败时跳过，直接处理下一个步骤。

一个连贯的操作如下所示：

![gui3](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/g_gui_1.gif)

## 3. 配置循环测试用例
在testCase节点上，可以配置循环执行参数，控制本testCase的执行循环次数，默认为1次，为避免循环次数太多造成执行时间过长，因此最多可设置为99次。设置0次则会跳过本testCase的执行。

建议如果每次执行参数需要变化时，将相应的testStep放在同一个testCase下。

建议循环执行用例中的testStep的循环时间不宜设置的太长，否则导致用例执行时间过长。

## 4. 执行用例
在runTestCase界面，打开配置树，只能显示到testSuite一层。在testSuite上右键，选择runTestSuite，即可开始执行此测试套件。执行完成后，可点击“showResult”按钮查看执行结果。
  
![s_startCase1](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_startCase1.png)
#

![s_startCase2](https://github.com/windrainmoon/autoTest/blob/master/app_src/static/docs_pic/s_startCase2.png)

 
