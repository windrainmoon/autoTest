function moveMiddleline() {
    var leftChild = document.getElementById('treeDetail');
    var oLine = document.getElementById('line');
    var rightChild = document.getElementById('testCaseDetail');
    var parent = document.getElementById('box');

    oLine.onmousedown = function (ev) {
        var iEvent = ev || event;
        var dx = iEvent.clientX;//当你第一次单击的时候，存储x轴的坐标。//相对于浏览器窗口
        var leftWidth = leftChild.offsetWidth;
        var parentWidth = parent.offsetWidth;
        var oLineWidth = oLine.offsetWidth;
        var rightWidth = parentWidth - leftWidth - oLineWidth - 25;
        document.onmousemove = function (ev) {
            var iEvent = ev || event;
            var diff = iEvent.clientX - dx;//移动的距离（向左滑时为负数,右滑时为正数）
            if (100 < (leftWidth + diff) && 100 < (rightWidth - diff)) {
                //两个div的最小宽度均为100px
                leftChild.style.width = (leftWidth + diff) + 'px';
                rightChild.style.width = (rightWidth - diff) + 'px';
            }
        };
        document.onmouseup = function () {
            document.onmousedown = null;
            document.onmousemove = null;
        };
        return false;
    }
}


function changeScreen() {
    var leftChild = document.getElementById('treeDetail');
    var oLine = document.getElementById('line');
    var rightChild = document.getElementById('testCaseDetail');
    var parentEle = document.getElementById('box');
    if ($("#full-screen-btn").text() == "全屏显示") {
        parent.quan();

        leftWidth = leftChild.offsetWidth;
        parentWidth = parentEle.offsetWidth;
        oLineWidth = oLine.offsetWidth;
        rightWidth = parentWidth - leftWidth - oLineWidth - 25;
        leftChild.style.width = leftWidth + 'px';
        rightChild.style.width = rightWidth + 'px';

        $("#full-screen-btn").text("退出全屏");
    } else {
        parent.exitQ();

        leftWidth = leftChild.offsetWidth;
        oLineWidth = oLine.offsetWidth;
        // 缩小比较尴尬，实际缩小的比较慢，需要等一等
        setTimeout(function () {
            parentWidth = parentEle.offsetWidth;
            rightWidth = parentWidth - leftWidth - oLineWidth - 25;
            leftChild.style.width = leftWidth + 'px';
            rightChild.style.width = rightWidth + 'px';
        }, 300);

        $("#full-screen-btn").text("全屏显示");
    }
}

function GetTreeData(tree_item_id, tree_item_type) {
    var arrs = [];
    $.ajax({
        type: "GET",
        url: "/main/root.json?id=" + tree_item_id + "&type=" + tree_item_type,
        dataType: "json",
        async: false,
        success: function (result) {
            if (result.resultCode == '302') {
                top.location.href = result.result;
            } else if (result.resultCode != '200') {
                alert("load error!");
            } else {
                var arrays = result.result;
                for (var i = 0; i < arrays.length; i++) {
                    var arr = {
                        "id": arrays[i].id,
                        "parent": arrays[i].parent,
                        "text": arrays[i].text,
                        "type": arrays[i].type,
                        "children": arrays[i].children,
                        "a_attr": {
                            "step_param1": arrays[i].step_param1,
                            "step_param2": arrays[i].step_param2,
                            "step_param3": arrays[i].step_param3,
                            "step_param4": arrays[i].step_param4,
                            "step_param5": arrays[i].step_param5
                        }
                    };
                    arrs.push(arr);
                }
            }
        },
        error: function (xhr, state, errorThrown) {
            console.log(xhr, state, errorThrown)
        }
    });
    return arrs
}

function searchTree() {
    var to = false;
    $('#search_input').keyup(function () {
        if (to) {
            clearTimeout(to);
        }
        to = setTimeout(function () {
            $('#jstree').jstree(true).search($('#search_input').val());

        }, 250);
    });
}

// $('#jstree').on('hover_node.jstree', function (e, data) { //鼠标移上事件
//         var id = data.node.a_attr.id;
//         var item = document.getElementById(id);
//         item.style.display='inline';            });
// $('#jstree').on('dehover_node.jstree', function (e, data) {
//             //监听鼠标移出事件
//             var id = data.node.a_attr.id;
//         var item = document.getElementById(id);
//         item.style.display='inline-block';            });