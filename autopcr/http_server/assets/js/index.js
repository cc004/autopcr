function register() {
    document.getElementById('card-index').style.pointerEvents = 'none';
    $.ajax({
        url: "/daily/api/config?account=" + $("#account").val(),
        type: "post",
        contentType: "application/json;charset=utf-8",
        data: JSON.stringify({
            username: "",
            password: "",
            alian: "",
            qq: ""
        }),
        processData: false,
        success: function (ret) {
            alert("注册成功。")
            login();
        },
        error: function (ret) {
            alert(ret.responseText);
            document.getElementById('card-index').style.pointerEvents = 'auto';
        }
    });
}
function login() {
    document.getElementById('card-index').style.pointerEvents = 'none';
    let account = $("#account").val()
    $.ajax({
        url: "/daily/api/login?account=" + account,
        type: "get",
        processData: false,
        success: function (ret) {
            window.location.href = "/daily/config.html?account=" + account;
        },
        error: function (ret) {
            alert("账号无效或不存在，第一次使用请先注册。\n如需帮助，请联系管理员。\n" + ret.responseText);
            document.getElementById('card-index').style.pointerEvents = 'auto';
        }
    });
}
document.addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        login();
    }
});