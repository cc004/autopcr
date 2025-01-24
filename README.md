# autopcr

[![License](https://img.shields.io/github/license/cc004/autopcr)](LICENSE)

自动清日常
bug反馈/意见/交流群: 885228564

请先运行一次`python3 _download_web.py`下载前端资源。

如果网络不好，可自行[下载压缩包](https://github.com/Lanly109/AutoPCR_Web/releases/latest)，然后`python3 _download_web.py /path/to/zip`安装。

## HTTP 服务器模式

```bash
python3 _httpserver_test.py
```

访问`/daily/login`

## Hoshino插件模式

使用前请更新Hoshino到最新版，并**更新Hoshino的配置文件`__bot__.py`**

## 渠道服支持

渠道服需要自抓`uid`和`access_key`，作为用户名和密码。

## 配置

| 环境变量                          | 描述            | 默认值（留空则表示必填）     |
|-------------------------------|---------------|------------------|
| AUTOPCR_SERVER_PORT           | 自定义服务器启动端口    | 13200            |
| AUTOPCR_SERVER_DEBUG_LOG      | 是否输出 Debug 日志 | False            |
| AUTOPCR_SERVER_ALLOW_REGISTER | 是否允许注册        | True             |
| AUTOPCR_SERVER_SUPERUSER      | 设置无条件拥有管理员的用户 | （可选，设置为登录使用的 QQ） |

## Credits
- aiorequests 来自 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
- 图片绘制改自 [convert2img](https://github.com/SonderXiaoming/convert2img)
- 前端html来自 [AutoPCR_Web](https://github.com/Lanly109/AutoPCR_Web)
- ~~前端html来自 [autopcr_web](https://github.com/cca2878/autopcr_web)~~
- ~~前端html来自 [AutoPCR_Archived](https://github.com/watermellye/AutoPCR_Archived)~~
- ~~模型生成来自 [PcrotoGen](https://github.com/cc004/PcrotoGen)~~
