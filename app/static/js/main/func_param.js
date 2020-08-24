/**
 * Created by Administrator on 2020/7/15.
 */


function setParamTable() {
    $.ajax({
        type: "GET",
        url: "/main/queryUserParam?type=root",
        dataType: "json",
        async: false,
        success: function (result) {
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else if (result.resultCode == '200') {
                $("#testDetail").html("");
                $("#testDetail").append("<h2>用户参数配置</h2>");
                $("#testDetail").append("<input class='button round' type='button' onclick='synchronizeParam()' value='同步'/>");
                //var td = "<table name='userParams' id='userParams' class='paramTable' style='margin: 0px auto;'>" +
                //    "<th style='width:150px'>参数类型</th><th style='width:200px'>参数名称</th><th style='width:220px'>参数值</th><th style='width:150px'>操作</th>";
                var td = "<table id='content' class='fl-table'><tr><th class='td_Num'>序号</th><th class='td_Item'>参数类型</th><th class='td_Item'>参数名称</th><th class='td_Item'>参数值</th><th class='td_Oper'>相关操作 <a href='#' onclick='add_line();'>添加</a></th></tr>";
                td += result.result;
                $("#testDetail").append(td);
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
        }
        else {
            max_line_num = parseInt(max_line_num);
            max_line_num += 1;
        }
        $('#content').append(
        "<tr id='line" + max_line_num + "'>" +
            "<td class='td_Num'>" + max_line_num + "</td>" +
            "<td class='td_Item'><select name='param_type'>" +
                    "<option value='string'>string</option>" +
                    "<option value='oracle'>oracle</option>" +
                    "<option value='linux'>linux</option>" +
                    "<option value='oracle_result'>oracle_result</option>" +
                    "</select></td>" +
            "<td class='td_Item'><input type='text' name='param_name' value=''></td>" +
            "<td class='td_Item'><input type='text' name='param_value' value=''></td>" +
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
        if (index != null) {
            currentStep = $(index).parent().parent().find("td:first-child").html();
        }
        if (currentStep == 0) {
            alert('请选择一项!');
            return false;
        }
        if (confirm("确定要删除改记录吗？")) {
            $("#content tr").each(function () {
                var seq = parseInt($(this).children("td").html());
                if (seq == currentStep) { $(this).remove(); }
                if (seq > currentStep) { $(this).children("td").each(function (i) { if (i == 0) $(this).html(seq - 1); }); }
            });
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
        $('#content tr').each(function () { $(this).css("background-color", "#ffffff"); });
        $('#line' + upStep).css("background-color", "yellow");
        //event.stopPropagation(); //阻止事件冒泡
    }

function insert_onTheLine(index){
    add_line();
    max_line_num = $("#content tr:last-child").children("td").html();
    for (var i=max_line_num;i>index;i--){
        console.log(i.toString());
        up_exchange_line(i.toString());
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
        //修改序号
        $('#line' + nextStep + " td:first-child").html(currentStep);
        $('#line' + currentStep + " td:first-child").html(nextStep);
        //取得两行的内容
        var nextContent = $('#line' + nextStep).html();
        var currentContent = $('#line' + currentStep).html();
        //交换当前行与上一行内容
        $('#line' + nextStep).html(currentContent);
        $('#line' + currentStep).html(nextContent);

        $('#content tr').each(function () { $(this).css("background-color", "#ffffff"); });
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
//    cell0.innerHTML = "<select name='param_type'><option value='string'>string</option><option value='oracle'>oracle</option><option value='linux'>linux</option><option value='oracle_result'>oracle_result</option></select>";
//    var cell1 = row.insertCell(1);
//    cell1.innerHTML = "<input type='text' name='param_name' value=''>";
//    var cell2 = row.insertCell(2);
//    cell2.innerHTML = "<input type='text' name='param_value' value=''>";
//    var cell3 = row.insertCell(3);
//    cell3.innerHTML = "<input class='button round' type='button' onclick='deleteParam(" + id + ")' value='删除'/>";
//}
var sleep = function(time) {
    var startTime = new Date().getTime() + parseInt(time, 10);
    while(new Date().getTime() < startTime) {}
};

function synchronizeParam() {
    //console.log($('#testDetail'));
    //console.log($('#testDetail').serialize());
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/main/synchronizeParam",
        data: $('#testDetail').serialize(),
        success: function (result) {
//                console.log(result);//打印服务端返回的数据(调试用)
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else if (result.resultCode == 200) {
                alert("SUCCESS");
            }
        },
        error: function () {
            alert("异常！");
        }
    });
    sleep(1000);
    setParamTable();

}