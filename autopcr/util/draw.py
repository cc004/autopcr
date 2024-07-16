import os, io
from typing import List
from PIL import Image, ImageFont 
from ..constants import DATA_DIR
from .draw_table import grid2img

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

    async def draw_tasks_result(self, data: "TaskResult") -> Image.Image:
        content = []
        header = ["序号", "名字","配置","状态","结果"]
        result = data.result
        cnt = 0
        for key in data.order:
            value = result[key]
            if value.log == "功能未启用":
                continue
            cnt += 1
            content.append([str(cnt), value.name.strip(), value.config.strip(), "#"+value.status.value, value.log.strip()])
        img = await self.draw(header, content)
        return img

    async def draw_task_result(self, data: "ModuleResult") -> Image.Image:
        content = [["配置", data.config.strip()], ["状态", "#"+data.status.value], ["结果", data.log.strip()]]
        header = ["名字", data.name.strip()]
        img = await self.draw(header, content)
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
    
    async def img2bytesio(self, img: Image.Image) -> io.BytesIO:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        return img_byte_arr

instance = Drawer()
