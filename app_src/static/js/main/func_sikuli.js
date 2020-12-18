/**
 * Created by Administrator on 2020/7/15.
 */


function setGUITable(dom) {
    var step_id = dom.id;
    $.ajax({
        type: "GET",
        url: "/main/queryGUIParam?param_tree_id=" + step_id,
        dataType: "json",
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else if (result.resultCode == '200') {
                $("#testCaseDetail").html("");
                $("#testCaseDetail").append("<form id='testDetail'></form>");
                $("#testDetail").append("<h2>GUI测试配置</h2>");
                $("#testDetail").append("<input class='button round' type='button' onchange='changeInputValue(this)' onclick='synGUIParam(\"" + step_id + "\")' value='同步'/>");
                var td = "<table id='content' class='fl-table'><tr><th class='td_Num'>序号</th><th class='td_Item' style='min-width: 80px'>步骤类型</th><th class='td_Item'>对象</th><th class='td_Item'>参数值</th><th class='td_Item' style='min-width: 55px'>是否可忽略</th><th class='td_Oper' style='min-width: 70px'>相关操作 <a href='#' onclick='gui_add_line();'>添加</a></th></tr>";
                td += result.result;
                $("#testDetail").append(td);

                max_line_num = $("#content tr:last-child").children("td").html();
                for (i = 1; i <= parseInt(max_line_num); i++) {
                    listenPaste(i);
                }
            } else {
                alert('get param error! resultCode = ' + result.resultCode);
            }
        },
        error: function (result) {
            alert("获取用户参数异常！" + result.result);
        }
    });
}


var currentStep = 0;
var max_line_num = 0;

//添加新记录
function gui_add_line() {
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
        // "<option value='environment'>environment</option>" +
        "<option value='openApp'>openApp</option>" +
        "<option value='wait'>wait</option>" +
        "<option value='input'>input</option>" +
        "<option value='click'>click</option>" +
        "<option value='closeApp'>closeApp</option>" +
        "</select></td>" +
        "<td class='td_Item' style='text-align: left;'><input type='text' onchange='changeInputValue(this)' name='pasteInput' placeholder='截屏后粘贴到输入框中' size='17'/></div>\n" +
        "<div class='img' style='padding: 0px;'></div>" +
        "<input name='x' hidden='hidden' value='0'/>" +
        "<input name='y' hidden='hidden' value='0'/>" +
        "<input name='xo' hidden='hidden' value='0'/>" +
        "<input name='yo' hidden='hidden' value='0'/>" +
        "<input name='picSrc' hidden='hidden' value=''/>" +
        "</td>" +

        "<td class='td_Item'><input type='text' onchange='changeInputValue(this)' name='param_value' value=''></td>" +
        "<td class='td_Item'><select type='text' name='is_pass'><option value='0'>no</option><option value='1'>yes</option></select></td>" +
        "<td class='td_Oper'>" +
        "<span onclick=\"gui_up_exchange_line($(this).parent().parent().find('td:first-child').html());\"> 上移 </span> " +
        "<span onclick=\"gui_down_exchange_line($(this).parent().parent().find('td:first-child').html());\"> 下移 </span> " +
        "<span onclick=\"gui_insert_onTheLine($(this).parent().parent().find('td:first-child').html());\"> 上插 </span> " +
        "<span onclick='gui_remove_line(this);'> 删除 </span> " +
        "</td>" +
        "</tr>");

    listenPaste(max_line_num);
}

