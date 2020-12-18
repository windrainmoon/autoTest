/**
 * Created by Administrator on 2020/7/15.
 */


function setParamTable(dom) {
    var step_id = dom.id;
    $.ajax({
        type: "GET",
        url: "/main/queryUserParam?param_tree_id=" + step_id,
        dataType: "json",
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else if (result.resultCode == '200') {
                $("#testCaseDetail").html("");
                $("#testCaseDetail").append("<form id='testDetail'></form>");
                if (step_id.slice(0, 4) == 'root') {
                    $("#testDetail").append("<h2>用户公共参数配置</h2>");
                } else {
                    $("#testDetail").append("<h2>业务参数配置</h2>");
                }
                $("#testDetail").append("<input class='button round' type='button' onclick='synchronizeParam(\"" + step_id + "\")' value='同步'/>");
                $("#testDetail").append("<div class=\"help-tip tip-left\">" +
                    "<p>系统默认参数：<br>random:生成随机字符，默认长度为8，形式如$(random)<br>" +
                    "sysdate:生成当前时间，形式如$(sysdate)，结果如2020-08-20 11:12:13</p>" +
                    "</div>");
                //var td = "<table name='userParams' id='userParams' class='paramTable' style='margin: 0px auto;'>" +
                //    "<th style='width:150px'>参数类型</th><th style='width:200px'>参数名称</th><th style='width:220px'>参数值</th><th style='width:150px'>操作</th>";
                var td = "<table id='content' class='fl-table'><tr><th class='td_Num'>序号</th><th class='td_Item'>参数类型</th><th class='td_Item'>参数名称</th><th class='td_Item'>参数值</th><th class='td_Oper'>相关操作 <a href='#' onclick='add_line();'>添加</a></th></tr>";
                td += result.result;
                $("#testDetail").append(td);
            } else {
                alert('get param error! resultCode = ' + result.resultCode);
            }
        },
        error: function (result) {
            alert("获取用户参数异常！" + result.result);
        }
    });
}

//function deleteParam(id) {
//    id.remove();
//}

var currentStep = 0;
var max_line_num = 0;

//添加新记录
function add_line() {
    max_line_num = $("#content tr:last-child").children("td").html();
    if (max_line_num == null) {
        max_line_num = 1;
    } else {
        max_line_num = parseInt(max_line_num);
        max_line_num += 1;
    }
    $('#content').append(
        "<tr id='line" + max_line_num + "'>" +
        "<td class='td_Num'>" + max_line_num + "</td>" +
        "<td class='td_Item'><select name='param_type'>" +
        "<option value='string'>string</option>" +
        "<option value='linux'>linux</option>" +
        "<option value='cmd'>cmd</option>" +
        "<option value='db_oracle'>db_oracle</option>" +
        "<option value='db_gmdb'>db_gmdb</option>" +
        "<option value='db_mysql'>db_mysql</option>" +
        "<option value='sql_result'>sql_result</option>" +
        "</select></td>" +
        "<td class='td_Item'><input type='text' name='param_name' value='' onchange='changeInputValue(this)'></td>" +
        "<td class='td_Item'><input type='text' name='param_value' value='' onchange='changeInputValue(this)'></td>" +
        "<td class='td_Oper'>" +
        "<span onclick=\"up_exchange_line($(this).parent().parent().find('td:first-child').html());\"> 上移 </span> " +
        "<span onclick=\"down_exchange_line($(this).parent().parent().find('td:first-child').html());\"> 下移 </span> " +
        "<span onclick=\"insert_onTheLine($(this).parent().parent().find('td:first-child').html());\"> 上插 </span> " +
        "<span onclick='remove_line(this);'> 删除 </span> " +
        "</td>" +
        "</tr>");
}

//删除选择记录
function remove_line(index) {
    max_line_num = $("#content tr:last-child").children("td").html();
    last_line = document.getElementById("line" + max_line_num);
    if (index != null) {
        currentStep = $(index).parent().parent().find("td:first-child").html();
    }
    if (currentStep == 0) {
        alert('请选择一项!');
        return false;
    }
    if (confirm("确定要删除改记录吗？")) {
        if (currentStep === max_line_num) {
            last_line.remove();
        } else {
            for (var i = currentStep; i < parseInt(max_line_num); i++) {
                gui_down_exchange_line(i);
            }
            last_line.remove();
        }

        // $("#content tr").each(function () {
        //     var seq = parseInt($(this).children("td").html());
        //     if (seq == currentStep) {
        //         $(this).remove();
        //     }
        //     if (seq > currentStep) {
        //         $(this).children("td").each(function (i) {
        //             if (i == 0) $(this).html(seq - 1);
        //         });
        //     }
        // });
    }
}

