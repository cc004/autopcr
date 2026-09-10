import asyncio  
import os  
import sys  
from pathlib import Path  
  
sys.path.insert(0, str(Path(__file__).parent))  
  
import UnityPy  
from PIL import Image  
  
from autopcr.db.dbstart import db_start  
from autopcr.db.database import db  
from autopcr.db.assetmgr import instance as assetmgr  
from autopcr.constants import CACHE_DIR  
  
IMAGE_DIR = Path(CACHE_DIR) / "image"  
  
async def extract_image(bundle_url: str):  
    data = await assetmgr.download(bundle_url)  
    UnityPy.config.FALLBACK_UNITY_VERSION = "2021.3.20f1"  
    env = UnityPy.load(data)  
    for obj in env.objects:  
        if obj.type.name in ("Texture2D", "Sprite"):  
            return obj.read().image  
    return None  
  
async def main():  
    print("==== 初始化数据库中... ====")  
    await db_start()  
  
    print(f"EX装备数据：{len(db.ex_equipment_data)} 条")  
  
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)  
  
    print("\n==== 开始下载EX装备图标 ====")  
    for ex_id in db.ex_equipment_data:  
        path = IMAGE_DIR / f"icon_icon_extra_equip_{ex_id}.png"  
        bundle_url = f"a/icon_icon_extra_equip_{ex_id}.unity3d"  
  
        if path.exists():  
            continue  
        if bundle_url not in assetmgr.registries:  
            print(f"跳过EX装备: {ex_id} (资源不存在)")  
            continue  
  
        print(f"下载EX装备: {ex_id}")  
        try:  
            image = await extract_image(bundle_url)  
            if image:  
                image.save(path)  
        except Exception as e:  
            print(f"失败: {ex_id} - {e}")  
  
    print("\n==== 所有资源下载完成！====")  
  
if __name__ == "__main__":  
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(main())