function listenPaste(line_num) {
    var point = $('#line' + line_num + " td:nth-child(3)"),
        pasteInput = point.children('input[name=pasteInput]');
    if (pasteInput[0]) {
        pasteInput[0].addEventListener('paste', function (e) {
            var clipboardData = e.clipboardData,
                i = 0,
                items, item, types;
            if (clipboardData) {
                items = clipboardData.items;
                if (!items) {
                    return;
                }
                item = items[0];
                types = clipboardData.types || [];
                for (; i < types.length; i++) {
                    if (types[i] === 'Files') {
                        item = items[i];
                        break;
                    }
                }
                if (item && item.kind === 'file' && item.type.match(/^image\//i)) {
                    imgReader(point, item);
                }
            }
        });
    }
    background = point.children('div');
    var myImage = background.children('img')[0];
    if (myImage) {
        myImage.onclick = function (e) {
            var currWidth = myImage.clientWidth;
            var currHeight = myImage.clientHeight;
            // alert("图片高度："+currHeight);
            // alert("图片宽度："+currWidth);
            // var ProportionWidthInImg = x / currWidth;
            // var ProportionHeightInImg = y / currHeight;
            // alert("图片比例高度："+ProportionHeightInImg);
            // alert("图片比例宽度："+ProportionWidthInImg);
            e = e || window.event;
            x = e.offsetX || e.layerX;
            y = e.offsetY || e.layerY;
            innerX = x - currWidth / 2;
            innerY = y - currHeight / 2;
            createMarker(point, x, y, innerX, innerY);
        };
    }
}


var imgReader = function (point, item) {
    var background = point.children('div'),
        image = background.children('img'),
        picSrc = point.children('input[name=picSrc]'),
        px = point.children('input[name=x]'),
        py = point.children('input[name=y]'),
        xo = point.children('input[name=xo]'),
        yo = point.children('input[name=yo]');

    var blob = item.getAsFile(),
        reader = new FileReader();

    if (image[0]) {
        image[0].parentElement.removeChild(image[0]);

        px[0].setAttribute("value", 0);
        py[0].setAttribute("value", 0);
        xo[0].setAttribute("value", 0);
        yo[0].setAttribute("value", 0);
        // picSrc[0].value = "";
    }

    reader.onload = function (e) {
        var img = new Image();
        img.src = e.target.result;
        img.name = name;
        img.onclick = function (e) {
            myImg = background.children('img')[0];
            var currWidth = myImg.clientWidth;
            var currHeight = myImg.clientHeight;

            // alert("图片高度："+currHeight);
            // alert("图片宽度："+currWidth);
            // var ProportionWidthInImg = x / currWidth;
            // var ProportionHeightInImg = y / currHeight;
            // alert("图片比例高度："+ProportionHeightInImg);
            // alert("图片比例宽度："+ProportionWidthInImg);

            e = e || window.event;
            var px = e.offsetX || e.layerX,
                py = e.offsetY || e.layerY,
                innerX = px - currWidth / 2,
                innerY = py - currHeight / 2;
            console.log('init1', px, py, innerX, innerY)
            createMarker(point, px, py, innerX, innerY);
        };
        img.onload = function () {
            if (px[0].value == 0 && py[0].value == 0 && xo[0].value == 0 && yo[0].value == 0) {
                console.log('init2', img.clientWidth / 2, img.clientHeight / 2, 0, 0)
                // if picture initial, show 0,0
                createMarker(point, img.clientWidth / 2, img.clientHeight / 2, 0, 0);
            } else {
                console.log('init3', px[0].value, py[0].value, xo[0].value, yo[0].value)
                createMarker(point, px[0].value, py[0].value, xo[0].value, yo[0].value);
            }
            picSrc[0].setAttribute('value', img.src);
        };
        background[0].appendChild(img);
    };
    reader.readAsDataURL(blob);
};


function createMarker(point, x, y, innerX, innerY) {
    var background = point.children('div'),
        marker = background.children('div');
    px = point.children('input[name=x]');
    py = point.children('input[name=y]');
    xo = point.children('input[name=xo]');
    yo = point.children('input[name=yo]');
    if (marker[0]) {
        marker[0].parentElement.removeChild(marker[0]);
    }
    var div = document.createElement('div');
    div.className = 'marker';
    div.style.left = x + 'px';
    div.style.top = y + 'px';
    div.style.padding = 0;
    background[0].appendChild(div);
    px[0].setAttribute("value", x);
    py[0].setAttribute("value", y);
    xo[0].setAttribute("value", innerX);
    yo[0].setAttribute("value", innerY);
}

//上移
function gui_up_exchange_line(index) {
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

    listenPaste(upStep);
    listenPaste(currentStep);

    $('#content tr').each(function () {
        $(this).css("background-color", "#e2e2e2");
    });
    $('#line' + upStep).css("background-color", "yellow");
    //event.stopPropagation(); //阻止事件冒泡
}

function gui_insert_onTheLine(index) {
    gui_add_line();
    max_line_num = $("#content tr:last-child").children("td").html();
    for (var i = parseInt(max_line_num); i > index; i--) {
        gui_up_exchange_line(i);
    }
}

//下移
function gui_down_exchange_line(index) {
    max_line_num = $("#content tr:last-child").children("td").html();
    if (index != null) {
        currentStep = index;
        //currentStep = $(index).parent().parent().find("td:first-child").html();   //when gui_down_exchange_line(this)
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
    // console.log('down', currentStep, nextStep);
    //修改序号
    $('#line' + nextStep + " td:first-child").html(currentStep);
    $('#line' + currentStep + " td:first-child").html(nextStep);
    //取得两行的内容
    var nextContent = $('#line' + nextStep).html();
    var currentContent = $('#line' + currentStep).html();
    //交换当前行与上一行内容
    $('#line' + nextStep).html(currentContent);
    $('#line' + currentStep).html(nextContent);

    listenPaste(nextStep);
    listenPaste(currentStep);

    $('#content tr').each(function () {
        $(this).css("background-color", "#ffffff");
    });
    $('#line' + nextStep).css("background-color", "yellow");
    //event.stopPropagation(); //阻止事件冒泡
}

//删除选择记录
function gui_remove_line(index) {
    max_line_num = $("#content tr:last-child").children("td").html();
    last_line = document.getElementById("line" + max_line_num);

    if (index != null) {
        currentStep = $(index).parent().parent().find("td:first-child").html();
    }
    if (currentStep === 0) {
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
        //             if (i == 0) {
        //                 console.log($(this));
        //                 $(this).html(seq - 1);
        //                 $(this).id = 'line' + (seq - 1)
        //             }
        //
        //         });
        //     }
        // });
    }
}

function synGUIParam(id) {
    //console.log($('#testDetail'));
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/main/synGUIParam?param_tree_id=" + id,
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
    // setParamTable({"id": id});
}
