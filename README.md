# autopcr

[![License](https://img.shields.io/github/license/cc004/autopcr)](LICENSE)

自动清日常
bug反馈/意见/交流群: 885228564

请先运行一次`_download_web.py`下载前端资源。

## HTTP 服务器模式

```bash
py -3.8 httpserver_test.py
```

访问`/daily/login`

## Hoshino插件模式

使用前请更新Hoshino到最新版，并**更新Hoshino的配置文件`__bot__.py`**

## 渠道服支持

渠道服需要自抓`uid`和`access_key`，作为用户名和密码，渠道服和b服同一模块目前仅能支持一个，更改登录使用b服或者渠道服需要到`autopcr/constants.py`中修改`SDK_CLIENT`为`BSDK`或者`QSDK`（默认为`BSDK`，即b服）

## Credits
- aiorequests 来自 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
- 图片绘制改自 [convert2img](https://github.com/SonderXiaoming/convert2img)
- 前端html来自 [AutoPCR_Web](https://github.com/Lanly109/AutoPCR_Web)
- ~~前端html来自 [autopcr_web](https://github.com/cca2878/autopcr_web)~~
- ~~前端html来自 [AutoPCR_Archived](https://github.com/watermellye/AutoPCR_Archived)~~
- ~~模型生成来自 [PcrotoGen](https://github.com/cc004/PcrotoGen)~~
