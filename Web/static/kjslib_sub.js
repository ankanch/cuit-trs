String.prototype.replaceAt = function(index, character) {
    return this.substr(0, index) + character + this.substr(index + character.length);
}

function subscrible() {
    stype = "00000000000000";
    if (document.getElementById('agreeagreement').checked == false) {
        $.snackbar({
            content: "请同意我们的服务协议！"
        });
        return;
    }
    //获取邮件地址
    email = document.getElementById('inputEmail').value;
    //获取订阅类型
    if (document.getElementById('sub_xueshu').checked == true) { stype = stype.replaceAt(0, "1"); }
    if (document.getElementById('sub_wenhua').checked == true) { stype = stype.replaceAt(1, "1"); }
    if (document.getElementById('sub_zonghe').checked == true) { stype = stype.replaceAt(2, "1"); }
    if (document.getElementById('sub_jiaodian').checked == true) { stype = stype.replaceAt(3, "1"); }
    if (document.getElementById('sub_xingxi').checked == true) { stype = stype.replaceAt(4, "1"); }
    if (document.getElementById('sub_gongzuo').checked == true) { stype = stype.replaceAt(5, "1"); }
    if (stype.indexOf("1") == -1) {
        $.snackbar({
            content: "请选择您要订阅的新闻！"
        });
        return;
    }
    console.log(email + "," + stype);
    //请求添加订阅
    $.snackbar({
        content: "订阅中..."
    });
    $.get("/subscrible/" + email + "/" + stype, function(data) {
        $.snackbar({
            content: data
        });
        toggleDiv('subscriable')
    });
}