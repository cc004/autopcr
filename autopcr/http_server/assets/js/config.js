const iframeActionID = 'iframe-action'
const iframeInfoID = 'iframe-info'
const toastContainerID = 'toast-container-1'
const configFormID = ['form-normal-config', 'form-account-config'];
$(document).ready(function () {
    document.getElementById('card-main').style.pointerEvents = 'none';
    ready_get_info(true)
    $(`#${iframeActionID}`).attr('src', 'action.html' + window.location.search);
    $(`#${iframeInfoID}`).attr('src', 'info.html' + window.location.search);
    document.getElementById('card-main').style.pointerEvents = 'auto';
}
);
function ready_get_info(toggle) {
    document.getElementById('main-tab-content').style.pointerEvents = 'none';
    $.ajax({
        url: `/daily/api/${jinjaUrlConfig}` + window.location.search,
        type: "get",
        processData: false,
        success: function (ret) {
            $("#input-alian").val(ret.alian);
            $("#input-qqnum").val(ret.qq);
            $("#input-uname").val(ret.username);
            $("#input-upwd").val(ret.password);
            if ((ret.username || ret.alian) && toggle) {
                $("#tab-main a[href='#tab-2']").tab("show");
            } else {
                $("tab-main a[href='#tab-1']").tab("show");
            }
            document.getElementById('main-tab-content').style.pointerEvents = 'auto';
        },
        error: function (ret) {
            document.getElementById('card-main').style.pointerEvents = 'none';
            show_toast('error', '获取个人信息失败。', `${ret.responseText}`);
        },
    });
}
function updateElementHeight() {
    var viewportHeight = window.innerHeight;
    var elementPos = document.getElementById('tab-items').getBoundingClientRect().bottom;
    var result = viewportHeight - elementPos - 73;
    document.getElementById(iframeActionID).style.height = result + 'px';
    document.getElementById(iframeInfoID).style.height = result + 'px';
}
window.onresize = updateElementHeight;
window.onload = updateElementHeight;
var themeDropdownItems = document.querySelectorAll("#themeDropdown + .dropdown-menu a");
var childWindowAction = $(`#${iframeActionID}`)[0].contentWindow;
var childWindowInfo = $(`#${iframeInfoID}`)[0].contentWindow;
themeDropdownItems.forEach(function (item) {
    item.addEventListener("click", function (event) {
        var themeValue = this.getAttribute("data-bs-theme-value");
        childWindowAction.document.body.setAttribute("data-bs-theme", themeValue);
        childWindowInfo.document.body.setAttribute("data-bs-theme", themeValue);
    });
});
function toggle_spinner(status = 'hidden', element) {
    let spanEl = $(element).children("span.spinner-border")
    switch (status) {
        case 'hidden':
            if (!(spanEl.hasClass("visually-hidden"))) {
                spanEl.addClass("visually-hidden")
            }
            break;
        case 'show':
            if (spanEl.hasClass("visually-hidden")) {
                spanEl.removeClass("visually-hidden")
            }
            break
        default:
            spanEl.addClass("visually-hidden")
            break;
    }
};
function show_toast(status, text, desc = null) {
    const classDict = {
        'success': [`text-success-emphasis`, `bg-success-subtle`, `border-success-subtle`],
        'info': [`text-info-emphasis`, `bg-info-subtle`, `border-info-subtle`],
        'warning': [`text-warning-emphasis`, `bg-warning-subtle`, `border-warning-subtle`],
        'error': [`text-danger-emphasis`, `bg-danger-subtle`, `border-danger-subtle`],
    }
    let date = new Date();
    if (desc != null) {
        desc = desc.replace(/\n/g, '<br>')
        var res = `<div id="toast" class="toast" role="alert">
        <div class="toast-header">
        <strong class="me-auto">${text}</strong>
        <small>${date.toLocaleTimeString('en-US', { hour12: false })}</small>
        <button class="btn-close ms-2 mb-1 close" type="button" aria-label="Close" data-bs-dismiss="toast"></button></div>
        <div class="toast-body" role="alert">
        <p>${desc}</p>
        </div></div>`
    } else {
        var res = `<div id="toast" class="toast" role="alert">
        <div class="toast-body d-flex align-items-center" role="alert" style="padding: var(--bs-toast-padding-y) var(--bs-toast-padding-x);">
        <strong class="me-auto">${text}</strong>
        <small>${date.toLocaleTimeString('en-US', { hour12: false })}</small>
        <button class="btn-close ms-2 mb-1 close" type="button" aria-label="Close" data-bs-dismiss="toast" style="margin-right: calc(-.5 * var(--bs-toast-padding-x));"></button>
        </div></div>`;
    }
    if (status in classDict) {
        var classNames = classDict[status];
    } else {
        var classNames = classDict['info'];
    }
    let parser = new DOMParser();
    let toastElement = parser.parseFromString(res, 'text/html').getElementById('toast');
    for (let i = 0; i < classNames.length; i++) {
        toastElement.classList.add(classNames[i]);
    }
    document.getElementById(toastContainerID).appendChild(toastElement);
    let toast = new bootstrap.Toast(toastElement);
    toast.show()
    toastElement.addEventListener('hidden.bs.toast', function () {
        toastElement.parentNode.removeChild(toastElement);
    });
}
function delete_config() {
    let element = $("#delete_config")
    element.attr('disabled', true);
    toggle_spinner('show', element[0])
    document.getElementById('card-main').style.pointerEvents = 'none';
    $.ajax({
        url: '/daily/api/config' + window.location.search,
        type: 'delete',
        processData: false,
        success: function (ret) {
            show_toast('success', "删除账号成功。")
            toggle_spinner('hidden', element[0])
            window.location.href = "/daily/";
        },
        error: function (ret) {
            show_toast('error', "删除账号失败。", ret.responseText)
            toggle_spinner('hidden', element[0])
            element.attr('disabled', false);
            document.getElementById('card-main').style.pointerEvents = 'auto';
        }
    })
}
function update_info() {
    let config = {};
    document.getElementById('main-tab-content').style.pointerEvents = 'none';
    config['alian'] = $("#input-alian").val();
    config['qq'] = $("#input-qqnum").val();
    config['username'] = $("#input-uname").val();
    config['password'] = $("#input-upwd").val();
    $.ajax({
        url: `/daily/api/${jinjaUrlConfig}` + window.location.search,
        type: "put",
        data: JSON.stringify(config),
        contentType: "application/json;charset=utf-8",
        processData: false,
        success: function (ret) {
			show_toast('success', '本次修改保存成功。')
        },
        error: function (ret) {
            show_toast('error', '本次修改保存失败。', `将于三秒后刷新页面，如有需要请联系管理员。\n${ret.responseText}`);
            setTimeout(function() {
                location.reload(true);
            }, 3000);
        },
    });
}
function reset_config_form() {
    configFormID.forEach(function (item) {
        document.getElementById(item).reset();
    });
}
