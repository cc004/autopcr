import os, io, re  
from typing import Dict, List  
from PIL import Image, ImageFont, ImageDraw  
from ..constants import DATA_DIR, CACHE_DIR  
from .draw_table import grid2img, json2img  
from pathlib import Path  
from ..db.imagemgr import instance as imgmgr    
class Drawer():  
  
    font_path = os.path.join(DATA_DIR, "微软雅黑.ttf")  
    font=ImageFont.truetype(font_path, size=30)  
  
    def dark_color(self):  
        return {  
            'bg': '#222529',  
            'odd_row_cell_bg': '#3A3A3C',  
            'even_row_cell_bg': '#2C2C2E',  
            'header_bg': '#1C1C1E',  
            'font': '#DFE2E6',  
            'rowline': 'white',  
            'colline': 'white',  
            '成功': '#255035',  
            '跳过': '#35778D',  
            '警告': '#FF8C00',  
            '中止': '#937526',  
            '错误': '#79282C',  
            '致命': '#8B0000',  
        }  
  
    def light_color(self):  
        return {  
            'bg': 'white',  
            'odd_row_cell_bg': '#EEEEEE',  
            'even_row_cell_bg': 'white',  
            'header_bg': '#C8C8C9',  
            'font': 'black',  
            'rowline': 'black',  
            'colline': 'black',  
            '成功': '#E1FFB5',  
            '跳过': '#C8D6FA',  
            '警告': '#FFD700',  
            '中止': 'yellow',  
            '错误': 'red',  
            '致命': '#8B0000',  
        }  
  
    def color(self):  
        from datetime import datetime  
        now = datetime.now()  
        is_night = not(now.hour < 18 and now.hour > 7)  
        if is_night:  
            return self.dark_color()  
        else:  
            return self.light_color()  
  
    async def draw(self, header: List[str], content: List[List[str]]) -> Image.Image:  
        img = grid2img(content, header, colors=self.color(), font=self.font, stock=True)  
        return img  
  
    async def draw_json(self, titles: List[str], records: List[Dict]) -> Image.Image:  
        img = json2img(records, titles, colors=self.color(), font=self.font, stock=True)  
        return img  
  
    #过滤了跳过的内容
    async def draw_tasks_result(self, data: "TaskResult", skip_skipped: bool = False) -> Image.Image:  
        content = []  
        header = ["序号", "名字","配置","状态","结果"]  
        result = data.result  
        cnt = 0  
        for key in data.order:  
            value = result[key]  
            if value.log == "功能未启用":  
                continue  
            if skip_skipped and value.status.value == "跳过":  
                continue  
            cnt += 1  
            content.append([str(cnt), value.name.strip(), value.config.strip(), "#"+value.status.value, value.log.strip()])  
        img = await self.draw(header, content)  
        return img
  
    async def draw_task_result(self, data: "ModuleResult") -> Image.Image:  
        # 「我的支援」：日志同时含 [unit: 和 [ex:，必须先判断 [unit:  
        if '[unit:' in data.log:  
            return await self.draw_my_support_result(data)  
        # 检测是否包含EX装备图标标记  
        if '[ex:' in data.log:  
            return await self.draw_ex_equip_result(data)
        if data.table and data.table.data and len(data.table.data) > 1:  
            return await self.draw_task_table(data)  
        content = [["配置", data.config.strip()], ["状态", f"#{data.status.value}"], ["结果", data.log.strip()]]  
        header = ["名字", data.name.strip()]  
        img = await self.draw(header, content)  
        return img  
  
    async def draw_ex_equip_result(self, data: "ModuleResult") -> Image.Image:  
        """渲染带EX装备图标的预览图"""  
  
        colors = self.color()  
        font = self.font  
  
        ICON_SIZE = 144  
        LINE_HEIGHT = max(ICON_SIZE + 8, 44)  
        HEADER_LINE_HEIGHT = 40  
        LEFT_MARGIN = 12  
        ICON_TEXT_GAP = 8  
        TOP_MARGIN = 10  
        RIGHT_MARGIN = 20  
  
        # 解析log，提取 [ex:XXXXXXX] 标记  
        log_text = data.log.strip()  
        raw_lines = log_text.split('\n')  
  
        ex_pattern = re.compile(r'^\[ex:(\d+)\](.*)')  
  
        parsed_lines = []  # list of (equip_id 或 None, 显示文本)  
        for line in raw_lines:  
            m = ex_pattern.match(line)  
            if m:  
                equip_id = int(m.group(1))  
                text = m.group(2)  
                parsed_lines.append((equip_id, text))  
            else:  
                parsed_lines.append((None, line))  
  
        # 加载图标（使用 imagemgr，会自动下载缓存）  
        icon_cache = {}  
        for equip_id, _ in parsed_lines:  
            if equip_id and equip_id not in icon_cache:  
                try:  
                    icon = await imgmgr.ex_equip_icon(equip_id)  
                    if icon:  
                        icon_cache[equip_id] = icon  
                except Exception:  
                    pass  
  
        # 头部信息（config 可能有多行，逐行拆分）  
        header_texts = [f"【{data.name.strip()}】"]  
        for line in data.config.strip().split('\n'):  
            line = line.strip()  
            if line:  
                header_texts.append(line)
  
        # 计算画布尺寸  
        dummy_img = Image.new('RGB', (1, 1))  
        dummy_draw = ImageDraw.Draw(dummy_img)  
  
        max_width = 0  
        for text in header_texts:  
            bbox = dummy_draw.textbbox((0, 0), text, font=font)  
            max_width = max(max_width, bbox[2] - bbox[0])  
  
        for equip_id, text in parsed_lines:  
            bbox = dummy_draw.textbbox((0, 0), text, font=font)  
            tw = bbox[2] - bbox[0]  
            line_width = LEFT_MARGIN + ICON_SIZE + ICON_TEXT_GAP + tw + RIGHT_MARGIN  
            max_width = max(max_width, line_width)  
  
        canvas_width = int(max_width + LEFT_MARGIN + RIGHT_MARGIN)  
        canvas_height = int(  
            TOP_MARGIN +  
            len(header_texts) * HEADER_LINE_HEIGHT +  
            10 +  
            len(parsed_lines) * LINE_HEIGHT +  
            TOP_MARGIN  
        )  
  
        bg_color = colors['bg']  
        font_color = colors['font']  
  
        canvas = Image.new('RGB', (canvas_width, canvas_height), bg_color)  
        draw = ImageDraw.Draw(canvas)  
  
        # 绘制头部  
        y = TOP_MARGIN  
        for text in header_texts:  
            draw.text((LEFT_MARGIN, y), text, font=font, fill=font_color)  
            y += HEADER_LINE_HEIGHT  
  
        # 分隔线  
        y += 5  
        draw.line([(LEFT_MARGIN, y), (canvas_width - RIGHT_MARGIN, y)], fill=font_color)  
        y += 5  
  
        # 绘制日志行（带图标）  
        for equip_id, text in parsed_lines:  
            icon_img = icon_cache.get(equip_id) if equip_id else None  
  
            if icon_img:  
                resized = icon_img.copy().resize(  
                    (ICON_SIZE, ICON_SIZE),  
                    Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS  
                )  
                icon_y = y + (LINE_HEIGHT - ICON_SIZE) // 2  
                if resized.mode == 'RGBA':  
                    canvas.paste(resized, (LEFT_MARGIN, icon_y), resized)  
                else:  
                    canvas.paste(resized, (LEFT_MARGIN, icon_y))  
                text_x = LEFT_MARGIN + ICON_SIZE + ICON_TEXT_GAP  
            else:  
                # 没有图标的行，文本也从同一位置开始（保持对齐）  
                text_x = LEFT_MARGIN + ICON_SIZE + ICON_TEXT_GAP  
  
            bbox = draw.textbbox((0, 0), text, font=font)  
            text_h = bbox[3] - bbox[1]  
            text_y = y + (LINE_HEIGHT - text_h) // 2  
            draw.text((text_x, text_y), text, font=font, fill=font_color)  
            y += LINE_HEIGHT  
  
        return canvas  
  
    async def draw_my_support_result(self, data: "ModuleResult") -> Image.Image:  
        """我的支援：同类角色横向并列，角色直接转头像，下面纵向列出其EX装备"""  
        colors = self.color()  
        font = self.font  
        name_font = ImageFont.truetype(self.font_path, size=22)  
        ex_font = ImageFont.truetype(self.font_path, size=22)  
  
        AVATAR_SIZE = 96  
        EX_ICON_SIZE = 56  
        EX_TEXT_GAP = 6  
        EX_LINE_HEIGHT = EX_ICON_SIZE + 6  
        CARD_PADDING = 12  
        CARD_GAP = 16  
        CAT_TITLE_HEIGHT = 46  
        NAME_HEIGHT = 30  
        TOP_MARGIN = 12  
        LEFT_MARGIN = 16  
        ROW_GAP = 18  
  
        cat_pattern = re.compile(r'^【(.*)】$')  
        unit_pattern = re.compile(r'^\[unit:(\d+)\](.*)')  
        ex_pattern = re.compile(r'^\[ex:(\d+)\](.*)')  
  
        # 解析成 分类 -> 角色 -> EX 三层结构  
        categories = []  
        cur_cat = None  
        cur_char = None  
        for raw in data.log.strip().split('\n'):  
            line = raw.strip()  
            if not line:  
                continue  
            mc = cat_pattern.match(line)  
            mu = unit_pattern.match(line)  
            me = ex_pattern.match(line)  
            if mc:  
                cur_cat = {"title": mc.group(1), "chars": [], "empty": None}  
                categories.append(cur_cat)  
                cur_char = None  
            elif mu:  
                cur_char = {"unit_id": int(mu.group(1)), "exs": []}  
                if cur_cat is not None:  
                    cur_cat["chars"].append(cur_char)  
            elif me:  
                if cur_char is not None:  
                    cur_char["exs"].append((int(me.group(1)), me.group(2).strip()))  
            else:  
                if cur_cat is not None and not cur_cat["chars"]:  
                    cur_cat["empty"] = line  
  
        # 从 db 取角色名（不依赖日志文本）  
        from ..db.database import db  
  
        # 预加载头像与EX图标  
        unit_icons, ex_icons = {}, {}  
        for cat in categories:  
            for ch in cat["chars"]:  
                uid = ch["unit_id"]  
                if uid not in unit_icons:  
                    try:  
                        ic = await imgmgr.unit_icon(uid)  
                        if ic:  
                            unit_icons[uid] = ic  
                    except Exception:  
                        pass  
                for ex_id, _ in ch["exs"]:  
                    if ex_id not in ex_icons:  
                        try:  
                            ic = await imgmgr.ex_equip_icon(ex_id)  
                            if ic:  
                                ex_icons[ex_id] = ic  
                        except Exception:  
                            pass  
  
        dummy = ImageDraw.Draw(Image.new('RGB', (1, 1)))  
        def text_w(txt, f):  
            b = dummy.textbbox((0, 0), txt, font=f)  
            return b[2] - b[0]  
  
        def card_size(ch):  
            name = db.get_unit_name(ch["unit_id"])  
            max_ex_text = 0  
            for _, t in ch["exs"]:  
                max_ex_text = max(max_ex_text, text_w(t, ex_font))  
            content_w = max(AVATAR_SIZE, text_w(name, name_font),  
                            EX_ICON_SIZE + EX_TEXT_GAP + max_ex_text)  
            w = CARD_PADDING * 2 + content_w  
            ex_h = max(1, len(ch["exs"])) * EX_LINE_HEIGHT  
            h = CARD_PADDING * 2 + AVATAR_SIZE + NAME_HEIGHT + ex_h  
            return w, h  
  
        # 布局计算  
        canvas_width = 220  
        row_infos = []  
        for cat in categories:  
            if cat["chars"]:  
                widths, row_h = [], 0  
                for ch in cat["chars"]:  
                    w, h = card_size(ch)  
                    widths.append(w)  
                    row_h = max(row_h, h)  
                row_w = LEFT_MARGIN * 2 + sum(widths) + CARD_GAP * (len(widths) - 1)  
                canvas_width = max(canvas_width, row_w)  
                row_infos.append((cat, row_h, widths))  
            else:  
                row_infos.append((cat, 44, []))  
            canvas_width = max(canvas_width, LEFT_MARGIN * 2 + text_w(f"【{cat['title']}】", font))  
  
        canvas_height = TOP_MARGIN  
        for (_, row_h, _) in row_infos:  
            canvas_height += CAT_TITLE_HEIGHT + row_h + ROW_GAP  
  
        canvas = Image.new('RGB', (int(canvas_width), int(canvas_height)), colors['bg'])  
        draw = ImageDraw.Draw(canvas)  
        font_color = colors['font']  
        resample = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS  
  
        y = TOP_MARGIN  
        for (cat, row_h, widths) in row_infos:  
            draw.text((LEFT_MARGIN, y + 6), f"【{cat['title']}】", font=font, fill=font_color)  
            y += CAT_TITLE_HEIGHT  
            if not cat["chars"]:  
                draw.text((LEFT_MARGIN + 12, y), cat["empty"] or "无", font=name_font, fill=font_color)  
                y += row_h + ROW_GAP  
                continue  
            # 每个分类按角色数等分成 N 个等宽格子，卡片在各自格子内居中  
            n = len(cat["chars"])  
            cell_w = canvas_width // n  
            for i, (ch, cw) in enumerate(zip(cat["chars"], widths)):  
                cell_x = i * cell_w  
                card_x = cell_x + (cell_w - cw) // 2   # 卡片在格子内居中  
                # 头像（在卡片内居中）  
                av = unit_icons.get(ch["unit_id"])  
                av_x = card_x + (cw - AVATAR_SIZE) // 2  
                if av:  
                    r = av.copy().resize((AVATAR_SIZE, AVATAR_SIZE), resample)  
                    if r.mode == 'RGBA':  
                        canvas.paste(r, (av_x, y + CARD_PADDING), r)  
                    else:  
                        canvas.paste(r, (av_x, y + CARD_PADDING))  
                # 角色名（db 取，画在头像下方）  
                name = db.get_unit_name(ch["unit_id"])  
                name_y = y + CARD_PADDING + AVATAR_SIZE + 2  
                nx = card_x + (cw - text_w(name, name_font)) // 2  
                draw.text((nx, name_y), name, font=name_font, fill=font_color)  
                # EX 装备（图标+文字，纵向）  
                ex_y = name_y + NAME_HEIGHT  
                ex_x = card_x + CARD_PADDING  
                if not ch["exs"]:  
                    draw.text((ex_x, ex_y), "无EX装备", font=ex_font, fill=font_color)  
                for ex_id, t in ch["exs"]:  
                    icon = ex_icons.get(ex_id)  
                    if icon:  
                        ri = icon.copy().resize((EX_ICON_SIZE, EX_ICON_SIZE), resample)  
                        if ri.mode == 'RGBA':  
                            canvas.paste(ri, (ex_x, ex_y), ri)  
                        else:  
                            canvas.paste(ri, (ex_x, ex_y))  
                    tb = draw.textbbox((0, 0), t, font=ex_font)  
                    th = tb[3] - tb[1]  
                    draw.text((ex_x + EX_ICON_SIZE + EX_TEXT_GAP, ex_y + (EX_ICON_SIZE - th) // 2),  
                              t, font=ex_font, fill=font_color)  
                    ex_y += EX_LINE_HEIGHT  
            y += row_h + ROW_GAP
  
        return canvas
    
    async def draw_task_table(self, data: "ModuleResult") -> Image.Image:  
        content = data.table.data  
        header = data.table.header  
        img = await self.draw_json(header, content)  
        return img  
  
    async def draw_msgs(self, msgs: List[str]) -> Image.Image:  
        content = [[msg] for msg in msgs]  
        img = await self.draw(["结果"], content)  
        return img  
  
    async def horizon_concatenate(self, images_path: List[str]):  
        images = [Image.open(i) for i in images_path]  
        widths, heights = zip(*(i.size  for i in images))  
  
        max_height = max(heights)  
        total_widths = sum(widths)  
  
        new_image = Image.new('RGB', (total_widths, max_height))  
  
        x_offset = 0  
        for img in images:  
            new_image.paste(img, (x_offset, 0))  
            x_offset += img.size[0]  
  
        return new_image  
      
    async def img2bytesio(self, img: Image.Image, format: str = 'JPEG') -> io.BytesIO:  
        img_byte_arr = io.BytesIO()  
        img.save(img_byte_arr, format=format)  
        img_byte_arr.seek(0)  
        return img_byte_arr  
  
instance = Drawer()