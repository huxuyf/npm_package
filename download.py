"""
前端资源批量下载脚本
下载 Font Awesome 字体、Leaflet 插件图标等缺失资源
"""

import os
import urllib.request
import urllib.error
from urllib.parse import urlparse, unquote

# 资源列表：(URL, 本地保存路径)
RESOURCES = [
    # ========== Font Awesome 字体文件 ==========
    (
        "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/webfonts/fa-solid-900.woff2",
        "webfonts/fa-solid-900.woff2"
    ),
    (
        "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/webfonts/fa-solid-900.ttf",
        "webfonts/fa-solid-900.ttf"
    ),
    (
        "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/webfonts/fa-regular-400.woff2",
        "webfonts/fa-regular-400.woff2"
    ),
    (
        "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/webfonts/fa-brands-400.woff2",
        "webfonts/fa-brands-400.woff2"
    ),
    
    # ========== Leaflet.fullscreen 图标 ==========
    (
        "https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/icon-fullscreen.svg",
        "css/icon-fullscreen.svg"
    ),
    (
        "https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/icon-fullscreen@2x.svg",
        "css/icon-fullscreen@2x.svg"
    ),
    
    # ========== Leaflet 核心图片资源 ==========
    (
        "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/images/layers.png",
        "css/images/layers.png"
    ),
    (
        "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/images/layers-2x.png",
        "css/images/layers-2x.png"
    ),
    (
        "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/images/marker-icon.png",
        "css/images/marker-icon.png"
    ),
    (
        "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/images/marker-icon-2x.png",
        "css/images/marker-icon-2x.png"
    ),
    (
        "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/images/marker-shadow.png",
        "css/images/marker-shadow.png"
    ),
]

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_filename(url):
    """从URL提取文件名"""
    path = urlparse(url).path
    return unquote(path.split("/")[-1]) or "unknown"

def download_file(url, save_path, max_retries=3):
    """下载单个文件，带重试机制"""
    filename = os.path.basename(save_path)
    print(f"⬇️  {filename}", end=" ... ")
    
    # 创建目录
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                
            with open(save_path, "wb") as f:
                f.write(data)
            
            size_kb = len(data) / 1024
            print(f"✅ {size_kb:.1f}KB")
            return True
            
        except urllib.error.URLError as e:
            if attempt < max_retries - 1:
                print(f"\n   重试 {attempt+1}/{max_retries}... ", end="")
                continue
            else:
                print(f"❌ 失败: {e.reason}")
                return False
        except Exception as e:
            print(f"❌ 异常: {e}")
            return False
    
    return False


def main():
    print("="*60)
    print("🚀 前端资源批量下载脚本")
    print("="*60 + "\n")
    
    success = fail = 0
    
    # 下载常规资源
    print("📦 下载字体和图标资源...\n")
    for url, save_path in RESOURCES:
        if download_file(url, save_path):
            success += 1
        else:
            fail += 1
    
    # 下载 Leaflet.awesome-markers 图片（从 jsDelivr）
    print("\n🖼️  下载 Leaflet.awesome-markers 图标...")
    marker_images = [
        "markers.png", "markers-soft.png", "markers-shadow.png",
        "markers@2x.png", "markers-soft@2x.png", "markers-shadow@2x.png"
    ]
    img_base = "https://cdn.jsdelivr.net/npm/leaflet.awesome-markers@2.0.2/dist/images/"
    
    for img in marker_images:
        url = img_base + img
        save_path = os.path.join("css", "images", img)
        if download_file(url, save_path):
            success += 1
        else:
            fail += 1
    
    # 汇总
    print("\n" + "="*60)
    print(f"📊 下载结果: ✅ 成功 {success} 个 | ❌ 失败 {fail} 个")
    print("="*60)
    
    # 目录结构提示
    print("\n📁 建议的目录结构:")
    print("""
    your-project/
    ├── css/
    │   ├── icon-fullscreen.svg
    │   ├── icon-fullscreen@2x.svg
    │   └── images/
    │       ├── layers.png
    │       ├── layers-2x.png
    │       ├── marker-icon.png
    │       ├── marker-icon-2x.png
    │       ├── marker-shadow.png
    │       └── markers*.png (awesome-markers)
    ├── webfonts/
    │   ├── fa-solid-900.woff2
    │   ├── fa-solid-900.ttf
    │   ├── fa-regular-400.woff2
    │   └── fa-brands-400.woff2
    └── tiles/ (可选，OpenStreetMap瓦片)
        └── osm/
            └── {zoom}/{x}/{y}.png
    """)
    
    
    if fail > 0:
        print(f"\n⚠️  {fail} 个文件下载失败，请检查网络连接或手动下载")

if __name__ == "__main__":
    main()