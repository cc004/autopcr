#type: ignore
from typing import List
from .assetmgr import instance as assetmgr
from ..constants import CACHE_DIR
from pathlib import Path
from PIL import Image

class imagemgr:
    def __init__(self):
        self.path = Path(CACHE_DIR) / "image"
        self.path.mkdir(parents=True, exist_ok=True)
        self.ver = None

    async def update_image(self, mgr: assetmgr):
        self.ver = mgr.ver

    def get_image_path(self, prefix: str, image_name: str) -> Path:
        return self.path / f"{prefix}_{image_name}"

    async def get_image(self, prefix: str, image_name: str) -> Image:
        path = self.get_image_path(prefix, image_name)
        if path.exists():
            return Image.open(path)
        try:
            image = await assetmgr.get_image(prefix, image_name)
        except Exception:
            return None
        image.save(path)
        return image

    def unit_icon_url(self, unit_id: int, star: int = 3) -> str:
        if unit_id > 100000:
            unit_id //= 100
        star = next((s for s in [6, 3, 1] if s <= star), 3)
        unit = unit_id * 100 + star * 10 + 1
        url = f"/daily/image/unit_icon_unit_{unit}.png"
        return url

    async def unit_icon(self, unit_id: int, star: int = 3) -> Image:
        if unit_id > 100000:
            unit_id //= 100
        star = next((s for s in [6, 3, 1] if s <= star), 3)
        unit = unit_id * 100 + star * 10 + 1
        path = self.get_image_path("unit_icon", f"unit_{unit}.png")  
        if path.exists():  
            return Image.open(path)  
        # 优先从 HoshinoBot priconne 本地资源目录读取  
        hoshino_path = Path(r"C:\Resources\img\priconne\unit") / f"icon_unit_{unit}.png"  
        if hoshino_path.exists():  
            return Image.open(hoshino_path)  
        try:  
            image = await assetmgr.unit_icon(unit)  
        except Exception:  
            return None  
        image.save(path)  
        return image

    async def ex_equip_icon(self, equip_id: int) -> Image:
        path = self.get_image_path("icon_icon", f"extra_equip_{equip_id}.png")
        if path.exists():
            return Image.open(path)
        try:
            image = await assetmgr.ex_equip_icon(equip_id)
        except Exception:
            return None
        image.save(path)
        return image

# should lock before use
instance = imagemgr()