//上移
function up_exchange_line(index) {
    if (index != null) {
        //currentStep = $(index).parent().parent().find("td:first-child").html();
        currentStep = index;
    }
    if (currentStep == 0) {
        alert('请选择一项!');
        return false;
    }
    if (currentStep <= 1) {
        alert('已经是最顶项了!');
        return false;
    }
    var upStep = currentStep - 1;
    //修改序号
    $('#line' + upStep + " td:first-child").html(currentStep);
    $('#line' + currentStep + " td:first-child").html(upStep);
    //取得两行的内容
    var upContent = $('#line' + upStep).html();
    var currentContent = $('#line' + currentStep).html();
    $('#line' + upStep).html(currentContent);
    //交换当前行与上一行内容
    $('#line' + currentStep).html(upContent);
    $('#content tr').each(function () {
        $(this).css("background-color", "#e2e2e2");
    });
    $('#line' + upStep).css("background-color", "yellow");
    //event.stopPropagation(); //阻止事件冒泡
}

function insert_onTheLine(index) {
    add_line();
    max_line_num = $("#content tr:last-child").children("td").html();
    for (var i = parseInt(max_line_num); i > index; i--) {
        up_exchange_line(i);
    }
}

//下移
function down_exchange_line(index) {
    max_line_num = $("#content tr:last-child").children("td").html();
    if (index != null) {
        currentStep = index;
        //currentStep = $(index).parent().parent().find("td:first-child").html();   //when down_exchange_line(this)
    }
    if (currentStep == 0) {
        alert('请选择一项!');
        return false;
    }
    if (currentStep >= max_line_num) {
        alert('已经是最后一项了!');
        return false;
    }
    var nextStep = parseInt(currentStep) + 1;
    console.log('down', currentStep, nextStep);
    //修改序号
    $('#line' + nextStep + " td:first-child").html(currentStep);
    $('#line' + currentStep + " td:first-child").html(nextStep);
    //取得两行的内容
    var nextContent = $('#line' + nextStep).html();
    var currentContent = $('#line' + currentStep).html();
    //交换当前行与上一行内容
    $('#line' + nextStep).html(currentContent);
    $('#line' + currentStep).html(nextContent);

    $('#content tr').each(function () {
        $(this).css("background-color", "#ffffff");
    });
    $('#line' + nextStep).css("background-color", "yellow");
    //event.stopPropagation(); //阻止事件冒泡
}

//保存数据
//function SaveData() {
//    var data = "<root>";
//    $('#content tr').each(function () {
//        data += "<item>";
//        var stepName = $(this).find("td:eq(1)").find("input").val();
//        var stepDescription = $(this).find("td:eq(2)").find("input").val();
//        data += "   <stepName>" + stepName + "</stepName>";
//        data += "   <stepDescription>" + stepDescription + "</stepDescription>";
//        data += "<item>";
//    });
//    data += "</root>";
//    alert(data);
//}

//function addNewParam() {
//    var id = randomString(10);
//    var table = document.getElementById("userParams");
//    var rowsNum = table.length;
//    var row = table.insertRow(rowsNum);
//    row.setAttribute('id', id);
//    var cell0 = row.insertCell(0);
//    cell0.innerHTML = "<select name='param_type'><option value='string'>string</option><option value='db'>db</option><option value='linux'>linux</option><option value='sql_result'>sql_result</option></select>";
//    var cell1 = row.insertCell(1);
//    cell1.innerHTML = "<input type='text' name='param_name' value=''>";
//    var cell2 = row.insertCell(2);
//    cell2.innerHTML = "<input type='text' name='param_value' value=''>";
//    var cell3 = row.insertCell(3);
//    cell3.innerHTML = "<input class='button round' type='button' onclick='deleteParam(" + id + ")' value='删除'/>";
//}

function synchronizeParam(id) {
    //console.log($('#testDetail'));
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/main/synchronizeParam?param_tree_id=" + id,
        data: $('#testDetail').serialize().replace(/\+/g, " "),
        success: function (result) {
//                console.log(result);//打印服务端返回的数据(调试用)
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else if (result.resultCode == 200) {
                alert("SUCCESS");
            }
        },
        error: function () {
            alert("异常！");
        }
    });
    sleep(1000);
    setParamTable({"id": id});
}

// function input2select() {
//     var wps = new Array();
//     var start = 0;
//     var pos = aa.indexOf('\n');
//
//     while (pos > -1) {
//         wps.push(aa.substr(start, pos - start));
//         start = pos + 1;
//         pos = aa.indexOf('\n', pos + 1);
//     }
// }