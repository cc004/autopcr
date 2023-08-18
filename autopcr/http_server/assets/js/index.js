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
    window.location.href = "/daily/config.html?account=" + $("#account").val();
}
document.addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        login();
    }
});