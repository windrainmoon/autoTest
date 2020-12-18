/**
 * Created by Administrator on 2020/7/17.
 */


function customMenu(node) {
    var items = {
        'synchronize': {
            'icon': '/static/icons/synchronize.png',
            'label': 'synchronize',
            "separator_before": false, //Create这一项在分割线之下?
            "separator_after": true, //Create这一项在分割线之上?
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedId = inst.get_node(obj.reference).id;
                var clickedType = inst.get_node(obj.reference).type;
                var all_tree_object = [{'clickedId': clickedId, 'clickedType': clickedType}];
                var data = $("#jstree").jstree(true)._model.data;
                var dataChild = findChildrenNodes(clickedId);
                for (i in data) {
                    for (j in dataChild) {
                        if (dataChild[j] == i) {
                            if (i != "#") {
                                // console.log('find!', i);
                                all_tree_object.push({
                                    'id': data[i]['id'],
                                    'text': data[i]['text'],
                                    'parent': data[i]['parent'],
                                    'type': data[i]['type'],
                                    'step_param1': data[i]['a_attr']['step_param1'],
                                    'step_param2': data[i]['a_attr']['step_param2'],
                                    'step_param3': data[i]['a_attr']['step_param3'],
                                    'step_param4': data[i]['a_attr']['step_param4'],
                                    'step_param5': data[i]['a_attr']['step_param5']
                                });
                            }
                        }
                    }
                }
                $.ajax({
                    type: "POST",
                    url: "/main/synchronizeTestSuite",
                    data: JSON.stringify(all_tree_object),
                    dataType: "json",
                    processData: false,
                    async: false,
                    success: function (result) {
                        if (result.resultCode == '302') {
                            top.location.href = result.result;
                        } else {
                            alert("synchronize success!");
                        }
                    },
                    error: function () {
                        alert("synchronize error!");
                    }
                });
            }
        },
        'addTestHome': {
            'icon': '/static/icons/testHome.png',
            'label': 'create testHome',
            'action': function (obj) {
                //reference获取当前选中节点的引用
                var inst = jQuery.jstree.reference(obj.reference);
                //通过get_node方法获取节点的信息，类似于实例对象
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testHome',
                        'text': ''
                    },
                    'last',
                    function (node) {
                        //回调返回创建后点节点，给新节点改名
                        addNode(nodeId, 'testHome', clickedNode.id);
                        try {
                            node.text = "new testHome";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'addTestSuite': {
            'icon': '/static/icons/testSuite.png',
            'label': 'create testSuite',
            'action': function (obj) {
                //reference获取当前选中节点的引用
                var inst = jQuery.jstree.reference(obj.reference);
                //通过get_node方法获取节点的信息，类似于实例对象
                var clickedNode = inst.get_node(obj.reference);
                /*
                 inst.create_node 参数1:父节点  参数2:新节点的数据
                 参数3: 1）first：当前节点下的头部新增节点
                 2）last：当前节点下的尾部新增节点
                 3）before：当前节点同级的上部新增节点
                 4）after：当前节点同级的下部新增节点
                 参数4:回调函数
                 参数5:Boolean类型,内部参数，指示父节点是否成功加载
                 */
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testSuite',
                        'text': ''
                    },
                    'last',
                    function (node) {
                        //回调返回创建后点节点，给新节点改名
                        addNode(nodeId, 'testSuite', clickedNode.id);
                        try {
                            node.text = "new testSuite";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'addTestCase': {
            'icon': '/static/icons/testCase.png',
            'label': 'create test case',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testCase',
                        'text': '',
                        "a_attr": {
                            "step_param1": "1",    // repeat execute
                            "step_param2": "",
                            "step_param3": "",
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testCase', clickedNode.id);
                        try {
                            node.text = "new TestCase";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'addDbStep': {
            'icon': '/static/icons/testStep_database.png',
            'label': 'add Db Step',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepDbExecute',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // db base
                            "step_param2": "",    // sql to execute
                            "step_param3": "",    // result save
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepDbExecute', clickedNode.id);
                        try {
                            node.text = "new OraStep";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'addDbCheck': {
            'icon': '/static/icons/testStep_dataAssert.png',
            'label': 'add Db check',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepDbCheck',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // db base
                            "step_param2": "",    // predict result
                            "step_param3": "",    // check sql
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepDbCheck', clickedNode.id);
                        try {
                            node.text = "new OraCheck";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'addFileStep': {
            'icon': '/static/icons/testStep_file.png',
            'label': 'add File Step',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepFile',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // machine host
                            "step_param2": "",    // file type--file_name
                            "step_param3": "",    // property1--file path
                            "step_param4": "",    // property2--file_content
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepFile', clickedNode.id);
                        try {
                            node.text = "new FileStep";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'addWebInterfaceStep': {
            'icon': '/static/icons/testStep_interface.png',
            'label': 'add webService Step',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepWebInterface',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // webservice url
                            "step_param2": "",    // webservice body
                            "step_param3": "",
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepWebInterface', clickedNode.id);
                        try {
                            node.text = "new webInterface Step";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'addCmdStep': {
            'icon': '/static/icons/testStep_CMD.png',
            'label': 'add cmd Step',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepCmd',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // linux host
                            "step_param2": "",    // cmd
                            "step_param3": "",
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepCmd', clickedNode.id);
                        try {
                            node.text = "new Cmd Step";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'addReportStep': {
            'icon': '/static/icons/testStep_report.png',
            'label': 'add report Step',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepReport',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // send robot address; empty means not send
                            "step_param2": "",    // report message
                            "step_param3": "",
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepReport', clickedNode.id);
                        try {
                            node.text = "new Report";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'testStepGui': {
            'icon': '/static/icons/testStep_GUI.png',
            'label': 'add testStepGui',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepGui',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // send robot address; empty means not send
                            "step_param2": "",    // report message
                            "step_param3": "",
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepGui', clickedNode.id);
                        try {
                            node.text = "new TestGUI";
                            inst.edit(node);
                        } catch (ex) {
                            setTimeout(function () {
                                inst.edit(node);
                            }, 0);
                        }
                    }, '');
            }
        },
        'rename': {
            'icon': '/static/icons/icon_rename.png',
            'label': 'change name',
            "separator_before": true, //Create这一项在分割线之下?
            "separator_after": false, //Create这一项在分割线之上?
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                inst.edit(obj.reference, clickedNode.val);
            }
        },
        'delete': {
            'icon': '/static/icons/icon_delete.png',
            "label": "delete item",
            'action': function (obj) {
                function doDelete() {
                    var inst = jQuery.jstree.reference(obj.reference);
                    var clickedNode = inst.get_node(obj.reference);
                    var result = deleteItem(clickedNode.id, clickedNode.type);
                    if (result) {
                        inst.delete_node(obj.reference);
                    }
                }

                var isAlarm = queryUserAuthority('isDeleteAlarm');
                if (isAlarm) {
                    myConfirm('系统提示', '确定要删除嘛？！', function (r) {
                        if (r) {
                            doDelete()
                        }
                    });
                } else {
                    doDelete()
                }
            }
        }

    };


    if (node.type == 'root') {
        delete items.addTestSuite;
        delete items.addTestCase;
        delete items.delete;
        delete items.rename;
        delete items.addDbStep;
        delete items.addFileStep;
        delete items.addDbCheck;
        delete items.addWebInterfaceStep;
        delete items.addCmdStep;
        delete items.addReportStep;
        delete items.testStepGui;
    } else if (node.type == 'testHome') {
        delete items.addTestHome;
        delete items.addTestCase;
        delete items.addDbStep;
        delete items.addFileStep;
        delete items.addDbCheck;
        delete items.addWebInterfaceStep;
        delete items.addCmdStep;
        delete items.addReportStep;
        delete items.testStepGui;
    }else if (node.type == 'testSuite') {
        delete items.addTestHome;
        delete items.addTestSuite;
        delete items.addDbStep;
        delete items.addFileStep;
        delete items.addDbCheck;
        delete items.addWebInterfaceStep;
        delete items.addCmdStep;
        delete items.addReportStep;
        delete items.testStepGui;
    } else if (node.type == 'testCase') {
        delete items.addTestHome;
        delete items.addTestCase;
        delete items.addTestSuite;
        // if (user_type != 'admin'){
        //     delete items.testStepGui;
        // }
    } else if (node.type.substr(0, 8) == 'testStep') {
        delete items.addTestHome;
        delete items.addTestSuite;
        delete items.addTestCase;
        delete items.addDbStep;
        delete items.addDbCheck;
        delete items.addFileStep;
        delete items.addWebInterfaceStep;
        delete items.addCmdStep;
        delete items.addReportStep;
        delete items.testStepGui;
    } else {
        delete items.addTestHome;
        delete items.addTestSuite;
        delete items.addTestCase;
        delete items.delete;
        delete items.rename;
        delete items.addDbStep;
        delete items.addDbCheck;
        delete items.addFileStep;
        delete items.addWebInterfaceStep;
        delete items.addCmdStep;
        delete items.addReportStep;
        delete items.testStepGui;
    }

    return items;
}//注意要有返回值

function addNode(nodeId, nodeType, parentId) {
    $.ajax({
        type: "POST",
        url: "/main/addNode",
        data: JSON.stringify({'id': nodeId, 'type': nodeType, 'parent': parentId}),
        dataType: "json",
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            }
            // console.log("create node!", nodeId, nodeType)
        },
        error: function (result) {
            console.log("create node error!", nodeId, nodeType);
        }
    });
}

function moveNode(data) {
    var id = data.node.id;
    var type = data.node.type;
    var old_position = data.old_position;
    var old_parent = data.old_parent;
    var new_position = data.position;
    var new_parent = data.parent;
    $.ajax({
        type: "POST",
        url: "/main/moveNode",
        data: JSON.stringify({
            'id': id, 'type': type, 'old_position': old_position, 'new_position': new_position,
            'old_parent': old_parent, 'new_parent': new_parent
        }),
        dataType: 'json',
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else {
                var params = result.result;
            }
        },
        error: function (result) {
            alert("move node error!");
        }
    });
}

function copyNode(data) {
    // console.log('copy:', data);
    var type = data.original.type;
    var oriId = data.original.id;
    var oriParent = data.old_parent;
    var oriChildren = data.original.children_d;
    var newId = data.node.id;
    var newParent = data.parent;
    var newChildren = data.node.children_d;
    var position = data.position;

    $.ajax({
        type: "POST",
        url: "/main/copyNode",
        data: JSON.stringify({
            'oriId': oriId, 'type': type, 'oriParent': oriParent, 'newId': newId,
            'newParent': newParent, 'position': position, 'oriChildren': oriChildren, 'newChildren': newChildren
        }),
        dataType: 'json',
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else {
                params = result.result;
            }


        },
        error: function (result) {
            alert("copy node error!");
        }
    });
}

function deleteItem(item_id, item_type) {
    var res = false;
    $.ajax({
        //几个参数需要注意一下
        type: "GET",//方法类型
        async: false,
        dataType: "json",//预期服务器返回的数据类型
        url: "/main/delete?item_id=" + item_id + "&item_type=" + item_type,
        success: function (result) {
//                console.log(result);//打印服务端返回的数据(调试用)
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else if (result.resultCode == 200) {
                res = true;
            } else {
                console.log(result);
            }
        },
        error: function () {
            alert("异常！");
        }
    });
    return res;
}

function queryUserAuthority(authority_type) {
    var res = false;
    $.ajax({
        //几个参数需要注意一下
        type: "GET",//方法类型
        async: false,
        dataType: "json",//预期服务器返回的数据类型
        url: "/main/queryUserRole?authority_type=" + authority_type,
        success: function (result) {
//                console.log(result);//打印服务端返回的数据(调试用)
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else if (result.resultCode == 200 && result.result == 1) {
                res = true;
            } else {
                console.log(result);
            }
        },
        error: function () {
            alert("异常！");
        }
    });
    return res;
}


function refreshTreeParam1() {
    var val = $("#step_param1").val();
    var id = $("#testDetailId").val();
    $("#jstree").jstree(true)._model.data[id].a_attr['step_param1'] = val;
    //console.log(val);
}

function refreshTreeParam2() {
    var val = $("#step_param2").val();
    var id = $("#testDetailId").val();
    $("#jstree").jstree(true)._model.data[id].a_attr['step_param2'] = val;
    //console.log(val);
}

function refreshTreeParam3() {
    var val = $("#step_param3").val();
    var id = $("#testDetailId").val();
    $("#jstree").jstree(true)._model.data[id].a_attr['step_param3'] = val;
    //console.log(val);
}

function refreshTreeParam4() {
    var val = $("#step_param4").val();
    var id = $("#testDetailId").val();
    $("#jstree").jstree(true)._model.data[id].a_attr['step_param4'] = val;
    //console.log(val);
}


function findChildrenNodes(id) {
    var children = findChildrenNode(id);
    var temp = children.slice();
    var tempChild = [];
    for (var i = 0; i < 4; i++) {
        for (j in temp) {
            var res = findChildrenNode(temp[j]);
            children = children.concat(res);
            tempChild = tempChild.concat(res);

        }
        temp = tempChild.slice();
        tempChild = [];
    }
    return children.concat(id);
}


function findChildrenNode(id) { //ids 是子节点数组
    var children = [];
    var data = $("#jstree").jstree(true)._model.data;
    for (j in data) {
        // console.log(j, '-->', data[j]['parent'], '-->', id);
        if (data[j]['parent'] == id) {
            children.push(j);
        }
    }
    return children;


    // for (var i = 0; i < 3; i++) {
    //     var parent_id = $("#jstree").jstree(true)._model.data[id].parent;
    //     var parent_name = $("#jstree").jstree(true)._model.data[parent_id].text;
    //     if (parent_id != "root") {
    //         parents.push(parent_id, parent_name);
    //         id = parent_id;
    //     } else {
    //         break
    //     }
    // }
    // return parents;
}

function findParentNode(id) {
    var parents = "";
    for (var i = 0; i < 3; i++) {
        var parent_id = $("#jstree").jstree(true)._model.data[id].parent;
        if (parent_id != "root") {
            id = parent_id;
        } else {
            return id;
        }
    }
}


function setTestCaseRecycle(dom) {
    var step_id = dom.id;
    var step_param1 = dom.a_attr.step_param1;

    var text = "<div style='width: 100%'><div class='bc_field_label'>请选择testCase循环执行次数:</div><input id='step_param1' maxlength='2' type=\"text\" name=\"\" onchange='refreshTreeParam1();' oninput=\"value=value.replace(/[^\\d]/g,'')\" value='" + step_param1 + "'></div>";


    $("#testCaseDetail").html("");
    $("#testCaseDetail").append("<h2>循环执行testCase</h2>");
    $("#testCaseDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'/>");
    $("#testCaseDetail").append("<div id='aaaaa' style='width:90%'>" + text);

    refreshTreeParam1();
}

function setStepDbExecute(dom) {
    var step_id = dom.id;
    var parent = findParentNode(step_id);
    var params;
    $.ajax({
        type: "GET",
        url: "/main/queryStepParam?stepType=testStepDbExecute&param_tree_id=" + parent,
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else {
                params = result.result;
            }
        },
        error: function (result) {
            alert("Get user params error!");
        }
    });
    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;
    var step_param3 = dom.a_attr.step_param3;

    var oraChoice = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择数据库:</div><div class='bc_field_select'><select id='step_param1' class='select_limit' name='step_param1' onchange='refreshTreeParam1();'>";
    var param1_choose_flag = false;
    for (i in params[0]) {
        if (params[0][i][1] == step_param1) {
            oraChoice += "<option value='" + params[0][i][1] + "' selected>" + "(" + params[0][i][2] + ")" + params[0][i][1] + "</option>";
            param1_choose_flag = true;
        } else {
            oraChoice += "<option value='" + params[0][i][1] + "'>" + "(" + params[0][i][2] + ")" + params[0][i][1] + "</option>"
        }
    }
    if (false == param1_choose_flag) {
        oraChoice += "<option value='' selected>";
    }
    oraChoice += "</select></div></div>";

    var oraResult = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择结果保存参数:</div><div class='bc_field_select'><select name='step_param2' class='select_limit' id='step_param2' onchange='refreshTreeParam2();'>";
    oraResult += "<option value='' selected>";
    for (i in params[1]) {
        if (params[1][i][1] == step_param2) {
            oraResult += "<option value='" + params[1][i][1] + "' selected>" + params[1][i][1] + "</option>";
        } else {
            oraResult += "<option value='" + params[1][i][1] + "'>" + params[1][i][1] + "</option>"
        }
    }


    oraResult += "</select></div></div>";

    var SQLinput = "<div style='width: 100%'><div class='bc_field_label'>请输入执行sql:</div><textarea onkeyup='refreshTreeParam3();' class='bc_field_textarea' name='editor1' id='step_param3'>" + step_param3;

    $("#testCaseDetail").html("");
    $("#testCaseDetail").append("<h2>数据库操作模块</h2>");
    $("#testCaseDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'></input");
    $("#testCaseDetail").append("<div id='aaaaa' style='width:90%'>" + oraChoice + oraResult + SQLinput);

    refreshTreeParam1();
    refreshTreeParam2();
    refreshTreeParam3();

}


function setStepFile(dom) {
    var step_id = dom.id;
    var parent = findParentNode(step_id);
    var params;
    $.ajax({
        type: "GET",
        url: "/main/queryStepParam?stepType=testStepFile&param_tree_id=" + parent,
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else {
                params = result.result;
            }
        },
        error: function (result) {
            alert("Get user params error!");
        }
    });

    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;
    var step_param3 = dom.a_attr.step_param3;
    var step_param4 = dom.a_attr.step_param4;

    var HostChoice = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择执行的主机:</div><div class='bc_field_select'><select id='step_param1'  name='step_param1' onchange='refreshTreeParam1();'>";
    for (i in params[0]) {
        if (params[0][i][1] == step_param1) {
            HostChoice += "<option value='" + params[0][i][1] + "' selected>" + params[0][i][1] + "</option>"
        } else {
            HostChoice += "<option value='" + params[0][i][1] + "'>" + params[0][i][1] + "</option>"
        }
    }
    HostChoice += "</select></div></div>";

    var FileName = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请输入文件名:</div>" +
        "<div class='bc_field_input'>";
    FileName += "<input name='step_param2' class='bc_field_input' id='step_param2' onchange='refreshTreeParam2();' value='" + step_param2 + "'>";
    FileName += "</div></div>";

    var FilePath = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请输入路径:</div>" +
        "<div class='bc_field_input'>";
    FilePath += "<input name='step_param3' class='bc_field_input' id='step_param3' onchange='refreshTreeParam3();' value='" + step_param3 + "'>";
    FilePath += "</div></div>";


    var FileContent = "<div style='width: 100%'><div class='bc_field_label'>请输入文件内容:</div><textarea placeholder='文件内容可以使用固定内容，或$()符号将预定参数包含，如$(server)。数据库查询结果内容默认以逗号分隔。' onkeyup='refreshTreeParam4();' class='bc_field_textarea' name='editor1' id='step_param4'>" + step_param4;

    $("#testCaseDetail").html("");
    $("#testCaseDetail").append("<h2>文件操作模块</h2>");
    $("#testCaseDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'>");
    $("#testCaseDetail").append("<div id='aaaaa' style='width:90%'>" + HostChoice + FileName + FilePath + FileContent);

    refreshTreeParam1();
    refreshTreeParam2();
    refreshTreeParam3();
    refreshTreeParam4();

}


function setStepDbCheck(dom) {
    var step_id = dom.id;
    var parent = findParentNode(step_id);
    var params;
    $.ajax({
        type: "GET",
        url: "/main/queryStepParam?stepType=testStepDbCheck&param_tree_id=" + parent,
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else {
                params = result.result;
            }
        },
        error: function (result) {
            alert("Get user params error!");
        }
    });
    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;
    var step_param3 = dom.a_attr.step_param3;
    var step_param4 = dom.a_attr.step_param4;

    var oraChoice = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择数据库:</div><div class='bc_field_select'><select id='step_param1' class='select_limit' name='step_param1' onchange='refreshTreeParam1();'>";
    var param1_choose_flag = false;
    for (i in params[0]) {
        if (params[0][i][1] == step_param1) {
            oraChoice += "<option value='" + params[0][i][1] + "' selected>" + "(" + params[0][i][2] + ")" + params[0][i][1] + "</option>";
            param1_choose_flag = true;
        } else {
            oraChoice += "<option value='" + params[0][i][1] + "'>" + "(" + params[0][i][2] + ")" + params[0][i][1] + "</option>"
        }
    }
    if (false == param1_choose_flag) {
        oraChoice += "<option value='' selected>";
    }
    oraChoice += "</select></div></div>";

    var oraCheck = "<div style='width: 100%'><div class='bc_field_label'>请输入验证结果:</div><textarea placeholder='在此输入数据库待验证结果。如期待多字段结果分别为1，2，3时，请输入1,2,3' onkeyup='refreshTreeParam2();' class='bc_field_textarea' name='editor1' id='step_param2' style='height: 15%'>" + step_param2 + "</textarea></div>";

    var SQLinput = "<div style='width: 100%'><div class='bc_field_label'>请输入执行sql:</div><textarea placeholder='如果SQL为多个时，请以分号分隔；以最后一个sql的结论为准' onkeyup='refreshTreeParam3();' class='bc_field_textarea' name='editor1' id='step_param3'>" + step_param3 + "</textarea></div>";

    //新增参数4控制执行循环次数，直到循环执行，直到超过最大次数还不能匹配才报错
    var repeatCheck = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择最大执行次数:</div><div class='bc_field_select'><select id='step_param4' class='select_limit' name='step_param1' onchange='refreshTreeParam4();'>";
    for (i in params[1][0]) {
        if (params[1][0][i] == step_param4) {
            repeatCheck += "<option value='" + params[1][0][i] + "' selected>" + params[1][0][i] + "</option>";
        } else {
            repeatCheck += "<option value='" + params[1][0][i] + "'>" + params[1][0][i] + "</option>"
        }
    }
    repeatCheck += "</select></div></div>";

    $("#testCaseDetail").html("");
    $("#testCaseDetail").append("<h2>数据库断言模块</h2>");
    $("#testCaseDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'></input");
    $("#testCaseDetail").append("<div id='aaaaa' style='width:90%'>" + oraChoice + repeatCheck + oraCheck + SQLinput);

    refreshTreeParam1();
    refreshTreeParam2();
    refreshTreeParam3();
    refreshTreeParam4();
}

function setStepWebInterface(dom) {
    var step_id = dom.id;
    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;
    var step_param3 = dom.a_attr.step_param3;

    var webServiceUrl = "<div style='width: 100%'><div class='bc_field_label'>请输入接口地址:</div><textarea placeholder='在此输入接口地址' onkeyup='refreshTreeParam1();' class='bc_field_textarea' name='editor1' id='step_param1' style='height: 10%'>" + step_param1 + "</textarea></div>";
    var webServiceBody = "<div style='width: 100%'><div class='bc_field_label'>请输入接口内容:</div><textarea placeholder='在此输入报文内容' onkeyup='refreshTreeParam2();' class='bc_field_textarea' name='editor1' id='step_param2'>" + step_param2 + "</textarea></div>";
    var webServiceAssert = "<div style='width: 100%'><div class='bc_field_label'>请输入接口预期结果:</div><textarea placeholder='在此输入报文预期结果，如果没有预期则返回正常' onkeyup='refreshTreeParam3();' class='bc_field_textarea' name='editor1' id='step_param3' style='height: 10%'>" + step_param3 + "</textarea></div>";

    $("#testCaseDetail").html("");
    $("#testCaseDetail").append("<h2>webservice接口模块</h2>");
    $("#testCaseDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'></input");
    $("#testCaseDetail").append("<div id='aaaaa' style='width:90%'>" + webServiceUrl + webServiceAssert + webServiceBody);

    refreshTreeParam1();
    refreshTreeParam2();
    refreshTreeParam3();

}

var all_params;

function setStepCmd(dom) {
    var step_id = dom.id;
    var parent = findParentNode(step_id);
    var params;
    $.ajax({
        type: "GET",
        url: "/main/queryStepParam?stepType=testStepCmd&param_tree_id=" + parent,
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else {
                params = result.result;
                all_params = params;
            }
        },
        error: function (result) {
            alert("Get user params error!");
        }
    });

    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;
    var step_param3 = dom.a_attr.step_param3;
    var step_param4 = dom.a_attr.step_param4;


    var HostChoice = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择执行的主机:</div><div class='bc_field_select'><select id='step_param1'  name='step_param1' onchange='refreshTreeParam1();'>";
    for (i in params[0]) {
        if (params[0][i][1] == step_param1) {
            HostChoice += "<option value='" + params[0][i][1] + "' selected>" + params[0][i][1] + "</option>"
        } else {
            HostChoice += "<option value='" + params[0][i][1] + "'>" + params[0][i][1] + "</option>"
        }
    }
    HostChoice += "</select></div></div>";

    var CmdChoice = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择执行的命令:</div>" +
        "<div class='bc_field_select'><select id='step_param2' style='width: 200%' name='step_param2' " +
        "onchange='refreshTreeParam2();" +
        "$(\"#cmdDetail\").html(\"\");" +
        "for (i in all_params[1]) {if (all_params[1][i][1] == this.options[this.options.selectedIndex].value) {$(\"#cmdDetail\").html(all_params[2][i])}};" +
        "if( $(\"#step_p2_bak\").val()== this.options[this.options.selectedIndex].value) {splitValue()};' >";
    CmdChoice += "<option value='' selected>";
    for (i in params[1]) {
        if (params[1][i][1] == step_param2) {
            CmdChoice += "<option value='" + params[1][i][1] + "' selected>" + params[1][i][1] + "</option>"
            var cmdDetail = params[2][i];
        } else {
            CmdChoice += "<option value='" + params[1][i][1] + "'>" + params[1][i][1] + "</option>"
        }
    }
    CmdChoice += "</select></div></div>";
    if (typeof (cmdDetail) == "undefined") {
        var cmdDetailDom = "<div id='cmdDetail'></div>";
    } else {
        var cmdDetailDom = "<div id='cmdDetail'>" + cmdDetail + "</div>";
    }


    //新增参数4控制执行循环次数，直到循环执行，直到超过最大次数还不能匹配才报错
    var repeatCheck = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择最大执行次数:</div><div class='bc_field_select'><select id='step_param4' class='select_limit' name='step_param1' onchange='refreshTreeParam4();'>";
    for (i in params[3][0]) {
        if (params[3][0][i] == step_param4) {
            repeatCheck += "<option value='" + params[3][0][i] + "' selected>" + params[3][0][i] + "</option>";
        } else {
            repeatCheck += "<option value='" + params[3][0][i] + "'>" + params[3][0][i] + "</option>"
        }
    }
    repeatCheck += "</select></div></div>";

    $("#testCaseDetail").html("");
    $("#testCaseDetail").append("<h2>CMD命令模块</h2>");
    $("#testCaseDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'>");
    $("#testCaseDetail").append("<textarea id='step_param3' hidden='hiddin'>" + step_param3 + "</textarea>");
    $("#testCaseDetail").append("<input id='step_p2_bak' hidden='hiddin' value='" + step_param2 + "'>");
    $("#testCaseDetail").append("<div id='aaaaa' style='width:90%'>" + HostChoice + repeatCheck + CmdChoice + cmdDetailDom);

    splitValue();
    refreshTreeParam1();
    refreshTreeParam2();
    // 第三个参数分解为其他节点单独刷新refreshTreeParam3();
    refreshTreeParam4();
}

// 自定义参数使用此方法刷新参数
function combineValue(length) {
    var res = "";
    for (var i = 0; i < length; i++) {
        res += $("#cmd_" + i).val() + "=="
    }
    $("#step_param3").val(res);
    refreshTreeParam3();
}

function splitValue() {
    var step_param3 = $("#step_param3").val();
    var origin_value = new Array();
    var start = 0;
    var pos = step_param3.indexOf('==');

    while (pos > -1) {
        origin_value.push(step_param3.substr(start, pos - start));
        start = pos + 2;
        pos = step_param3.indexOf('==', pos + 2);
    }
    for (i in origin_value) {
        $("#cmd_" + i).val(origin_value[i])
    }
}

function setStepReport(dom) {
    var step_id = dom.id;
    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;

    var reportUrl = "<div style='width: 100%'><div class='bc_field_label'>请输入接口地址:</div><textarea placeholder='在此输入report robot地址,如果没有地址则不会主动推送(目前不启用)' onkeyup='refreshTreeParam1();' class='bc_field_textarea' name='editor1' id='step_param1' style='height: 10%'>" + step_param1 + "</textarea></div>";
    var reportBody = "<div style='width: 100%'><div class='bc_field_label'>请输入接口内容:</div>" +
        "<textarea placeholder='在此输入report内容，语法为markdown语法，仅替换图片格式为自定义图片。格式为：\n\n![title](type=[bar|pie|table];head=[head];datas=[datas]) \n\n如：\n![这里是title](type=bar;head=2019,2020;datas=甲,1,2\n乙,2,3\n丙,3,4)' " +
        "onkeyup='refreshTreeParam2();' class='bc_field_textarea' name='editor1' id='step_param2'>" + step_param2 + "</textarea></div>";

    $("#testCaseDetail").html("");
    $("#testCaseDetail").append("<h2>report模块</h2>");
    $("#testCaseDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'></input");
    $("#testCaseDetail").append("<div id='aaaaa' style='width:90%'>" + reportUrl + reportBody);

    refreshTreeParam1();
    refreshTreeParam2();
}