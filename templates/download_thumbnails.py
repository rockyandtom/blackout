#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import requests
from pathlib import Path

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)  # 项目根目录

# 配置路径
JSON_PATH = os.path.join(current_dir, "blackout_games.json")
THUMBNAILS_DIR = os.path.join(root_dir, "assets", "images", "games")

# 游戏缩略图URL映射 - 使用更可靠的图片源
THUMBNAIL_URLS = {
    # 原有游戏
    "celeste-thumbnail.jpg": "https://cdn.cloudflare.steamstatic.com/steam/apps/504230/capsule_616x353.jpg",
    "hollow-knight-thumbnail.jpg": "https://cdn.cloudflare.steamstatic.com/steam/apps/367520/capsule_616x353.jpg",
    "slope-thumbnail.jpg": "https://play-lh.googleusercontent.com/uJn2i9h7KxYQarC_c3K4qH6o7gLtflFnhD_dN14MNkzHJ1NeNFzCL69jpB3QbRQtf-w=w526-h296-rw",
    "mc-thumbnail.jpg": "https://cdn.cloudflare.steamstatic.com/steam/apps/219740/capsule_616x353.jpg",
    "supersmash-thumbnail.jpg": "https://assets.nintendo.com/image/upload/c_fill,w_1200/q_auto:best/f_auto/dpr_2.0/ncom/en_US/games/switch/s/super-smash-bros-ultimate-switch/hero",
    
    # 新增游戏
    "mc2-thumbnail.jpg": "https://cdn.cloudflare.steamstatic.com/steam/apps/219740/header.jpg",
    "marioboom-thumbnail.jpg": "https://mario.wiki.gallery/images/thumb/4/44/MPS_Mario_Artwork.png/1200px-MPS_Mario_Artwork.png",
    "smb3-thumbnail.jpg": "https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_1240/b_white/f_auto/q_auto/ncom/software/nes/super-mario-bros-3/screenshot-gallery/screenshot01",
    "mariokart-thumbnail.jpg": "https://assets.nintendo.com/image/upload/c_fill,f_auto,q_auto,w_1200/v1/ncom/en_US/games/switch/m/mario-kart-8-deluxe-switch/hero",
    "morebots-thumbnail.jpg": "https://cdn.cloudflare.steamstatic.com/steam/apps/440/header.jpg",
    "bald-thumbnail.jpg": "https://assets-prd.ignimgs.com/2022/08/19/baldis-basics-plus-button-fin-1660932736566.jpg",
    "vex7-thumbnail.jpg": "https://play-lh.googleusercontent.com/FCGMLJwK1pN0Q7kiVgXlBp3fakYVZBuE5YdL5WahMCtZDOblAj_QO8pZw_uLOQhCA8c=w526-h296-rw",
    "volley-thumbnail.jpg": "https://cdn1.epicgames.com/salesEvent/salesEvent/EGS_SpikingVolleyballOnline_NeturalInfo_S2_1200x1600-19ac2aeed45bb51e2240e4e6590809cc",
    "soccer-thumbnail.jpg": "https://cdn1.epicgames.com/salesEvent/salesEvent/EGS_EASPORTSFIFAFOOTBALL_EACanada_S2_1200x1600-5384a4b823d3affda90e9e8c8d24e91a",
    "cookie-thumbnail.jpg": "https://play-lh.googleusercontent.com/OssE3ON9WsLZedOF39UCgtIHcRYfV0OqQS9O78LfmRdxSyKdHX52G2OFa0LkG6D-k9w",
    "world-thumbnail.jpg": "https://play-lh.googleusercontent.com/RV0A_nkW3MgZg86chdkRzKa10v4GR_cbYPPkLTdFg6zNP8M45KDvYYxyKs6HGmtwoWy7"
}

def ensure_directory(directory):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)

def load_games():
    """加载游戏数据JSON文件"""
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"错误: JSON文件未找到: {JSON_PATH}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"错误: JSON文件格式不正确: {JSON_PATH}")
        sys.exit(1)

def download_image(url, filename):
    """从URL下载图片并保存到指定路径"""
    try:
        # 添加User-Agent头，模拟浏览器请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, stream=True, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"已下载: {filename}")
            return True
        else:
            print(f"下载失败: {url}, 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"下载出错: {url}, 错误: {e}")
        return False

def main():
    """主函数"""
    print("游戏缩略图下载器启动...")
    
    # 确保目标目录存在
    ensure_directory(THUMBNAILS_DIR)
    
    # 下载预定义的缩略图
    for filename, url in THUMBNAIL_URLS.items():
        output_path = os.path.join(THUMBNAILS_DIR, filename)
        if not os.path.exists(output_path):
            print(f"下载 {filename}...")
            download_image(url, output_path)
        else:
            print(f"已存在: {filename}")
    
    print("缩略图下载完成!")

if __name__ == "__main__":
    main() 