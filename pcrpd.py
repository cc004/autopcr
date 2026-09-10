from hoshino import Service, privfrom hoshino.typing import CQEventimport jsonimport osimport re  # 确保导入re模块import tracebacksv = Service('一键配队', enable_on_default=False, help_='一键生成配队\n用法：一键配队 队伍名 角色1 角色2 角色3 角色4 角色5')
CHARA_NAME = {
    1000: ["未知角色", "未知キャラ", "Unknown"],
    1001: ["日和", "ヒヨリ", "Hiyori", "日和莉", "猫拳", "东山", "🐱👊"],
    1002: ["优衣", "ユイ", "Yui", "种田", "普田", "由衣", "结衣", "ue", "↗↘↗↘"],
    1003: ["怜", "レイ", "Rei", "剑圣", "普怜", "伶"],
    1004: ["禊", "ミソギ", "Misogi", "未奏希", "炸弹", "炸弹人", "熊孩子", "💣"],
    1005: ["茉莉", "マツリ", "Matsuri", "跳跳虎", "老虎", "虎", "跳刀虎", "🐅"],
    1006: ["茜里", "アカリ", "Akari", "妹法", "阿卡丽", "妹妹法"],
    1007: ["宫子", "ミヤコ", "Miyako", "布丁", "布", "幽灵", "🍮"],
    1008: ["雪", "ユキ", "Yuki", "小雪", "镜子", "镜法", "伪娘", "男孩子", "男孩纸", "雪哥"],
    1009: ["杏奈", "アンナ", "Anna", "中二", "煤气罐"],
    1010: ["真步", "マホ", "Maho", "狐狸", "真扎", "咕噜灵波", "真布", "🦊"],
    1011: ["璃乃", "リノ", "Rino", "妹弓"],
    1012: ["初音", "ハツネ", "Hatsune", "hego", "星法", "星星法", "⭐法", "睡法", "拍大星"],
    1013: ["七七香", "ナナカ", "Nanaka", "娜娜卡", "77k", "77香", "十十力", "77"],
    1014: ["霞", "カスミ", "Kasumi", "香澄", "侦探", "杜宾犬", "驴", "驴子", "驴妹", "🔍"],
    1015: ["美里", "ミサト", "Misato", "圣母"],
    1016: ["铃奈", "スズナ", "Suzuna", "暴击弓", "暴弓", "爆击弓", "爆弓", "辣妹弓", "政委"],
    1017: ["香织", "カオリ", "Kaori", "琉球犬", "狗子", "狗", "狗拳", "🐶", "🐕", "🐶👊🏻", "🐶👊"],
    1018: ["伊绪", "イオ", "Io", "老师", "魅魔", "依绪"],

    1020: ["美美", "ミミ", "Mimi", "兔子", "兔兔", "兔剑", "萝卜霸断剑", "人参霸断剑", "天兔霸断剑", "🐇", "🐰"],
    1021: ["胡桃", "クルミ", "Kurumi", "铃铛", "🔔"],
    1022: ["依里", "ヨリ", "Yori", "姐法", "姐姐法"],
    1023: ["绫音", "アヤネ", "Ayane", "熊锤", "🐻🔨", "🐻"],

    1025: ["铃莓", "スズメ", "Suzume", "女仆", "妹抖", "悠木碧", "umb", "雀"],
    1026: ["铃", "リン", "Rin", "松鼠", "🐿", "🐿️"],
    1027: ["惠理子", "エリコ", "Eriko", "病娇"],
    1028: ["咲恋", "サレン", "Saren", "充电宝", "青梅竹马", "幼驯染", "院长", "园长", "🔋", "普电"],
    1029: ["望", "ノゾミ", "Nozomi", "偶像", "小望", "🎤"],
    1030: ["妮诺", "ニノン", "Ninon", "妮侬", "扇子"],
    1031: ["忍", "シノブ", "Shinobu", "普忍", "鬼父", "💀"],
    1032: ["秋乃", "アキノ", "Akino", "哈哈剑"],
    1033: ["真阳", "マヒル", "Mahiru", "奶牛", "🐄", "🐮", "真☀"],
    1034: ["优花梨", "ユカリ", "Yukari", "由加莉", "黄骑", "酒鬼", "奶骑", "圣骑", "🍺", "🍺👻", "油咖喱"],

    1036: ["镜华", "キョウカ", "Kyouka", "Kyoka", "小仓唯", "xcw", "小苍唯", "8岁", "八岁", "喷水萝", "八岁喷水萝", "8岁喷水萝"],
    1037: ["智", "トモ", "Tomo", "卜毛", "脱毛", "智爷"],
    1038: ["栞", "シオリ", "Shiori", "tp弓", "小栞", "白虎弓", "白虎妹", "栞栞", "白虎"],

    1040: ["碧", "アオイ", "Aoi", "香菜", "香菜弓", "绿毛弓", "毒弓", "绿帽弓", "绿帽"],

    1042: ["千歌", "チカ", "Chika", "绿毛奶", "精灵奶"],
    1043: ["真琴", "マコト", "Makoto", "狼", "🐺", "月月", "朋", "狼姐"],
    1044: ["伊莉亚", "イリヤ", "Iriya", "Illya", "伊利亚", "伊莉雅", "伊利雅", "yly", "吸血鬼", "那个女人"],
    1045: ["空花", "クウカ", "Kuuka", "抖m", "抖"],
    1046: ["珠希", "タマキ", "Tamaki", "猫剑", "🐱剑", "🐱🗡️"],
    1047: ["纯", "ジュン", "Jun", "黑骑", "saber"],
    1048: ["美冬", "ミフユ", "Mifuyu", "子龙", "赵子龙"],
    1049: ["静流", "シズル", "Shizuru", "姐姐"],
    1050: ["美咲", "ミサキ", "Misaki", "大眼", "眼球法", "👀", "👁️", "👁"],
    1051: ["深月", "ミツキ", "Mitsuki", "眼罩", "抖s", "医生"],
    1052: ["莉玛", "リマ", "Rima", "Lima", "草泥马", "羊驼", "🦙", "🐐"],
    1053: ["莫妮卡", "モニカ", "Monika", "毛二力", "莫尼卡"],
    1054: ["纺希", "ツムギ", "Tsumugi", "裁缝", "蜘蛛侠", "🕷️", "🕸️"],
    1055: ["步未", "アユミ", "Ayumi", "步美", "路人", "路人妹"],
    1056: ["流夏", "ルカ", "Ruka", "大姐", "大姐头", "儿力", "luka", "刘夏", "露卡", "卢卡"],
    1057: ["吉塔", "ジータ", "Jiita", "Djeeta", "姬塔", "团长", "吉他", "🎸", "骑空士", "qks"],
    1058: ["贪吃佩可", "ペコリーヌ", "Pecorine", "Pekoriinu", "佩可莉姆", "吃货", "佩可", "公主", "饭团", "🍙"],
    1059: ["可可萝", "コッコロ", "Kokkoro", "可可罗", "妈", "普白", "普妈", "kkr"],
    1060: ["凯留", "キャル", "Karyl", "Kyaru", "凯露", "百地希留耶", "希留耶", "Kiruya", "黑猫", "臭鼬", "普黑", "接头霸王", "街头霸王", "猫猫", "猫猫头"],
    1061: ["矛依未", "ムイミ", "Muimi", "诺维姆", "Noemu", "夏娜", "511", "611", "无意义", "天楼霸断剑", "姆咪", "母咪"],

    1063: ["亚里莎", "アリサ", "Arisa", "鸭梨瞎", "瞎子", "亚里沙", "鸭梨傻", "亚丽莎", "亚莉莎", "瞎子弓", "🍐🦐", "yls"],
    1064: ["雪菲", "シェフィ", "Shephy", "Shefi", "Sheffy", "紫布菜", "冰龙"],
    1065: ["嘉夜", "カヤ", "Kaya", "憨憨龙", "龙拳", "🐲👊🏻", "🐉👊🏻", "接龙笨比", "鬼道嘉夜", "卡雅", "卡亚", "卡娅"],
    1066: ["祈梨", "イノリ", "Inori", "梨老八", "李老八", "龙锤", "🐲🔨"],
    1067: ["帆稀", "ホマレ", "Homare", "穗希", "龙妈", "龙王", "大仓唯"],
    1068: ["拉比林斯达", "ラビリスタ", "Labyrista", "Rabirisuta", "迷宫女王", "模索路晶", "模索路", "晶", "迷宫女", "王晶", "晶姐", "日日日"],
    1069: ["真那", "マナ", "Mana", "Kaiser Insight", "霸瞳皇帝", "千里真那", "千里", "霸瞳", "霸铜"],
    1070: ["似似花", "ネネカ", "Neneka", "变貌大妃", "现士实似似花", "現士実似々花", "現士実", "现士实", "nnk", "448", "捏捏卡", "变貌", "大妃", "奶奶卡"],
    1071: ["克莉丝提娜", "クリスティーナ", "Kurisutiina", "Christina", "誓约女君", "克莉丝提娜·摩根", "Christina", "Cristina", "克总", "女帝", "克", "摩根", "克姐"],
    1072: ["可萝爹", "長老", "Chourou", "岳父", "爷爷"],
    1073: ["拉基拉基", "ラジニカーント", "Rajinigaanto", "跳跃王", "Rajiraji", "Lajilaji", "垃圾垃圾", "教授"],

    1075: ["贪吃佩可(夏日)", "ペコリーヌ(サマー)", "Pecorine(Summer)", "Pekoriinu(Summer)", "SPecorine", "佩可莉姆(夏日)", "水吃", "水饭", "水吃货", "水佩可", "水公主", "水饭团", "水🍙", "泳吃", "泳饭", "泳吃货", "泳佩可", "泳公主", "泳饭团", "泳🍙", "泳装吃货", "泳装公主", "泳装饭团", "泳装🍙", "佩可(夏日)", "🥡", "👙🍙", "泼妇"],
    1076: ["可可萝(夏日)", "コッコロ(サマー)", "Kokkoro(Summer)", "SKokkoro", "水白", "水妈", "水可", "水可可", "水可可萝", "水可可罗", "泳装妈", "泳装可可萝", "泳装可可罗"],
    1077: ["铃莓(夏日)", "スズメ(サマー)", "Suzume(Summer)", "SSuzume", "水女仆", "水妹抖"],
    1078: ["凯留(夏日)", "キャル(サマー)", "Karyl(Summer)", "Kyaru(Summer)", "SKyaru", "凯露(夏日)", "水黑", "水黑猫", "水臭鼬", "泳装黑猫", "泳装臭鼬", "潶", "溴", "💧黑", "流泪猫猫头"],
    1079: ["珠希(夏日)", "タマキ(サマー)", "Tamaki(Summer)", "STamaki", "水猫剑", "水猫", "渵", "💧🐱", "💧🐱🗡️", "水🐱🗡️"],
    1080: ["美冬(夏日)", "ミフユ(サマー)", "Mifuyu(Summer)", "SMifuyu", "水子龙", "水美冬"],
    1081: ["忍(万圣节)", "シノブ(ハロウィン)", "Shinobu(Halloween)", "HShinobu", "万圣忍", "瓜忍", "鬼忍", "🎃忍", "🎃💀"],
    1082: ["宫子(万圣节)", "ミヤコ(ハロウィン)", "Miyako(Halloween)", "HMiyako", "万圣宫子", "万圣布丁", "狼丁", "狼布丁", "万圣🍮", "🐺🍮", "🎃🍮", "👻🍮"],
    1083: ["美咲(万圣节)", "ミサキ(ハロウィン)", "Misaki(Halloween)", "HMisaki", "万圣美咲", "万圣大眼", "瓜眼", "🎃眼", "🎃👀", "🎃👁️", "🎃👁"],
    1084: ["千歌(圣诞节)", "チカ(クリスマス)", "Chika(Xmas)", "Chika(Holiday)", "XChika", "圣诞千歌", "圣千", "蛋鸽", "🎄💰🎶", "🎄千🎶", "🎄1000🎶"],
    1085: ["胡桃(圣诞节)", "クルミ(クリスマス)", "Kurumi(Xmas)", "Kurumi(Holiday)", "XKurumi", "圣诞胡桃", "圣诞铃铛", "圣铃"],
    1086: ["绫音(圣诞节)", "アヤネ(クリスマス)", "Ayane(Xmas)", "Ayane(Holiday)", "XAyane", "圣诞熊锤", "蛋锤", "圣锤", "🎄🐻🔨", "🎄🐻"],
    1087: ["日和(新年)", "ヒヨリ(ニューイヤー)", "Hiyori(NewYear)", "NYHiyori", "新年日和", "春猫", "👘🐱"],
    1088: ["优衣(新年)", "ユイ(ニューイヤー)", "Yui(NewYear)", "NYYui", "新年优衣", "春田", "新年由衣"],
    1089: ["怜(新年)", "レイ(ニューイヤー)", "Rei(NewYear)", "NYRei", "春剑", "春怜", "春伶", "新春剑圣", "新年怜", "新年剑圣"],
    1090: ["惠理子(情人节)", "エリコ(バレンタイン)", "Eriko(Valentine)", "VEriko", "情人节病娇", "恋病", "情病", "恋病娇", "情病娇", "青椒"],
    1091: ["静流(情人节)", "シズル(バレンタイン)", "Shizuru(Valentine)", "VShizuru", "情人节静流", "情姐", "情人节姐姐", "恋姐"],
    1092: ["安", "アン", "An", "Anne", "胖安", "55kg", "小安"],
    1093: ["露", "ルゥ", "Ruu", "Lou", "逃课女王", "补考女帝"],
    1094: ["古蕾娅", "グレア", "Gurea", "Grea", "龙姬", "古雷娅", "古蕾亚", "古雷亚", "古蕾雅", "🐲🐔", "🐉🐔"],
    1095: ["空花(大江户)", "クウカ(オーエド)", "Kuuka(Ooedo)", "OKuuka", "江户空花", "江户抖m", "江m", "花m", "江花", "大江m", "花抖"],
    1096: ["妮诺(大江户)", "ニノン(オーエド)", "Ninon(Ooedo)", "ONinon", "江户扇子", "忍扇"],
    1097: ["雷姆", "レム", "Remu", "Rem", "蕾姆", "雷姆"],
    1098: ["拉姆", "ラム", "Ramu", "Ram"],
    1099: ["爱蜜莉雅", "エミリア", "Emilia", "艾米莉亚", "emt"],
    1100: ["铃奈(夏日)", "スズナ(サマー)", "Suzuna(Summer)", "SSuzuna", "瀑击弓", "水爆", "水爆弓", "水暴", "瀑", "水暴弓", "水暴击弓", "水政委", "瀑弓", "泳装暴弓", "泳装爆弓", "泳装政委"],
    1101: ["伊绪(夏日)", "イオ(サマー)", "Io(Summer)", "SIo", "水魅魔", "水老师", "泳装魅魔", "泳装老师", "水io"],
    1102: ["美咲(夏日)", "ミサキ(サマー)", "Misaki(Summer)", "水美咲", "水大眼", "泳装大眼"],
    1103: ["咲恋(夏日)", "サレン(サマー)", "Saren(Summer)", "SSaren", "水电", "泳装充电宝", "泳装咲恋", "水着咲恋", "水电站", "水电宝", "水充", "👙🔋"],
    1104: ["真琴(夏日)", "マコト(サマー)", "Makoto(Summer)", "SMakoto", "水狼", "浪", "水🐺", "泳狼", "泳月", "泳月月", "泳朋", "水月", "水月月", "水朋", "👙🐺"],
    1105: ["香织(夏日)", "カオリ(サマー)", "Kaori(Summer)", "SKaori", "水狗", "泃", "水🐶", "水🐕", "泳狗", "水狗拳"],
    1106: ["真步(夏日)", "マホ(サマー)", "Maho(Summer)", "SMaho", "水狐狸", "水狐", "水壶", "水真步", "水maho", "氵🦊", "水🦊", "💧🦊"],
    1107: ["碧(插班生)", "アオイ(編入生)", "Aoi(Hennyuusei)", "TSAoi", "生菜", "插班碧", "学院碧", "转校弓", "转学弓"],
    1108: ["克萝依", "クロエ", "Kuroe", "Chloe", "克罗依", "华哥", "黑江", "黑江花子", "花子"],
    1109: ["琪爱儿", "チエル", "Chieru", "千爱瑠", "切露", "茄露", "茄噜", "切噜", "佐仓"],
    1110: ["优妮", "ユニ", "Yuni", "真行寺由仁", "由仁", "优尼", "u2", "优妮辈先", "辈先", "书记", "uni", "先辈", "仙贝", "油腻", "优妮先辈", "学姐", "18岁黑丝学姐", "咖啡人"],
    1111: ["镜华(万圣节)", "キョウカ(ハロウィン)", "Kyouka(Halloween)", "Kyoka(Halloween)", "HKyouka", "万圣镜华", "万圣小仓唯", "万圣xcw", "猫仓唯", "黑猫仓唯", "mcw", "猫唯", "猫仓", "喵唯"],
    1112: ["禊(万圣节)", "ミソギ(ハロウィン)", "Misogi(Halloween)", "HMisogi", "万圣禊", "万圣炸弹人", "瓜炸弹人", "万圣炸弹", "万圣炸", "瓜炸", "南瓜炸", "万圣节禊", "万圣熊孩", "🎃💣"],
    1113: ["美美(万圣节)", "ミミ(ハロウィン)", "Mimi(Halloween)", "HMimi", "万圣兔", "万圣兔子", "万圣兔兔", "绷带兔", "绷带兔子", "万圣美美", "绷带美美", "瓜兔", "万圣🐰", "绷带🐰", "🎃🐰", "万圣🐇", "绷带🐇", "🎃🐇"],
    1114: ["露娜", "ルナ", "Runa", "Luna", "露仓唯", "露cw"],
    1115: ["克莉丝提娜(圣诞节)", "クリスティーナ(クリスマス)", "Kurisutiina(Xmas)", "Christina(Xmas)", "Cristina(Xmas)", "Christina(Holiday)", "XChristina", "圣诞克", "圣诞克总", "圣诞女帝", "蛋克", "蛋壳", "圣克", "必胜客"],
    1116: ["望(圣诞节)", "ノゾミ(クリスマス)", "Nozomi(Xmas)", "Nozomi(Holiday)", "XNozomi", "圣诞望", "圣诞偶像", "蛋偶像", "蛋望"],
    1117: ["伊莉亚(圣诞节)", "イリヤ(クリスマス)", "Iriya(Xmas)", "Illya(Holiday)", "XIllya", "圣诞伊莉亚", "圣诞伊利亚", "圣诞伊莉雅", "圣诞伊利雅", "圣诞yly", "圣诞吸血鬼", "圣伊", "圣yly", "伊利丹"],
    1118: ["贪吃佩可(新年)", "ペコリーヌ(ニューイヤー)", "Pecorine(NewYear)", "NYPecorine", "佩可莉姆(新年)", "春吃", "新吃", "新年吃货", "年货"],
    1119: ["可可萝(新年)", "コッコロ(ニューイヤー)", "Kokkoro(NewYear)", "NYKokkoro", "春可可", "春白", "新年妈", "春妈"],
    1120: ["凯留(新年)", "キャル(ニューイヤー)", "Karyl(NewYear)", "Kyaru(NewYear)", "NYKyaru", "凯露(新年)", "春凯留", "春黑猫", "春黑", "春臭鼬", "新年凯留", "新年黑猫", "新年臭鼬", "唯一神", "神"],
    1121: ["铃莓(新年)", "スズメ(ニューイヤー)", "Suzume(NewYear)", "NYSuzume", "春铃莓", "春女仆", "春妹抖", "新年铃莓", "新年女仆", "新年妹抖"],
    1122: ["霞(魔法少女)", "カスミ(マジカル)", "Kasumi(MagiGirl)", "Kasumi(Magical)", "MGKasumi", "魔法少女霞", "魔法侦探", "魔法杜宾犬", "魔法驴", "魔法驴子", "魔驴", "魔法霞", "魔法少驴"],
    1123: ["栞(魔法少女)", "シオリ(マジカル)", "Shiori(MagiGirl)", "Shiori(Magical)", "MGShiori", "魔法少女栞", "魔法tp弓", "魔法小栞", "魔法白虎弓", "魔法白虎妹", "魔法白虎", "魔栞", "魔弓", "魔法弓", "法弓"],
    1124: ["卯月(NGs)", "ウヅキ(デレマス)", "Udsuki(DEREM@S)", "Uzuki(IM@S CG)", "Uzuki(Deremasu)", "Uzuki", "卯月(偶像大师)", "卯月", "卵用", "Udsuki(DEREMAS)", "岛村卯月", "Udsuki"],
    1125: ["凛(NGs)", "リン(デレマス)", "Rin(DEREM@S)", "Rin(IM@S CG)", "Rin(Deremasu)", "Shiburin", "凛(偶像大师)", "凛", "Rin(DEREMAS)", "涩谷凛", "西部凛"],
    1126: ["未央(NGs)", "ミオ(デレマス)", "Mio(DEREM@S)", "Mio(IM@S CG)", "Mio(Deremasu)", "Mio", "未央(偶像大师)", "未央", "Mio(DEREMAS)", "本田未央", "Mio"],
    1127: ["铃(游侠)", "リン(レンジャー)", "Rin(Ranger)", "RRin", "骑兵松鼠", "游侠松鼠", "游骑兵松鼠", "护林员松鼠", "护林松鼠", "游侠🐿️", "武松", "钻头松鼠"],
    1128: ["真阳(游侠)", "マヒル(レンジャー)", "Mahiru(Ranger)", "RMahiru", "骑兵奶牛", "游侠奶牛", "游骑兵奶牛", "护林员奶牛", "护林奶牛", "游侠🐄", "游侠🐮", "牛叉"],
    1129: ["璃乃(奇幻)", "リノ(ワンダー)", "Rino(Wonder)", "Rino(Wonderland)", "WRino", "璃乃(奇境)", "璃乃(仙境)", "爽弓", "爱丽丝弓", "爱弓", "兔弓", "奇境妹弓", "奇幻妹弓", "奇幻璃乃", "仙境妹弓", "白丝妹弓", "爱丽丝妹弓"],
    1130: ["步未(奇幻)", "アユミ(ワンダー)", "Ayumi(Wonder)", "Ayumi(Wonderland)", "WAyumi", "步未(奇境)", "步未(仙境)", "路人兔", "兔人妹", "爱丽丝路人", "奇境路人", "奇幻路人", "奇幻步未", "仙境路人", "爱丽丝路人妹", "梦路", "步美(仙境)"],
    1131: ["流夏(夏日)", "ルカ(サマー)", "Ruka(Summer)", "SRuka", "泳装流夏", "水流夏", "泳装刘夏", "水刘夏", "泳装大姐", "泳装大姐头", "水大姐", "水大姐头", "水儿力", "泳装儿力", "水流"],
    1132: ["杏奈(夏日)", "アンナ(サマー)", "Anna(Summer)", "SAnna", "泳装中二", "泳装煤气罐", "水中二", "水煤气罐", "冲", "冲二"],
    1133: ["七七香(夏日)", "ナナカ(サマー)", "Nanaka(Summer)", "SNanaka", "泳装娜娜卡", "泳装77k", "泳装77香", "水娜娜卡", "水77k", "水77香", "水七七香", "泳装七七香", "水七", "水7"],
    1134: ["初音(夏日)", "ハツネ(サマー)", "Hatsune(Summer)", "SHatsune", "水星", "海星", "水hego", "水星法", "泳装星法", "水⭐法", "水睡法", "湦", "泳装初音", "水初音", "夏日初音"],
    1135: ["美里(夏日)", "ミサト(サマー)", "Misato(Summer)", "SMisato", "水母", "泳装圣母", "水圣母"],
    1136: ["纯(夏日)", "ジュン(サマー)", "Jun(Summer)", "SJun", "泳装黑骑", "水黑骑", "泳装纯", "水纯", "小次郎", "水骑"],
    1137: ["茜里(天使)", "アカリ(エンジェル)", "Akari(Angel)", "AAkari", "天使妹法", "天使茜里", "丘比特妹法", "天妹"],
    1138: ["依里(天使)", "ヨリ(エンジェル)", "Yori(Angel)", "AYori", "天使姐法", "天使依里", "丘比特姐法", "天姐"],
    1139: ["纺希(万圣节)", "ツムギ(ハロウィン)", "Tsumugi(Halloween)", "HTsumugi", "万圣裁缝", "万圣蜘蛛侠", "🎃🕷️", "🎃🕸️", "万裁", "瓜裁", "鬼裁", "鬼才"],
    1140: ["怜(万圣节)", "レイ(ハロウィン)", "Rei(Halloween)", "HRei", "万圣剑圣", "万剑", "瓜剑", "瓜怜", "万圣怜", "鬼剑", "鬼怜"],
    1141: ["茉莉(万圣节)", "マツリ(ハロウィン)", "Matsuri(Halloween)", "HMatsuri", "万圣跳跳虎", "万圣老虎", "瓜虎", "万圣虎", "🎃🐅", "鬼虎"],
    1142: ["莫妮卡(魔法少女)", "モニカ(マジカル)", "Monika(MagiGirl)", "MGMonika", "魔法少女莫妮卡", "魔二力", "魔卡少女"],
    1143: ["智(魔法少女)", "トモ(マジカル)", "Tomo(MagiGirl)", "MGTomo", "魔法少女智", "琪露诺", "9智", "⑨", "魔智"],
    1144: ["秋乃(圣诞节)", "アキノ(クリスマス)", "Akino(Xmas)", "XAkino", "圣剑", "生煎", "圣诞哈哈剑", "哈哈剑(圣诞节)", "圣哈", "蛋哈", "蛋剑"],
    1145: ["咲恋(圣诞节)", "サレン(クリスマス)", "Saren(Xmas)", "XSaren", "圣诞充电宝", "圣电", "圣诞咲恋"],
    1146: ["优花梨(圣诞节)", "ユカリ(クリスマス)", "Yukari(Xmas)", "XYukari", "蛋黄", "由加莉(圣诞节)", "圣诞黄骑", "圣诞圣骑", "蛋骑", "黄骑(圣诞节)", "圣黄"],
    1147: ["矛依未(新年)", "ムイミ(ニューイヤー)", "Muimi(NewYear)", "NYMuimi", "新年511", "春511", "春11", "春矛", "512"],


    1150: ["似似花(新年)", "ネネカ(ニューイヤー)", "Neneka(NewYear)", "NYNeneka", "新年似似花", "春似似花", "春nnk", "春花", "新年nnk", "春妃", "春448"],




    1155: ["可可萝(祭服)", "コッコロ(儀装束)", "Kokkoro(Costume)", "Kokkoro(Ceremonial)", "CKokkoro", "可可萝(礼服)", "可可萝(仪装束)", "礼妈", "仪妈", "仪装妈", "姨妈", "礼白"],
    1156: ["优衣(祭服)", "ユイ(儀装束)", "Yui(Costume)", "Yui(Ceremonial)", "CYui", "优衣(礼服)", "优衣(仪装束)", "礼ue", "礼装ue", "礼装优衣", "仪装ue", "礼衣", "礼田"],
    1157: ["霞(夏日)", "カスミ(サマー)", "Kasumi(Summer)", "SKasumi", "香澄(夏日)", "水驴", "泳装驴", "沪"],
    1158: ["莉玛(灰姑娘)", "リマ(シンデレラ)", "Rima(Cinderella)", "Lima(Cinderella)", "CLima", "人形羊驼", "人驼", "灰驼", "灰姑娘羊驼", "灰羊"],
    1159: ["真琴(灰姑娘)", "マコト(シンデレラ)", "Makoto(Cinderella)", "CMakoto", "灰姑娘狼", "灰狼"],
    1160: ["真步(灰姑娘)", "マホ(シンデレラ)", "Maho(Cinderella)", "CMaho", "灰姑娘狐狸", "灰狐狸", "灰狐", "灰壶", "茶狐", "茶壶"],

    1162: ["克萝依(圣学祭)", "クロエ(聖学祭)", "Kuroe(Seigakusai)", "Chloe(SchoolFestival)", "SFChloe", "克罗依(圣学祭)", "运动华", "运动华哥", "圣学祭华", "圣学祭克萝依", "圣华", "圣华哥"],
    1163: ["琪爱儿(圣学祭)", "チエル(聖学祭)", "Chieru(Seigakusai)", "Chieru(SchoolFestival)", "SFChieru", "千爱瑠(圣学祭)", "运动切噜", "圣学祭切噜", "圣学祭琪爱儿", "圣学祭千爱瑠", "圣爱瑠", "圣切噜"],
    1164: ["优妮(圣学祭)", "ユニ(聖学祭)", "Yuni(Seigakusai)", "Yuni(SchoolFestival)", "SFYuni", "圣优妮", "圣uni", "运动优妮", "运动服", "罗塞塔"],
    1165: ["祈梨(时间旅行)", "イノリ(タイムトラベル)", "Inori(TimeTravel)", "Inori(TimeTraveller)", "TTInori", "时间旅行龙锤", "穿越龙锤", "穿越梨老八", "军装龙锤", "元首龙锤","旅锤", "元首", "元老八"],
    1166: ["嘉夜(时间旅行)", "カヤ(タイムトラベル)", "Kaya(TimeTravel)", "Kaya(TimeTraveller)", "TTKaya", "时间旅行龙拳", "穿越龙拳", "水手龙", "水手龙拳", "时空龙拳", "白龙拳"],
    1167: ["碧(作业服)", "アオイ(作業服)", "Aoi(Sagyoufuku)", "Aoi(Work)", "WAoi", "碧(工作服)", "工菜", "韭菜", "工作碧", "贡菜"],
    1168: ["珠希(作业服)", "タマキ(作業服)", "Tamaki(Sagyoufuku)", "Tamaki(Work)", "WTamaki", "珠希(工作服)", "工猫贼", "工猫剑", "工贼", "工猫", "工珠希"],
    1169: ["美冬(作业服)", "ミフユ(作業服)", "Mifuyu(Sagyoufuku)", "Mifuyu(Work)", "WMifuyu", "美冬(工作服)", "电子龙", "工子龙", "工龙", "工头"],
    1170: ["惠理子(夏日)", "エリコ(サマー)", "Eriko(Summer)", "SEriko", "泳装惠理子", "泳装病娇", "水病", "水病娇", "水饺", "水娇"],
    1171: ["静流(夏日)", "シズル(サマー)", "Shizuru(Summer)", "SShizuru", "泳装静流", "泳装姐姐", "水姐", "水姐姐", "水解", "沮"],
    1172: ["望(夏日)", "ノゾミ(サマー)", "Nozomi(Summer)", "SNozomi", "泳装偶像", "泳装望", "水望", "水偶像", "夏日偶像", "夏日望", "潒"],
    1173: ["千歌(夏日)", "チカ(サマー)", "Chika(Summer)", "SChika", "泳装千歌", "水千", "汘", "泳千"],
    1174: ["纺希(夏日)", "ツムギ(サマー)", "Tsumugi(Summer)", "STsumugi", "泳装裁缝", "泳装纺希", "水裁缝", "水裁", "水彩", "水纺希", "漨"],
    1175: ["深月(大江户)", "ミツキ(オーエド)", "Mitsuki(Ooedo)", "OMitsuki", "江月", "江S", "江户深月", "大江户深月"],
    1176: ["雪(大江户)", "ユキ(オーエド)", "Yuki(Ooedo)", "OYuki", "江雪", "江哥", "江户雪", "江户小雪", "江户雪哥", "大江户雪"],
    1177: ["香织(万圣节)", "カオリ(ハロウィン)", "Kaori(Halloween)", "HKaori", "万圣狗", "瓜狗", "万圣狗拳"],
    1178: ["妮诺(万圣节)", "ニノン(ハロウィン)", "Ninon(Halloween)", "HNinon", "妮侬(万圣节)", "万圣扇", "瓜扇", "万圣扇子"],
    1179: ["铃奈(万圣节)", "スズナ(ハロウィン)", "Suzuna(Halloween)", "HSuzuna", "万圣暴弓", "瓜弓", "瓜暴弓", "万圣爆弓", "瓜爆弓"],
    1180: ["克蕾琪塔", "クレジッタ", "Kurejitta", "Creditta", "富婆", "信用卡"],
    1181: ["兰法", "ランファ", "Ranfa", "Ranpha", "兰法妈妈", "兰妈妈", "兰妈"],
    1182: ["美空", "ミソラ", "Misora", "坏女人", "魅空", "流魅空", "流美空"],
    1183: ["初音(初音&栞)", "ハツネ(ハツネ&シオリ)", "Hatsune(Hatsune&Shiori)", "星弓星", "星栞星"],
    1184: ["栞(初音&栞)", "シオリ(ハツネ&シオリ)", "Shiori(Hatsune&Shiori)", "星弓栞", "星弓弓", "星栞栞", "星栞弓"],
    1185: ["花凛", "カリン", "Karin", "佳凛", "绿色恶魔", "绿魔", "绿毛恶魔"],
    1186: ["涅比亚", "ネビア", "Nebbia", "涅比亞", "蚊子"],



    1190: ["伊绪(黑暗)", "イオ(ノワール)", "Io(Noir)", "NIo", "黑老师", "黑魅魔"],
    1191: ["空花(黑暗)", "クウカ(ノワール)", "Kuuka(Noir)", "NKuuka", "黑m", "暗m"],
    1192: ["真阳(圣诞节)", "マヒル(クリスマス)", "Mahiru(Xmas)", "Mahiru(Holiday)", "XMahiru", "圣牛", "蛋牛", "圣诞奶牛", "圣诞牛"],
    1193: ["璃乃(圣诞节)", "リノ(クリスマス)", "Rino(Xmas)", "Rino(Holiday)", "XRino", "圣诞妹弓", "圣诞璃乃", "弹弓", "蛋弓", "诞弓"],





    1199: ["宫子(圣诞节)", "ミヤコ(クリスマス)", "Miyako(Xmas)", "Miyako(Holiday)", "XMiyako", "圣诞布丁", "圣诞宫子", "诞丁", "蛋丁", "但丁"],
    1200: ["静流(黑暗)", "シズル(ノワール)", "Shizuru(Noir)", "NShizuru", "黑姐姐", "黑姐"],



    1204: ["美美(小小甜心)", "ミミ(リトルリリカル)", "Mimi(LittleLyrical)"],
    1205: ["禊(小小甜心)", "ミソギ(リトルリリカル)", "Misogi(LittleLyrical)", "未奏希(小小甜心)"],
    1206: ["镜华(小小甜心)", "キョウカ(リトルリリカル)", "Kyouka(LittleLyrical)"],
    1207: ["雪菲(新年)", "シェフィ(ニューイヤー)", "Shephy(NewYear)", "Shefi(NewYear)", "Sheffy(NewYear)", "NYSheffy", "新年雪菲", "春雪菲", "春菲", "春冰龙"],
    1208: ["流夏(新年)", "ルカ(ニューイヤー)", "Ruka(NewYear)", "NYRuka", "春流夏", "春流"],
    1209: ["伊莉亚(新年)", "イリヤ(ニューイヤー)", "Iriya(NewYear)", "Illya(NewYear)", "NYIllya", "新年伊莉亚", "新年伊利亚", "新年伊莉雅", "新年伊利雅", "新年yly", "新年吸血鬼", "春伊", "春yly", "伊莉旦"],
    1210: ["贪吃佩可(超载)", "ペコリーヌ(オーバーロード)", "Pecorine(Overload)", "Pekoriinu(Overload)", "OPecorine", "佩可莉姆(超负荷)", "超载吃", "超吃", "超载佩可", "超载佩", "超佩"],
    1211: ["凯留(超载)", "キャル(オーバーロード)", "Karyl(Overload)", "Kyaru(Overload)", "OKyaru", "凯露(超载)", "凯露(超负荷)", "超载凯留", "超凯留", "超载黑猫", "超黑", "超猫", "超威蓝猫"],
    1212: ["拉比林斯达(超载)", "ラビリスタ(オーバーロード)", "Labyrista(Overload)", "Rabirisuta(Overload)", "OLabyrista", "菈比莉斯塔(超负荷)", "超载晶", "超晶"],
    1213: ["胡桃(舞台)", "クルミ(ステージ)", "Kurumi(Stage)", "STKurumi", "舞台胡桃", "舞桃", "演员", "舞胡", "芜湖", "舞铃", "舞台铃", "戏铃"],
    1214: ["美咲(舞台)", "ミサキ(ステージ)", "Misaki(Satge)", "STMisaki", "舞台大眼", "舞台眼", "舞台美咲", "泥头车大眼", "车眼"],
    1215: ["步未(怪盗)", "アユミ(怪盗)", "Ayumi(Kaitou)", "Ayumi(PhantomThief)", "PTAyumi", "怪盗路人", "怪盗路人妹", "怪盗妹"],
    1216: ["祈梨(怪盗)", "イノリ(怪盗)", "Inori(Kaitou)", "Inori(PhantomThief)", "PTInori", "怪盗祈梨", "怪盗龙锤", "忍龙", "忍龙锤"],
    1217: ["秋乃(秋乃&咲恋)", "アキノ(アキノ&サレン)", "Akino(Akino&Saren)"],
    1218: ["咲恋(秋乃&咲恋)", "サレン(アキノ&サレン)", "Saren(Akino&Saren)"],
    1219: ["杏奈(海盗)", "アンナ(パイレーツ)", "Anna(Pirates)", "Anna(Pirate)", "PiAnna", "海盗中二", "海盗杏奈", "船长中二", "船二", "海二"],
    1220: ["忍(海盗)", "シノブ(パイレーツ)", "Shinobu(Pirates)", "Shinobu(Pirate)", "PiShinobu", "海盗忍", "海贼忍", "海忍", "水手忍", "手忍"],
    1221: ["碧(露营)", "アオイ(キャンプ)", "Aoi(Camp)", "CAoi", "露营碧", "露碧", "野菜"],
    1222: ["优花梨(露营)", "ユカリ(キャンプ)", "Yukari(Camp)", "CYukari", "由加莉(露营)", "露营优花梨", "露优花梨", "露花梨", "露营黄骑", "露黄骑", "露黄", "野黄", "野骑"],
    1223: ["斑比", "ヴァンピィ", "Vampy", "Vania", "斑比酱", "钉宫"],
    1224: ["日和(夏日)", "ヒヨリ(サマー)", "Hiyori(Summer)", "SHiyori", "日和莉(夏日)", "水猫拳", "水日和"],
    1225: ["怜(夏日)", "レイ(サマー)", "Rei(Summer)", "SRei", "水怜", "水剑圣"],
    1226: ["优衣(夏日)", "ユイ(サマー)", "Yui(Summer)", "SYui", "水优衣", "水ue", "水田", "泳衣", "游依", "水草"],
    1227: ["镜华(夏日)", "キョウカ(サマー)", "Kyouka(Summer)", "Kyoka(Summer)", "SKyouka", "泳装镜华", "水镜华", "水xcw", "水仓唯", "水cw", "scw", "水唯"],
    1228: ["禊(夏日)", "ミソギ(サマー)", "Misogi(Summer)", "SMisogi", "未奏希(夏日)", "水禊", "水炸弹人", "水炸", "水未奏希", "泳装炸弹人", "泳装未奏希"],
    1229: ["美美(夏日)", "ミミ(サマー)", "Mimi(Summer)", "SMimi", "水美美", "泳装美美", "水兔", "水兔兔", "水兔子"],
    1230: ["爱梅斯", "アメス", "Amesu", "Ameth", "ams", "爱美斯", "艾美斯", "艾梅斯"],
    1231: ["真步(探险家)",  "マホ(エクスプローラー)", "Maho(Explorer)", "EMaho", "真步(探索者)", "野狐", "探狐", "尻狐", "屁狐", "屁胡"],
    1232: ["绫音(探险家)", "アヤネ(エクスプローラー)", "Ayane(Explorer)", "EAyane", "绫音(探索者)", "野锤", "野炊"],
    1233: ["涅娅", "ネア", "Nea", "涅亚", "小黄", "史莱姆", "黄史莱姆"],
    1234: ["纯(露营)", "ジュン(キャンプ)", "Jun(Camp)"],
    1235: ["铃(万圣节)", "リン(ハロウィン)", "Rin(Halloween)", "HRin", "瓜松鼠", "鬼松鼠", "万圣松鼠", "瓜松", "鬼松"],
    1236: ["智(万圣节)", "トモ(ハロウィン)", "Tomo(Halloween)", "HTomo", "瓜智", "鬼智", "万圣智"],
    1237: ["七七香(万圣节)", "ナナカ(ハロウィン)", "Nanaka(Halloween)", "HNanaka", "鬼七", "瓜七", "万圣七七香", "鬼泣", "鬼7", "瓜7"],
    1238: ["克莉丝提娜(狂野)", "クリスティーナ(ワイルド)", "Kurisutiina(Wild)", "Christina(Wild)", "WChristina", "兔克", "兔女郎克", "野克"],
    1239: ["茉莉(狂野)", "マツリ(ワイルド)", "Matsuri(Wild)", "WMatsuri", "小虎", "野老虎", "野虎"],
    1240: ["茜里(圣诞节)", "アカリ(クリスマス)", "Akari(Xmas)", "Akari(Holiday)", "XAkari", "圣妹", "圣诞妹法"],
    1241: ["依里(圣诞节)", "ヨリ(クリスマス)", "Yori(Xmas)", "Yori(Holiday)", "XYori", "圣姐", "圣诞姐法"],
    1242: ["纯(圣诞节)", "ジュン(クリスマス)", "Jun(Xmas)", "Jun(Holiday)", "XJun", "圣骑", "白骑", "圣黑骑", "圣诞黑骑"],
    1243: ["安(安&古蕾雅)", "アン(アン&グレア)", "An(An&Gurea)"],
    1244: ["古蕾雅(安&古蕾雅)", "グレア(アン&グレア)", "Gurea(An&Gurea)"],
    1245: ["帆稀(新年)", "ホマレ(ニューイヤー)", "Homare(NewYear)", "NYHomare", "春龙妈", "新年龙妈"],
    1246: ["美里(新年)", "ミサト(ニューイヤー)", "Misato(NewYear)", "NYMisato", "春母", "新母", "新年圣母", "春圣母"],
    1247: ["深月(新年)", "ミツキ(ニューイヤー)", "Mitsuki(NewYear)", "NYMitsuki", "春月", "新月", "新年深月"],
    1248: ["望(解放者)", "ノゾミ(リベレイター)", "Nozomi(Liberator)", "LNozomi", "解望", "充电望", "白望", "女神望", "解放望"],
    1249: ["嘉夜(解放者)", "カヤ(リベレイター)", "Kaya(Liberator)", "LKaya", "解龙拳", "解放龙拳"],
    1250: ["矛依未(解放者)", "ムイミ(リベレイター)", "Muimi(Liberator)", "LMuimi", "513", "解11", "解放511"],
    1251: ["珠希(咖啡厅)", "タマキ(カフェ)", "Tamaki(Cafe)", "CTamaki", "猫咖", "咖啡猫", "咖猫剑"],
    1252: ["莫妮卡(咖啡厅)", "モニカ(カフェ)", "Monika(Cafe)", "CMonika", "莫妮咖", "咖二力", "猫二力"],
    1253: ["可可萝(游侠)", "コッコロ(レンジャー)", "Kokkoro(Ranger)", "RKokkoro", "游妈", "狗妈", "游侠可可萝", "游侠妈", "游白"],
    1254: ["栞(游侠)", "シオリ(レンジャー)", "Shiori(Ranger)", "RShiori", "游栞", "游侠栞", "游侠tp弓", "狼栞"],
    1255: ["姬塔(术士)", "ジータ(ウォーロック)", "Djeeta(Warlock)","WDjeeta","魔姬", "魔吉", "魔法姬塔", "魔法吉他","魔塔", "法吉", "法鸡"],
    1256: ["碧卡拉", "ビカラ", "Vikala", "毗伽菈", "鼠鼠", "鼠大将", "鼠妹"],
    1257: ["花凛(炼金术师)", "カリン(アルケミスト)", "Karin(Alchemist)", "AKarin", "绿术", "绿发术士", "炼金恶魔", "魔绿", "术花凛"],
    1258: ["莉莉(堕落)", "リリ(フォールン)", "Riri(Fallen)", "FRiri", "莉莉"],

    1260: ["可璃亚(堕落)", "クリア(フォールン)", "Quria(Fallen)", "FQuria", "可璃亚"],
    1261: ["普蕾西亚(堕落)", "プレシア(フォールン)", "Precia(Fallen)", "FPrecia", "普雷西娅(堕天使)", "普蕾西亚", "猪妹", "普雷西娅"],
    1262: ["伊莉亚(祭服)", "イリヤ(儀装束)", "Ilya(Costume)", "Illya(Ceremonial)", "CIllya", "伊莉亚(礼服)", "礼装伊莉亚", "礼装伊莉雅", "礼装伊利亚", "礼装yly", "礼服伊莉亚", "礼服伊莉雅", "礼服伊利亚", "礼服yly", "礼亚","礼伊", "仪莉亚"],
    1263: ["雪(祭服)", "ユキ(儀装束)", "Yuki(Costume)", "Yuki(Ceremonial)", "CYuki", "雪(礼服)", "礼雪", "礼服雪", "礼服雪哥"],
    1264: ["克萝茜", "クローチェ", "Croce", "Croche", "机娘"], 
    1265: ["莱拉耶尔", "ライラエル", "Lyrael", "lailael", "傲慢", "傲慢姬", "莱莱"],
    1266: ["似似花(夏日)", "ネネカ(サマー)", "Neneka(Summer)", "SNeneka", "水花", "水448", "泳装448", "水似似花", "泳装似似花"],
    1267: ["秋乃(夏日)", "アキノ(サマー)", "Akino(Summer)", "SAkino", "水哈", "泳装秋乃", "水哈哈"],
    1268: ["优花梨(夏日)", "ユカリ(サマー)", "Yukari(Summer)", "SYukari", "水黄", "泳装黄骑", "由加莉(夏日)", "泳装酒鬼"],
    1269: ["兰法(夏日)", "ランファ(サマー)", "Ranpha(summer)", "SRanpha", "泳装兰法", "水兰", "水兰法"],
    1270: ["空花(夏日)", "クウカ(サマー)", "Kuuka(summer)", "SKuuka", "泳装空花", "水M", "水空花", "水抖M", "泳装抖M"],
    1271: ["忍(夏日)", "シノブ(サマー)", "Shinobu(summer)", "SShinobu", "水忍", "泳装忍"],
    1272: ["凯留(插班生)", "キャル(編入生)", "Kyaru(Transfer Student)", "Karyl(Student)", "TSKyaru", "凯露(插班生)", "学猫", "偷腥猫"],
    1273: ["铃奈(插班生)", "スズナ(編入生)", "Suzuna(Transfer Student)", "Suzuna(Student)", "TSSuzuna", "学暴", "雪豹"],

    1275: ["咲恋(萨拉萨利亚)", "サレン(サラサリア)", "Saren(Salasaria)", "SaSaren", "火电", "火电站", "火舞旋风", "沙电", "咲恋(沙漠)"],
    1276: ["流夏(萨拉萨利亚)", "ルカ(サラサリア)", "Ruka(Salasaria)", "SaRuka", "流沙", "沙漠流夏", "流夏(沙漠)"],
    1277: ["琳德", "リンド", "Lind", "龙姐"],
    1278: ["乌尔姆", "ヴルム", "Wurm", "龙妹", "维尔姆"],
    1279: ["贪吃佩可(圣诞节)", "ペコリーヌ(クリスマス)", "Pecorine(Christmas)", "Pecorine(Holiday)", "XPeco", "圣吃", "剩饭", "圣诞吃货", "圣诞佩可"],
    1280: ["克蕾琪塔(圣诞节)", "クレジッタ(クリスマス)", "Creditta(Christmas)", "Creditta(Holiday)", "XCreditta", "圣诞富婆", "圣婆", "圣富婆"],
    1281: ["静流(静流&璃乃)", "シズル(シズル&リノ)", "Shizuru(Shizuru&Rino)"],
    1282: ["璃乃(静流&璃乃)", "リノ(シズル&リノ)", "Rino(Shizuru&Rino)"],
    1283: ["祈梨(新年)", "イノリ(ニューイヤー)", "Inori(NewYear)", "NYInori", "春锤", "新春龙锤", "春八", "新春老八", "春龙锤"],
    1284: ["初音(新年)", "ハツネ(ニューイヤー)", "Hatsune(NewYear)", "NYHatsune", "春星", "新春初音", "星春"],
    1285: ["霞(新年)", "カスミ(ニューイヤー)", "Kasumi(NewYear)", "NYKasumi", "春驴", "新春驴", "新春香澄", "新春霞"],

    1287: ["日和(星辰)", "ヒヨリ(アストラル)", "Hiyori(Astral)", "AHiyori", "日和莉(星幽)", "日和(星幽)", "星猫", "⭐猫"],
    1288: ["怜(星辰)", "レイ(アストラル)", "Rei(Astral)", "ARei", "怜(星幽)", "星怜", "⭐怜", "星剑"],
    1289: ["优衣(星辰)", "ユイ(アストラル)", "Yui(Astral)", "AYui", "优衣(星幽)", "星优", "星u", "星优衣", "⭐优衣", "星田", "星衣", "⭐田", "⭐衣"],
    1290: ["厄里斯", "エリス", "Elis", "Eris", "els"],


    1293: ["优妮(冬日)", "ユニ(ウィンター)", "Yuni(Winter)", "WYuni", "水un", "水优妮", "水油腻", "水辈先"],
    1294: ["克萝依(冬日)", "クロエ(ウィンター)", "Kuroe(Winter)", "Chloe(Winter)", "WChloe", "水华哥", "水华"],
    1295: ["琪爱儿(冬日)", "チエル(ウィンター)", "Chieru(Winter)", "WChieru", "千爱瑠(冬日)", "水切噜", "冬切噜", "水切", "冬切"],
    1296: ["安涅默涅", "アネモネ", "Anemone", "银莲", "银莲花"],
    1297: ["涅妃涅菈", "ネフィ＝ネラ", "Nephi-Nera", "Nephi＝Nela", "Nefi=Nera", "涅妃·涅罗", "涅妃"],
    1298: ["真琴(指挥官)", "マコト(コマンダー)", "Makoto(Commander)", "CoMakoto", "战狼", "指狼", "指琴"],
    1299: ["惠理子(指挥官)", "エリコ(コマンダー)", "Eriko(Commander)", "CoEriko", "战病", "病教", "娇官", "指病", "军病"],
    1300: ["倭", "ヤマト", "Yamato", "大和"],   
    1301: ["若菜", "ワカナ", "Wakana"],
    1302: ["布武机", "フブキ", "Fubuki", "吹雪", "雌小鬼"],



  
    1307: ["镜华(春日)", "キョウカ(スプリング)", "Kyouka(Spring)", "Kyoka(Spring)", "SpKyouka", "花唯", "花仓唯", "花cw"],
    1308: ["铃莓(春日)", "スズメ(スプリング)", "Suzume(Spring)", "SpSuzume", "春日女仆", "花女仆"],
    1309: ["库露露", "クルル", "Kururu", "宝石兔", "庫露露"],
    1310: ["真布(梦想乐园)", "マホ(ドリームパーク)", "Maho(DreamPark)", "DPMaho", "梦狐"],
    1311: ["涅娅(夏日)", "ネア(サマー)", "Nea(Summer)", "SNea", "夏娅", "涅娅夏日", "夏日涅娅", "水涅娅", "涅亚夏日", "夏日涅亚", "水涅亚", "水小黄"],
    1312: ["美空(夏日)", "ミソラ(サマー)", "Misora(Summer)", "SMisora", "美空夏日", "夏日美空", "水美空"],



    1316: ["莉莉(夏日)", "リリ(サマー)", "Riri(Summer)", "SRiri", "水莉", "水莉莉", "夏日莉莉", "莉莉夏日"],
    1317: ["爱梅斯(夏日)", "アメス(サマー)", "Amesu(Summer)", "Ameth(Summer)", "SAmeth", "水爱梅斯", "sms", "夏日爱梅斯", "水爱梅丝", "夏日爱梅丝", "水梅斯"],
    1318: ["帆稀(夏日)", "ホマレ(サマー)", "Homare(Summer)", "SHomare", "水龙妈", "夏日龙妈"],
    1319: ["爱蜜莉雅(夏日)", "エミリア(サマー)", "Emiria(Summer)", "SEmilia", "夏日艾米莉亚", "水emt", "水艾米", "水爱蜜", "夏日emt", "水莉雅"],
    1320: ["艾姬多娜(夏日)", "エキドナ(サマー)", "Echidna(Summer)", "SEchidna", "夏日艾姬多娜", "夏日强欲", "水艾姬多娜", "水强欲", "强欲魔女", "强欲", "魔女", "多娜"],
    1321: ["雷姆(夏日)", "レム(サマー)", "Remu(Summer)", "SRem", "蕾姆(夏日)", "夏日雷姆", "夏日蕾姆", "水蕾姆", "水雷姆", "水雷"],
    1322: ["望(炼金术师)", "ノゾミ(アルケミスト)", "Nozomi(Alchemist)", "ANozomi", "炼金望"],
    1323: ["露易丝玛莉", "ルイズマリー", "Louise-Marie", "鹿妹"],
    1324: ["彩羽", "イロハ", "Iroha", "伊吕波"],
    1325: ["苑", "ソノ", "Sono"],


    1328: ["莱拉耶尔(圣诞节)", "ライラエル(クリスマス)", "Lyrael(Christmas)", "Lyrael(Holiday)", "XLyrael", "圣莱", "雪莱"],
    1329: ["伊绪(圣诞节)", "イオ(クリスマス)", "Io(Christmas)", "Io(Holiday)", "XIo", "圣老师", "白老师", "圣魅魔"],
    1330: ["格蕾斯", "グレイス", "Grace", "幽灵妹", "幽灵骑士"],
    1331: ["薇欧莉特", "ヴァイオレット", "Violet", "紫罗兰", "薇尔莉特"],
    1332: ["莫妮卡(新年)", "モニカ(ニューイヤー)", "Monika(NewYear)", "NYMonika", "春二力", "新二力", "春莫妮卡", "新莫妮卡", "春毛", "春力"],


    1335: ["咲恋(新年)", "サレン(ニューイヤー)", "Saren(NewYear)", "NYSaren", "春咲", "春电"],
    1336: ["美杜莎", "メドゥーサ", "Medusa"],
    1337: ["拉比林斯达(始原)", "ラビリスタ(アルファ)", "Labyrista(Alpha)", "ALabyrista", "菈比莉斯塔(始原)", "原晶", "α晶", "阿晶"],
    1338: ["似似花(始原)", "ネネカ(アルファ)", "Neneka(Alpha)", "ANeneka", "原花", "α花", "阿花"],
    1339: ["克莉丝提娜(始原)", "クリスティーナ(アルファ)", "Kurisutiina(Alpha)", "AChristina", "原克", "α克", "阿克"],
    1340: ["菲欧", "フィオ", "Fio"],


    1343: ["兰法(祭服)", "ランファ(儀装束)", "Ranpha(Costume)", "Ranpha(Ceremonial)", "CRanpha", "兰法(礼服)", "礼服兰法", "礼兰法", "礼兰"],
    1344: ["千歌(祭服)", "チカ(儀装束)", "Chika(Costume)", "Ranpha(Ceremonial)", "CChika", "千歌(礼服)", "礼服千歌", "礼千歌", "礼千"],
    1345: ["克萝茜(风灵)", "クローチェ(エアリアル)", "Croce(Aerial)", "Croche(Aerial)", "ACroche", "火机", "火鸡", "飞机"],
    1346: ["碧(驾驶员)", "アオイ(パイロット)", "Aoi(pilot)", "PAoi", "机菜", "荠菜", "机碧", "白菜"],
    1347: ["凤凰", "ホウオウ", "Phoenix", "Houou", "Ho-oh", "小凤", "肥鸡"],
    1348: ["纺希(吉欧·格黑纳)", "ツムギ(ジオ·ゲヘナ)", "Tsumugi(Geo Gehenna)", "GGTsumugi", "光裁", "吉欧裁缝"],
    1349: ["华音", "カノン", "Kanon", "花音", "伽音"],
    1350: ["厄里斯(夏日)", "エリス(サマー)", "Eris(Summer)", "SEris", "水厄里斯", "水里斯", "水els", "sls"],
    # =================================== #
    1701: ["环奈", "カンナ", "Kanna", "桥本环奈", "红二力", "毛大力", "毛小力", "毛六力", "可大萝", "大可萝", "缝合怪", "一环"],
    1702: ["环奈(振袖)", "カンナ(振袖)", "Kanna(Furisode)", "振袖环奈", "春环", "春奈", "春环奈", "二环", "振环奈", "振环", "甄嬛", "震动环", "年糕环奈", "年糕环"],







    # =================================== #
    1801: ["日和(公主)", "ヒヨリ(プリンセス)", "Hiyori(Princess)", "PHiyori", "公主日和", "公猫", "炎拳猫", "火猫", "炎拳"],
    1802: ["优衣(公主)", "ユイ(プリンセス)", "Yui(Princess)", "PYui", "公主优衣", "公主yui", "公主种田", "公主田", "公主ue", "掉毛优衣", "掉毛yui", "掉毛ue", "掉毛", "飞翼优衣", "飞翼ue", "飞翼", "飞翼高达", "飞田", "羽田", "羽衣", "毛衣", "pfue"],
    1803: ["怜(公主)", "レイ(プリンセス)", "Rei(Princess)", "PRei", "公主怜", "公剑", "风剑", "pf怜"],
    1804: ["贪吃佩可(公主)", "ペコリーヌ(プリンセス)", "Pecorine(Princess)", "Pekoriinu(Princess)", "PPecorine", "佩可莉姆(公主)", "公主吃", "公主饭", "公主吃货", "公主佩可", "公主饭团", "公主🍙", "命运高达", "高达", "命运公主", "高达公主", "命吃", "春哥高达", "🤖🍙", "🤖", "公吃", "pf吃"],
    1805: ["可可萝(公主)", "コッコロ(プリンセス)", "Kokkoro(Princess)", "PKokkoro", "公主妈", "月光妈", "蝶妈", "蝴蝶妈", "月光蝶妈", "公主可", "公主可萝", "公主可可萝", "月光可", "月光可萝", "月光可可萝", "蝶可", "蝶可萝", "蝶可可萝", "公可", "pf妈", "飞妈"],
    1806: ["凯留(公主)", "キャル(プリンセス)", "Karyl(Princess)", "Kyaru(Princess)", "PKyaru", "凯露(公主)", "公主黑猫", "公主猫", "公主猫猫头", "白猫"],
    1807: ["初音&栞", "ハツネ&シオリ", "Hatsune&Shiori", "HatsuShio", "星弓", "星栞", "双子弓", "姐妹弓", "姊妹弓", "姐妹丼", "姊妹丼", "姐妹井", "贴贴弓", "替身弓", "白金之星", "食堂泼辣酱", "初音栞", "星法栞"],
    1808: ["禊&美美&镜华", "ミソギ&ミミ&キョウカ", "Misogi&Mimi&Kyouka", "LLTrio", "小小甜心", "狱三家", "小御三家"],
    1809: ["秋乃&咲恋", "アキノ&サレン", "Akino&Saren", "AkiSaren", "咲哈哈", "哈哈电", "哈哈咲", "哈电", "电哈", "光焰"],
    1810: ["安&古蕾雅", "アン&グレア", "An&Gurea", "Anne&Grea", "双姬", "古安", "龙安"],
    1811: ["静流&璃乃", "シズル&リノ", "Shizuru&Rino", "ShizuRino", "流璃", "琉璃"],
    1812: ["雪菲(公主)", "シェフィ(プリンセス)", "Shephy(Princess)", "Shefi(Princess)", "Sheffy(Princess)", "PSheffy", "公主雪菲", "公冰", "公雪", "公主冰龙", "公菲", "白菲"],








    # =================================== #
    # 1900: ["爱梅斯", "アメス", "Amesu"],
    # 1901: ["菲欧", "フィオ", "Fio"],





    1907: ["大古", "タイゴ", "Taigo", "大吾", "鬼道大吾"],
    # 1908: ["花凛", "カリン", "Karin", "绿毛恶魔"],
    1909: ["涅比亚", "ネビア", "Nevia", "Nebia"],
    1910: ["真崎", "マサキ", "Masaki"],
    1911: ["米涅尔β", "ミネルβ", "MineruBeta", "米涅尔", "ミネル", "Mineru"],

    1913: ["和正", "カズマサ", "Kazumasa"],
    1914: ["豪绅", "ゴウシン", "Goushin"],
    # 1915: ["克蕾琪塔", "クレジッタ", "Kurejitta"],
    1916: ["基洛", "キイロ", "Kiiro"],
    1917: ["赞恩", "ゼーン", "Seen", "大舅哥", "Zane"],
    # 1918: ["兰法", "ランファ", "Ranfa", "Ranpha"],
    1919: ["阿佐尔德", "アンゾールド", "Anzoorudo", "猪哥", "Azold"],
    # 1920: ["美空", "ミソラ", "Misora"],









    # =================================== #
    4031: ["骷髅", "髑髏", "Dokuro", "骷髅老爹", "老爹"],

    9000: ["祐树", "ユウキ", "Yuuki", "骑士", "骑士君"],
}def find_chara_id(name):    """支持中文名、别名查找"""    for chara_id, names in CHARA_NAME.items():        if name in names:            return chara_id    return Nonedef parse_teams(text):    """改进的队伍解析逻辑，支持换行输入"""    teams = []    lines = [line.strip() for line in text.split('\n') if line.strip()]        for line in lines:        parts = line.split()        if len(parts) < 6:            continue  # 忽略不完整的队伍                team_name = parts[0]        characters = parts[1:6]        teams.append((team_name, characters))        return teams@sv.on_prefix('一键配队')async def team_generator_auto_save(bot, ev: CQEvent):    """自动保存配队结果的版本，最终保存单反斜杠格式"""    try:        text = ev.message.extract_plain_text().strip()        if not text:            await bot.finish(ev, '请发送：一键配队 队伍1名 角色×5 队伍2名 角色×5...\n支持换行输入')        teams = parse_teams(text)        if not teams:            await bot.finish(ev, '未识别到有效队伍格式！请确保每行有队伍名和5个角色')        results = []        errors = []        unicode_results = []                def char_to_unicode(c):            """生成时使用双反斜杠保证Python字符串安全"""            if ord(c) > 127 or c in ['\t', '\n', '【', '】']:                return f'\\u{ord(c):04x}'  # 生成时使用双反斜杠            return c                    def str_to_unicode(s):            return ''.join(char_to_unicode(c) for c in str(s))        for team_name, chars in teams:            team_header = str_to_unicode(f"【{team_name}】")            team_lines = [team_header]            missing = []                for char in chars:                cid = find_chara_id(char)                if not cid:                    missing.append(char)                    continue                        char_name = CHARA_NAME[cid][0]                char_line = f"{cid}01\t{str_to_unicode(char_name)}\t280\t5"                team_lines.append(char_line)                if missing:                error_msg = f"{team_name} 未识别角色：{'、'.join(missing)}"  # 直接显示原名称                errors.append(error_msg)            else:                team_result = '\n'.join(team_lines)                results.append(team_result)                unicode_results.append(team_result)        if not results:            error_header = str_to_unicode("⚠️ 全部队伍生成失败！")            newline = str_to_unicode('\n')            await bot.finish(ev, f"{error_header}{newline}{newline.join(errors)}")                # 自动保存到JSON文件（会在保存时转换为单反斜杠）        qq_id = ev.user_id        save_success, save_msg = modify_json_with_exact_replacement(qq_id, '\n'.join(unicode_results))                msg_parts = []        if results:            newline = str_to_unicode('\n')            msg_parts.append(f"#导入编队 4 1 ")                if errors:            error_header = str_to_unicode("\n\n⚠️ 部分错误：")            newline = str_to_unicode('\n')            msg_parts.append(f"{error_header}{newline}{newline.join(errors)}")                if not save_success:            msg_parts.append(f"\n⚠️ 自动保存失败：{save_msg}")                full_msg = ''.join(msg_parts)        await bot.send(ev, full_msg)    except Exception as e:        error_msg = str_to_unicode(f'生成配队时出错：{str(e)}')        sv.logger.error(f'配队生成错误：{str(e)}')        await bot.send(ev, error_msg)        def get_cache_path():    # 尝试多种可能的路径    possible_paths = [        os.path.join(os.path.dirname(__file__), "../../autopcr/cache/http_server"),        os.path.join(os.path.dirname(__file__), "../autopcr/cache/http_server"),        "hoshino/modules/autopcr/cache/http_server",        "modules/autopcr/cache/http_server"    ]        for path in possible_paths:        if os.path.exists(path):            return os.path.abspath(path)    return NoneBASE_PATH = get_cache_path()def modify_json_with_exact_replacement(qq_id, new_text):    """精确修改JSON文件，保持原有格式，正确处理Unicode转义"""    user_folder = os.path.join(BASE_PATH, str(qq_id))        if not os.path.exists(user_folder):        return False, f"用户文件夹 {user_folder} 不存在"    if not os.path.isdir(user_folder):        return False, f"{user_folder} 不是文件夹"        json_files = []    for file in os.listdir(user_folder):        if file.lower().endswith('.json'):            full_path = os.path.join(user_folder, file)            if os.path.isfile(full_path):                json_files.append(full_path)        if not json_files:        return False, "用户文件夹中没有找到JSON文件"        success_count = 0    for json_file in json_files:        try:            # 1. 读取原始内容（保持原有格式）            with open(json_file, 'r', encoding='utf-8') as f:                original_content = f.read()                        # 2. 处理新文本 - 中文转Unicode（单反斜杠）            processed_text = new_text.encode('unicode-escape').decode('ascii').replace('\\\\', '\\')                        # 3. 构建精确匹配模式（不改变原有JSON结构）            pattern = r'("set_my_party_text"\s*:\s*)(["\'])(.*?)(\2)'                        # 4. 执行替换（保持原有缩进和格式）            def replacer(match):                return f'{match.group(1)}{match.group(2)}{processed_text}{match.group(4)}'                        modified_content, count = re.subn(                pattern,                replacer,                original_content,                flags=re.DOTALL            )                        # 5. 如果没找到匹配项，按原有格式添加新字段            if count == 0:                config_pos = original_content.find('"config"')                if config_pos != -1:                    config_end = original_content.find('}', config_pos)                    if config_end != -1:                        # 保持原有缩进                        indent = re.search(r'\n\s*"', original_content[config_pos:config_end])                        indent = indent.group(0)[1:-1] if indent else '    '                                                modified_content = (                            original_content[:config_end] +                             f',\n{indent}"set_my_party_text": "{processed_text}"' +                             original_content[config_end:]                        )                        # 6. 验证JSON有效性（确保导入功能正常）            try:                json.loads(modified_content)            except json.JSONDecodeError as e:                sv.logger.error(f"修改后的JSON无效: {json_file}, 错误: {str(e)}")                continue                        # 7. 写入文件（完全保留原有格式）            with open(json_file, 'w', encoding='utf-8') as f:                f.write(modified_content)                        success_count += 1                    except Exception as e:            sv.logger.error(f"处理文件 {json_file} 失败: {str(e)}")            continue        return True, f"成功修改 {success_count} 个JSON文件，保持原格式"@sv.on_prefix('修改队伍')async def exact_modify_party_text(bot, ev: CQEvent):    # 获取完整消息内容    msg = ev.message.extract_plain_text()    new_text = msg[len('精确修改队伍'):].strip()        if not new_text:        await bot.finish(ev, '请提供新的队伍配置内容\n例如：精确修改队伍 [新配置内容]')        qq_id = ev.user_id    sv.logger.info(f"开始为QQ {qq_id} 修改队伍配置...")        # 检查基础路径    if not os.path.exists(BASE_PATH):        await bot.finish(ev, f"错误：基础路径 {BASE_PATH} 不存在")        # 检查用户文件夹    user_folder = os.path.join(BASE_PATH, str(qq_id))    if not os.path.exists(user_folder):        await bot.finish(ev, f"错误：您的配置文件夹 {user_folder} 不存在")        # 执行修改    success, msg = modify_json_with_exact_replacement(qq_id, new_text)        if success:        # 截取部分内容显示        preview = new_text[:100] + "..." if len(new_text) > 100 else new_text        await bot.send(ev, f'队伍配置精确修改成功！\n{msg}\n内容预览：\n{preview}')    else:        error_msg = f'修改失败: {msg}\n可能原因：\n'        error_msg += '1. JSON文件格式特殊\n'        error_msg += '2. 文件权限问题\n'        error_msg += '3. 内容包含非法字符\n'        error_msg += '请查看日志获取详细信息'        await bot.send(ev, error_msg)