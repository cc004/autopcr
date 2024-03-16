import asyncio
import aiohttp
from requests import get
import os
import shutil

async def get_latest_release_info(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = get(url)
    if response.ok:
        release_info = response.json()
        tag_name = release_info['tag_name']
        assets = release_info['assets']
        asset_download_urls = [asset['browser_download_url'] for asset in assets]
        return tag_name, asset_download_urls
    else:
        print(response.status_code)
        print(response.json())
        return None, None

path = os.path.dirname(os.path.abspath(__file__))

async def check_version(version):
    now_version = None
    web_version = os.path.join(path, "autopcr", "http_server", "client_version")
    if os.path.exists(web_version):
        with open(web_version, "r") as f:
            now_version = f.read().strip()
    version = version.strip()
    if not now_version or now_version != version:
        return True
    return False

async def save_version(version):
    web_version = os.path.join(path, "autopcr", "http_server", "client_version")
    with open(web_version, "w") as f:
        f.write(version)

async def download_assets(asset_download_urls):
    web_path = os.path.join(path, "autopcr", "http_server", "ClientApp")
    if not os.path.exists(web_path):
        os.makedirs(web_path)
    async with aiohttp.ClientSession() as session:
        for url in asset_download_urls:
            async with session.get(url) as response:
                if response.status == 200:
                    filename = url.split('/')[-1]
                    print(f"Downloading {filename}")
                    filepath = os.path.join(path, filename)
                    with open(filepath, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    print(f"Downloaded {filename}")

                    shutil.rmtree(web_path)
                    print(f"Removed old web file")

                    import zipfile
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        zip_ref.extractall(web_path)
                    print(f"Unzipped {filename}")

                    os.remove(filepath)
                    print(f"Delete {filename}")
                else:
                    print(f"Failed to download {url}")
                    raise Exception(f"Failed to download {url}")

async def do_download():
    owner = 'Lanly109'
    repo = 'AutoPCR_Web'
    latest_release_tag, asset_download_urls = await get_latest_release_info(owner, repo)
    if latest_release_tag and asset_download_urls:
        print(f"Latest release tag: {latest_release_tag}")
        if await check_version(latest_release_tag):
            await download_assets(asset_download_urls)
            await save_version(latest_release_tag)
        else:
            print("Already up to date")
    else:
        print("Failed to fetch latest release info")
        raise Exception("Failed to fetch latest release info")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_download())
