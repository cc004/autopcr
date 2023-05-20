# autopcr
自动清日常

## HTTP 服务器模式

```bash
py -3.8 httpserver_test.py
```

url前缀为`/daily`

## Hoshino插件模式

目前感觉不是很必要所以先摆，但是欢迎pr

适配`hoshino`，同时`hoshino`下的网页版无法调用清日常，只能在群聊调用。

图片生成依赖于`imgkit`库，`linux`需要配置一下`x server`啥的

## Credits
- aiorequests 来自 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
- 前端html(~~虽然还没开始写但是先加上了~~) 来自 [@watermellye](https://github.com/watermellye)
