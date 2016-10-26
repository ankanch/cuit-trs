//<!--用户自动注册 -->
//<script type = "text/javascript" >
function autoRegiste() {
    var commentsbaseurl = "/autoregiste";
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
        var commentsbaseurl = "/autoregiste";
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