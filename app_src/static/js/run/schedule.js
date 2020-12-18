

function saveSchedule() {
    var suite_id = $("#suite_id").html();
    // console.log($('#scheduleForm').serialize());
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/run/synchronizeSchedule?suite_id=" + suite_id,
        data: $('#scheduleForm').serialize(),
        success: function (result) {
//                console.log(result);//打印服务端返回的数据(调试用)
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else if (result.resultCode == 200) {
                alert("SUCCESS!");
            }
        },
        error: function () {
            alert("异常！");
        }
    });
}

function addLine(rowData) {
        var table = document.getElementById("taskTable");
        var rowsNum = table.length;
        var row = table.insertRow(rowsNum);
        var cell0 = row.insertCell(0);
        cell0.innerHTML = rowData[1];
        var cell1 = row.insertCell(1);
        cell1.innerHTML = rowData[2];
        cell1.setAttribute("id", rowData[0] + 't');
        var cell2 = row.insertCell(2);
        cell2.innerHTML = "<progress id='" + rowData[0] + "p' max='100' value='" + rowData[3] + "'></progress>" +
            " <label id='" + rowData[0] + "l'>" + rowData[3] + "%</label>";
        var cell3 = row.insertCell(3);

        var res = "";
        if(rowData[3] >= 100){
            var temp = "showTestResult('" + rowData[0] + "')";
            res = '<input type="button" value="showResult" onclick=' + temp  + '>';
        }
        cell3.innerHTML = res;
        cell3.setAttribute("id", rowData[0] + 'd');
}

function showTestResult(runCaseId){
        window.open('showResult?runCaseId=' + runCaseId, 'testResult' + runCaseId, 'height=400, width=700, top=400, left=500, toolbar=no, menubar=no, scrollbars=no, resizable=no, location=no, status=no')
    }

function changeSchedule(suite_id) {
    if (suite_id == "root"){
        $("select[name='isRun']").val("");
                $("select[name='isSend']").val("");
                $("input[name='min']").val("");
                $("input[name='hour']").val("");
                $("input[name='day']").val("");
                $("input[name='month']").val("");
                $("input[name='week']").val("");
        $("#taskTable").html('<h2>欢迎来到执行计划配置模块，选择左侧的testSuite，即可展示最近3天的执行结果。对于不需要启用的任务请修改为不启动。</h2>');
        return
    }

    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/run/getSchedule?suite_id=" + suite_id,
        data: $('#scheduleForm').serialize(),
        success: function (result) {
//                console.log(result);//打印服务端返回的数据(调试用)
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else if (result.resultCode != '200'){
                    alert("load error!");
                }
            else{
                var res = result.result;
                // console.log(res);
                $("select[name='isRun']").val(res[0]);
                $("select[name='isSend']").val(res[1]);
                $("input[name='min']").val(res[2]);
                $("input[name='hour']").val(res[3]);
                $("input[name='day']").val(res[4]);
                $("input[name='month']").val(res[5]);
                $("input[name='week']").val(res[6]);
            }
        },
        error: function () {
            alert("异常！");
        }
    });

    $("#taskTable").html();
    $("#taskTable").html("<table id='taskTable' class='taskTable' style=\"float: right;width: 100%\">\n" +
        "                <tr>" +
        "                    <th style=\"width: 45%\">testCaseName</th>\n" +
        "                    <th style=\"width:15%\">test time</th>\n" +
        "                    <th style=\"width:30%\">test progress</th>\n" +
        "                    <th style=\"width: 10%\">查看结果</th>\n" +
        "                </tr>");
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/run/getRunLog?suite_id=" + suite_id,
        // data: $('#scheduleForm').serialize(),
        success: function (result) {
//                console.log(result);//打印服务端返回的数据(调试用)
            if (result.resultCode == '302'){
                            top.location.href = result.result;
                        }
            else if (result.resultCode == 200) {
                for (row in result.result){
                    addLine(result.result[row]);
                }
            }
        },
        error: function () {
            alert("异常！");
        }
    });
}

