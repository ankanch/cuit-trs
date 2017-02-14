//<!--用户自动注册 -->
//<script type = "text/javascript" >
function autoRegiste() {
    var commentsbaseurl = "/trs/autoregiste";
    $.get(commentsbaseurl, function(data) {
        if (data != "NULL") {
            return data
        }
    });
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=")
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1
            c_end = document.cookie.indexOf(";", c_start)
            if (c_end == -1) c_end = document.cookie.length
            return unescape(document.cookie.substring(c_start, c_end))
        }
    }
    return ""
}

function setCookie(c_name, value, expiredays) {
    var exdate = new Date()
    exdate.setDate(exdate.getDate() + expiredays)
    document.cookie = c_name + "=" + escape(value) +
        ((expiredays == null) ? "" : "; expires=" + exdate.toGMTString())
}

function getUID() {
    uid = getCookie('uid')
    if (uid != null && uid != "" && uid != "undefined	" && uid != "undefined") { return uid } else {
        var commentsbaseurl = "/trs/autoregiste";
        $.get(commentsbaseurl, function(data) {
            if (data != "NULL") {
                setCookie('uid', data, 365)
                return data
            }
        });
    }
}

//</script>


function copyToClipBoard(data) {
    var clipBoardContent = data;
    window.clipboardData.setData("Text", clipBoardContent);
}

function getusertable(userlist) {
    var usertable = "";
    TABLE_HEAD = "<tr> <td > "
    TABLE_MID_A = "</td> <td > "
    TABLE_MID_B = "</td> <td >"
    TABLE_MID_C = "</td> <td > "
    TABLE_TAIL = "</td> </tr>"
    userd = userlist.split(",");
    var i = 0;
    for (var user in userd) {
        pu = user.split(":");
        pmd = TABLE_HEAD + i.toString() + TABLE_MID_A + pu[0] + TABLE_MID_B + pu[1] + TABLE_MID_C + pu[2] + TABLE_TAIL;
        i++;
        usertable += pmd;
    }
    return usertable;
}

function getabout() {
    var abouttext = "<div style=\"width:65%;margin: 0 auto\">" +
        "    <div class=\"modal\">" +
        "        <div class=\"modal-dialog\">" +
        "            <div class=\"modal-content\">" +
        "                <div class=\"modal-header\">" +
        "                    <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\" onclick=\"javascript:toggleDiv(\'infodiv\');\">×</button>" +
        "                    <h4 class=\"modal-title\">关于成信助手-CUIT Helper- LUV201702132302</h4>" +
        "                </div>" +
        "                <div class=\"modal-body\">" +
        "                    <p>该站点的目的呢，就是没事做着玩。目前拥有以下功能：</p>" +
        "                    <p>成信好老师：从老师的教学风格，严格程度等方面评价老师。你的任何评价都有可能成为日后其它学生选课的依据。</p>" +
        "                    <p>成信贴吧大数据：可以对我们学校的贴吧进行一些简单的分析，包括用户维度和贴吧维度的分析。</p>" +
        "                    <p>成信匿名墙：匿名说出你想说的任何东西，在保证真实的情况下，分享给更多人的获得大家的支持与讨论。</p>" +
        "                    <p>目前项目已经开源，欢迎参与贡献，issues页面：<a href=\"https://github.com/ankanch/cuit-trs/issues\" target=\"_blank\">https://github.com/ankanch/cuit-trs/issues</a></p>" +
        "                </div>" +
        "                <div class=\"modal-footer\">" +
        "                    <button type=\"button\" class=\"btn btn-primary\">by Kanch</button>" +
        "                </div>" +
        "            </div>" +
        "        </div>" +
        "    </div>" +
        "</div>";
    return abouttext;
}

function getfooter() {
    var footertext = [" <br/><br/><p class=\"text-info\">hcnak \'s stcejorp © 2017 All Rights Reserved </p>"].join("");
    var uptimecode = "<a href=\"http://www.host-tracker.com/UptimeGraph/UptimeInfo/bc6eac20-39a0-4ae9-9dfa-03c270b358cd\" target=\'_blank\'>";
    uptimecode += "<img id=\'HostTrackerInformer\' width=\'80\' height=\'15\' border=\'0\' title=\'Check is site down - Website monitoring service Host-tracker.com\' alt=\'Check is site down - Website monitoring service Host-tracker.com\' src=\"//i.h-t.co/test website.png?id=bc6eac20-39a0-4ae9-9dfa-03c270b358cd\" /></a>";
    return footertext + uptimecode;
}