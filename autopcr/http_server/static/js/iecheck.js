(function(window){
    var userAgent = navigator.userAgent; 
    var isIE = userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1;
    var isIE11 = userAgent.indexOf('Trident') > -1 && userAgent.indexOf("rv:11.0") > -1;
    if(isIE || isIE11){
        var str = "你的浏览器版本太低了,已经和时代脱轨了 :(";
        var str2 = "推荐使用:<a href='https://www.google.cn/chrome/index.html' target='_blank' style='color:blue;'>Chrome</a>,"
            + "<a href='https://www.firefox.com.cn' target='_blank' style='color:blue;'>Firefox</a>,"
            + "<a href='https://www.microsoft.com/zh-cn/edge' target='_blank' style='color:blue;'>Edge</a>,"
            + "其他双核极速模式";
        document.writeln("<pre style='text-align:center;color:#000000;background-color:#ffffff; height:100%;border:0;position:fixed;top:0;left:0;width:100%;z-index:1234'>" +
            "<h2 style='padding-top:200px;margin:0'><strong>" + str + "<br/></strong></h2><h2>" +
            str2 + "</h2><h2 style='margin:0'><strong>如果你的使用的是双核浏览器,请切换到极速模式访问<br/></strong></h2></pre>");
        document.execCommand("Stop"); 
    }
})(window)
