const rotate_class_name = 'rotate-icon'
var user_config = {}
var share_key = {}
$(document).ready(function () {
    $.ajax({
        url: `/daily/api/account/${account}/${jinjaUrl}` + window.location.search,
        type: "get",
        processData: false,
        success: function (ret) {
            let ta_tab = $("#card-stack");
            result = ret.last_result;
            user_config = ret.config;
            const data = ret.data;
            const module = ret.order;
            for (let i = 0; i < module.length; ++i) {
                let val = data[module[i]];
                ta_tab.append(make_card(val));
                switch_toggle_collapse(val.key)
            }
            load_results(module, result);
            _icon_rotate()
        },
        error: function (ret) {
            show_toast('error', '获取配置失败。', `${ret.responseText}`);
        },
    });
});
function show_toast(status, text, desc = null) {
    window.parent.show_toast(status, text, desc)
}
function show_validate(url) {
    window.parent.show_validate(url)
}
function _icon_rotate() {
    const buttons = document.querySelectorAll('.btn-icon');
    buttons.forEach(button => {
        const svg = button.querySelector('svg');
        button.addEventListener('click', () => {
            if (((button.getAttribute('aria-expanded') === 'false') && !(svg.classList.contains(rotate_class_name))) || ((button.getAttribute('aria-expanded') === 'true') && (svg.classList.contains(rotate_class_name)))) {
                svg.classList.toggle(rotate_class_name);
            };
        });
    });
}
function switch_toggle_collapse(switchID) {
    const _switch = document.getElementById(switchID);
    const button = document.querySelector(`[data-bs-toggle="collapse"][data-bs-target="#collapse-${switchID}"]`);
    _switch.addEventListener("change", function () {
        if (_switch.checked ^ (button.getAttribute('aria-expanded') == 'true')) {
            var clickEvent = new MouseEvent("click");
            button.dispatchEvent(clickEvent);
        }
    });
}
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
            break;
    }
};
function generate_config_HTML(config) {
    share_key[config.key] = (share_key[config.key] || 0) + 1;
    let configHTML = '';
    configHTML = `<div class="input-group input-group-sm" name=${config.key}_card><span class="text-start align-items-start input-group-text">${config.desc}</span>${generate_option_HTML(config)}</div>`
    return configHTML;
}
function generate_option_HTML(config) {
    switch (config.config_type) {
        case 'single':
            return get_single_html(config)
            break;
        case 'multi':
            return get_multi_html(config)
            break;
        case 'int':
            return get_int_html(config)
            break;
        case 'bool':
            return get_bool_html(config)
            break;
        case 'time':
            return get_time_html(config)
            break;
    }
}
function get_single_html(config) {
    let res = `<select id=${config.key} class="form-select" style="display:inline-block" name=${config.key} onchange="selectOnChange(this)">`
    for (let i = 0; i < config.candidates.length; i++) {
        res += `<option value='${config.candidates[i]}' ${user_config[config.key] == config.candidates[i] ? "selected" : ""}>${config.candidates[i]}</option>`;
    }
    res += "</select>";
    return res;
}
function get_multi_html(config) {
    let res = `<select id=${config.key} class="form-select" style="display:inline-block" multiple name=${config.key} onchange="selectMultiOnChange(this)">`;
    for (let i = 0; i < config.candidates.length; i++) {
        res += `<option value='${config.candidates[i]}' ${user_config[config.key].includes(config.candidates[i]) ? "selected" : ""}>${config.candidates[i]}</option>`;
    }
    res += "</select>";
    return res;
}
function get_int_html(config) {
    return `<input id=${config.key} class="form-control" style="display:inline-block" type="number" value=${user_config[config.key]} onchange="selectOnChange(this)" oninput="value=value.replace(/\D/g,&#39;&#39;)" name=${config.key} placeholder="${config.candidates[0]} ~ ${config.candidates[config.candidates.length - 1]}" oninput="value=value.replace(/\D/g,'')" />`;
}
function get_bool_html(config) {
    let res = `<div class="input-group-text form-control form-switch px-3" style="display:inline-block">`
    res += `<input id=${config.key} class="form-check-input m-0" type="checkbox" style="transform: scale(1.30);" name=${config.key} ${user_config[config.key] ? 'checked="checked"' : ""} onclick="checkboxOnclick(this)" /></div>`;
    return res
}
function get_time_html(config) {
    return `<input id=${config.key} class="form-control" style="display:inline-block" type="time" name=${config.key} value=${user_config[config.key]} onchange="selectOnChange(this)" />`;
}
function set_tag(status, element) {
    const classDict = {
        'success': [`text-success-emphasis`, `bg-success-subtle`, `border-success-subtle`],
        'info': [`text-info-emphasis`, `bg-info-subtle`, `border-info-subtle`],
        'warning': [`text-warning-emphasis`, `bg-warning-subtle`, `border-warning-subtle`],
        'error': [`text-danger-emphasis`, `bg-danger-subtle`, `border-danger-subtle`],
    }
    const textDict = {
        'success': `运行成功`,
        'info': `跳过运行`,
        'warning': `运行中止`,
        'error': `运行出错`,
    }
    for (var key in classDict) {
        element.classList.remove(...classDict[key]);
    }
    switch (status) {
        case "success":
            element.classList.add(...classDict['success']);
            element.textContent = textDict['success'];
            return
            break;
        case "skip":
            element.classList.add(...classDict['info']);
            element.textContent = textDict['info'];
            return
            break;
        case "abort":
            element.classList.add(...classDict['warning']);
            element.textContent = textDict['warning'];
            return
            break;
        case "error":
            element.classList.add(...classDict['error']);
            element.textContent = textDict['error'];
            return
            break;
        default:
            element.classList.add(...classDict['info']);
            element.textContent = textDict['info'];
            return
            break;
    }
}
function update_new() {
    let config = user_config
    $.ajax({
        url: `/daily/api/account/${account}/${jinjaUrl}` + window.location.search,
        type: "put",
        data: JSON.stringify(config),
        contentType: "application/json;charset=utf-8",
        processData: false,
        success: function (ret) {
			show_toast('success', '修改保存成功。')
        },
        error: function (ret) {
            show_toast('error', '修改保存失败。', `将于三秒后刷新页面。\n如需帮助，请联系管理员。\n${ret.responseText}`);
            setTimeout(function() {
                location.reload(true);
            }, 3000);
        },
    });
}
function load_results(module, ret) {
    for (let i = 0; i < module.length; ++i) {
        load_result(ret, module[i]);
    }
}
function selectOnChange(e) {
    const key = e.id;
    let value = e.value;
    if (isDigit(value))
        value = parseInt(value);
    user_config[key] = value;
    update_new();
    $(`[name=${key}]`).val(value);
}
function isDigit(str) {
    for (var i = 0; i < str.length; i++) {
        if (isNaN(parseInt(str[i]))) {
            return false;
        }
    }
    return true;
};
function selectMultiOnChange(e) {
    const key = e.id;
    let value = Array.from(e.selectedOptions).map(option => option.value);
	if (value.every((val) => $.isNumeric((val)))){
		value = value.map(option => parseInt(option))
	}
    user_config[key] = value;
    update_new();
};
function checkboxOnclick(checkbox) {
    const key = checkbox.id;
    const value = checkbox.checked;
    user_config[key] = value;
    update_new();
}
function do_single(e) {
    const flag = e.getAttribute('flag');
    $(`[flag=${flag}]`).attr('disabled', true);
    toggle_spinner('show', e);
    show_toast('info', `已开始执行“${e.name}”。`)
    let config = {
        config: user_config,
        order: [`${e.getAttribute('key')}`]
    }
    $.ajax({
        url: '/daily/api/account/${account}/do_single' + window.location.search,
        type: 'post',
        contentType: "application/json;charset=utf-8",
        data: JSON.stringify(config),
        success: function (ret) {
            load_results(ret.order, ret.result);
            $(`[flag=${flag}]`).attr('disabled', false);
            toggle_spinner('hidden', e);
            show_toast('success', `“${e.name}”执行成功。`)
        },
        error: function (ret) {
            show_toast('error', `“${e.name}”执行失败。`, `${ret.responseText}`)
            $(`[flag=${flag}]`).attr('disabled', false);
            toggle_spinner('hidden', e);
        }
    })
	query_validate(e);
}
function do_all_task(e) {
    const flag = e.getAttribute('flag');
    $(`[flag=${flag}]`).attr('disabled', true);
    toggle_spinner('show', e)
    show_toast('info', `已开始执行任务。`)
    $.ajax({
        url: '/daily/api/account/${account}/do_task' + window.location.search,
        type: 'get',
        processData: false,
        success: function (ret) {
            show_toast('success', `任务执行完毕。`)
            toggle_spinner('hidden', e)
            $(`[flag=${flag}]`).attr('disabled', false);
            load_results(ret.order, ret.result);
        },
        error: function (ret) {
            show_toast("error", "任务执行失败。", `${ret.responseText}`);
            toggle_spinner('hidden', e)
            $(`[flag=${flag}]`).attr('disabled', false);
        }
    })
	query_validate(e);
};

var cnt = 0

function query_validate(e){
	if (cnt > 120){
		cnt = 0;
		return;
	}
    $.ajax({
        url: '/daily/api/account/${account}/query_validate' + window.location.search,
        type: 'get',
        processData: false,
        success: function (ret) {
			if (ret.status === 200) {
				cnt = 0
			  // 200 OK，不需要验证，结束循环
			}
        },
        error: function (ret) {
			cnt += 1;
			if (ret.status === 404) {
			  // 404 Not Found，未找到验证请求，等待一秒后继续发送请求
			  setTimeout(query_validate, 1000);
			} else if (ret.status === 400) {
			  // 400 Bad Request 
			  show_toast("error", "验证查询失败。", `${ret.responseText}`);
			  cnt = 0
			} else if (ret.status === 401) {
			  // 401 Unauthorized，抛出错误，继续轮训，可能二次验证
			  show_validate(ret.responseText)
			  setTimeout(query_validate, 1000);
			}
        }
    })
}
