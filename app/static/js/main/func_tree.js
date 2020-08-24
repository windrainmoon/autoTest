/**
 * Created by Administrator on 2020/7/17.
 */


function customMenu(node) {
    var items = {
        'synchronize': {
            'icon': '/static/icons/synchronize.png',
            'label': 'synchronize',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedId = inst.get_node(obj.reference).id;
                var clickedType = inst.get_node(obj.reference).type;
                var all_tree_object = [{'clickedId': clickedId, 'clickedType': clickedType}];
                var data = $("#jstree").jstree(true)._model.data;
                for (i in data) {
                    if (i !== "#") {
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
                console.log(JSON.stringify(all_tree_object));
                $.ajax({
                    type: "POST",
                    url: "/main/synchronizeTestSuite",
                    data: JSON.stringify(all_tree_object),
                    dataType: "json",
                    async: false,
                    success: function (result) {
                        if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
                        else{
                            alert("synchronize success!");
                        }
                    },
                    error: function (result) {
                        alert("synchronize error!");
                    }
                });
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
                        'text': ''
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
        //'addOracleCheck': {
        //    'label': 'addOracleCheck',
        //    'action': function (obj) {
        //        var inst = jQuery.jstree.reference(obj.reference);
        //        var clickedNode = inst.get_node(obj.reference);
        //        var newNode = inst.create_node(clickedNode,
        //            {
        //                'id': randomString(16),
        //                'type': 'testStep',
        //                'text': '',
        //                "a_attr": {
        //                    "test_type": "RB",
        //                    "test_object": "put test object here, for example:raw CDRs",
        //                    "test_limit": "sum(deduct_charge_amount)",
        //                    "test_limit_value": 0
        //                }
        //            },
        //            'last',
        //            function (node) {
        //                try {
        //                    node.text = "new testStep";
        //                    inst.edit(node);
        //                } catch (ex) {
        //                    setTimeout(function () {
        //                        inst.edit(node);
        //                    }, 0);
        //                }
        //            }, '');
        //    }
        //},
        'addOracleStep': {
            'icon': '/static/icons/testStep_database.png',
            'label': 'add Oracle Step',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepOracleExecute',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // oracle base
                            "step_param2": "",    // sql to execute
                            "step_param3": "",    // result save
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepOracleExecute', clickedNode.id);
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
        'addOracleCheck': {
            'icon': '/static/icons/testStep_dataAssert.png',
            'label': 'add Oracle check',
            'action': function (obj) {
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var nodeId = randomString(16);
                var newNode = inst.create_node(clickedNode,
                    {
                        'id': nodeId,
                        'type': 'testStepOracleCheck',
                        'text': '',
                        "a_attr": {
                            "step_param1": "",    // oracle base
                            "step_param2": "",    // predict result
                            "step_param3": "",    // check sql
                            "step_param4": "",
                            "step_param5": ""
                        }
                    },
                    'last',
                    function (node) {
                        addNode(nodeId, 'testStepOracleCheck', clickedNode.id);
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
                var inst = jQuery.jstree.reference(obj.reference);
                var clickedNode = inst.get_node(obj.reference);
                var result = deleteItem(clickedNode.id, clickedNode.type);
                if (result) {
                    inst.delete_node(obj.reference);
                }
            }
        }

    };
    //console.log(node);
//        if (node.parent == '#') { //如果是根节点
//            delete items.createmap;
    if (node.type == 'root') {
        delete items.addTestCase;
        delete items.delete;
        delete items.rename;
        delete items.addOracleStep;
        delete items.addFileStep;
        delete items.addOracleCheck;
        delete items.addWebInterfaceStep;
    } else if (node.type == 'testSuite') {
        delete items.addTestSuite;
        delete items.addOracleStep;
        delete items.addFileStep;
        delete items.addOracleCheck;
        delete items.addWebInterfaceStep;
    } else if (node.type == 'testCase') {
        delete items.addTestCase;
        delete items.addTestSuite;
    } else if (node.type.substr(0, 8) == 'testStep') {
        delete items.addTestSuite;
        delete items.addTestCase;
        delete items.addOracleStep;
        delete items.addOracleCheck;
        delete items.addFileStep;
        delete items.addWebInterfaceStep;
    } else {
        delete items.addTestSuite;
        delete items.addTestCase;
        delete items.delete;
        delete items.rename;
        delete items.addOracleStep;
        delete items.addOracleCheck;
        delete items.addFileStep;
        delete items.addWebInterfaceStep;
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
            if (result.resultCode == '302'){
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
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else{
                params = result.result;
            }
        },
        error: function (result) {
            alert("move node error!");
        }
    });
}

function copyNode(data) {
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
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else{
                params = result.result;
            }


        },
        error: function (result) {
            alert("copy node error!");
        }
    });
}

//function findParentsNode(id) { //ids 是子节点数组
//        var parents = [];
//        for (var i = 0; i < 3; i++) {
//            var parent_id = $("#jstree").jstree(true)._model.data[id].parent;
//            var parent_name = $("#jstree").jstree(true)._model.data[parent_id].text;
//            if (parent_id != "root") {
//                parents.push(parent_id, parent_name);
//                id = parent_id;
//            }
//            else {
//                break
//            }
//        }
//        return parents;
//    }

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

function setStepOracleExecute(dom) {
    var params;
    $.ajax({
        type: "GET",
        url: "/main/queryStepParam?stepType=testStepOracleExecute",
        async: false,
        success: function (result) {
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else{
                params = result.result;
            }
        },
        error: function (result) {
            alert("Get user params error!");
        }
    });
    var step_id = dom.id;
    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;
    var step_param3 = dom.a_attr.step_param3;

    var oraChoice = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择数据库:</div><div class='bc_field_select'><select id='step_param1' class='select_limit' name='step_param1' onchange='refreshTreeParam1();'>";
    var param1_choose_flag = false;
    for (i in params[0]) {
        if (params[0][i][1] == step_param1) {
            oraChoice += "<option value='" + params[0][i][1] + "' selected>" + params[0][i][1] + "</option>";
            param1_choose_flag = true;
        } else {
            oraChoice += "<option value='" + params[0][i][1] + "'>" + params[0][i][1] + "</option>"
        }
    }
    if (false == param1_choose_flag) {
        oraChoice += "<option value='' selected>";
    }
    oraChoice += "</select></div></div>";

    var oraResult = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择结果保存参数:</div><div class='bc_field_select'><select name='step_param2' class='select_limit' id='step_param2' onchange='refreshTreeParam2();'>";
    for (i in params[1]) {
        if (params[1][i][1] == step_param2) {
            oraResult += "<option value='" + params[1][i][1] + "' selected>" + params[1][i][1] + "</option>";
        } else {
            oraResult += "<option value='" + params[1][i][1] + "'>" + params[1][i][1] + "</option>"
        }
    }
    oraResult += "<option value='' selected>";

    oraResult += "</select></div></div>";

    var SQLinput = "<div style='width: 100%'><div class='bc_field_label'>请输入执行sql:</div><textarea onkeyup='refreshTreeParam3();' class='bc_field_textarea' name='editor1' id='step_param3'>" + step_param3;

    $("#testDetail").html("");
    $("#testDetail").append("<h2>数据库操作模块</h2>");
    $("#testDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'></input");
    $("#testDetail").append("<div id='aaaaa' style='width:90%'>" + oraChoice + oraResult + SQLinput);

    refreshTreeParam1();
    refreshTreeParam2();
    refreshTreeParam3();

}


function setStepFile(dom) {
    var params;
    $.ajax({
        type: "GET",
        url: "/main/queryStepParam?stepType=testStepFile",
        async: false,
        success: function (result) {
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else{
                params = result.result;
            }
        },
        error: function (result) {
            alert("Get user params error!");
        }
    });
    var step_id = dom.id;
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


    var FileContent = "<div style='width: 100%'><div class='bc_field_label'>请输入文件内容:</div><textarea placeholder='文件内容可以使用固定内容，或$()符号将预定参数包含，如$(server)。oracle查询结果内容默认以逗号分隔。' onkeyup='refreshTreeParam4();' class='bc_field_textarea' name='editor1' id='step_param4'>" + step_param4;

    $("#testDetail").html("");
    $("#testDetail").append("<h2>文件操作模块</h2>");
    $("#testDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'>");
    $("#testDetail").append("<div id='aaaaa' style='width:90%'>" + HostChoice + FileName + FilePath + FileContent);

    refreshTreeParam1();
    refreshTreeParam2();
    refreshTreeParam3();
    refreshTreeParam4();

}


function setStepOracleCheck(dom) {
    var params;
    $.ajax({
        type: "GET",
        url: "/main/queryStepParam?stepType=testStepOracleCheck",
        async: false,
        success: function (result) {
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else{
                params = result.result;
            }
        },
        error: function (result) {
            alert("Get user params error!");
        }
    });
    var step_id = dom.id;
    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;
    var step_param3 = dom.a_attr.step_param3;

    var oraChoice = "<div class='1' style='width:100%;float:left'><div class='bc_field_label'>请选择数据库:</div><div class='bc_field_select'><select id='step_param1' class='select_limit' name='step_param1' onchange='refreshTreeParam1();'>";
    var param1_choose_flag = false;
    for (i in params[0]) {
        if (params[0][i][1] == step_param1) {
            oraChoice += "<option value='" + params[0][i][1] + "' selected>" + params[0][i][1] + "</option>";
            param1_choose_flag = true;
        } else {
            oraChoice += "<option value='" + params[0][i][1] + "'>" + params[0][i][1] + "</option>"
        }
    }
    if (false == param1_choose_flag) {
        oraChoice += "<option value='' selected>";
    }
    oraChoice += "</select></div></div>";

    var oraCheck = "<div style='width: 100%'><div class='bc_field_label'>请输入验证结果:</div><textarea placeholder='在此输入oracle待验证结果。如期待多字段结果分别为1，2，3时，请输入1,2,3' onkeyup='refreshTreeParam2();' class='bc_field_textarea' name='editor1' id='step_param2' style='height: 15%'>" + step_param2 + "</textarea></div>";

    var SQLinput = "<div style='width: 100%'><div class='bc_field_label'>请输入执行sql:</div><textarea placeholder='如果SQL为多个时，请以分号分隔；以最后一个sql的结论为准' onkeyup='refreshTreeParam3();' class='bc_field_textarea' name='editor1' id='step_param3'>" + step_param3 + "</textarea></div>";

    $("#testDetail").html("");
    $("#testDetail").append("<h2>数据库断言模块</h2>");
    $("#testDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'></input");
    $("#testDetail").append("<div id='aaaaa' style='width:90%'>" + oraChoice + oraCheck + SQLinput);

    refreshTreeParam1();
    refreshTreeParam2();
    refreshTreeParam3();

}

function setStepWebInterface(dom) {
    var step_id = dom.id;
    var step_param1 = dom.a_attr.step_param1;
    var step_param2 = dom.a_attr.step_param2;

    var webServiceUrl = "<div style='width: 100%'><div class='bc_field_label'>请输入接口地址:</div><textarea placeholder='在此输入接口地址' onkeyup='refreshTreeParam1();' class='bc_field_textarea' name='editor1' id='step_param1' style='height: 10%'>" + step_param1 + "</textarea></div>";
    var webServiceBody = "<div style='width: 100%'><div class='bc_field_label'>请输入接口内容:</div><textarea placeholder='在此输入报文内容' onkeyup='refreshTreeParam2();' class='bc_field_textarea' name='editor1' id='step_param2'>" + step_param2 + "</textarea></div>";

    $("#testDetail").html("");
    $("#testDetail").append("<h2>webservice接口模块</h2>");
    $("#testDetail").append("<input id='testDetailId' hidden='hiddin' value='" + step_id + "'></input");
    $("#testDetail").append("<div id='aaaaa' style='width:90%'>" + webServiceUrl + webServiceBody);

    refreshTreeParam1();
    refreshTreeParam2();

}