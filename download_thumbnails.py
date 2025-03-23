#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from PIL import Image
import io
import json

# 目标目录
TARGET_DIR = "../assets/images/games"

# 如果目录不存在，创建它
os.makedirs(TARGET_DIR, exist_ok=True)

# 游戏缩略图URLs
THUMBNAILS = {
    "celeste": "https://cdn.cloudflare.steamstatic.com/steam/apps/504230/capsule_616x353.jpg",
    "hollow-knight": "https://cdn.cloudflare.steamstatic.com/steam/apps/367520/capsule_616x353.jpg",
    "slope": "https://play-lh.googleusercontent.com/uJn2i9h7KxYQarC_c3K4qX8f7cKd-MvRAvlnL78_QK4pPMisGVvHuIkbOQfzaLzhoQo",
    "minecraft-classic": "https://images.crazygames.com/games/minecraft-classic/cover-1591955301966.png",
    "supersmash": "https://ssb.wiki.gallery/images/thumb/5/5c/SSF2_promotional.png/1200px-SSF2_promotional.png",
    "mariokart": "https://www.mariowiki.com/images/thumb/8/8f/MK8_Deluxe_Box_Art.jpg/1200px-MK8_Deluxe_Box_Art.jpg",
    "mc2": "https://cdn.pixabay.com/photo/2016/11/18/14/00/blocks-1834846_1280.png",
    "roblox": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Roblox_player_icon_black.svg/1200px-Roblox_player_icon_black.svg.png",
    "terraria": "https://cdn.cloudflare.steamstatic.com/steam/apps/105600/capsule_616x353.jpg",
    "smb3": "https://upload.wikimedia.org/wikipedia/en/a/a5/Super_Mario_Bros._3_coverart.png",
    "world": "https://upload.wikimedia.org/wikipedia/en/3/32/Super_Mario_World_Coverart.png",
    "cookie": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Cookie_Clicker_logo.png/240px-Cookie_Clicker_logo.png"
}

def download_and_resize_image(url, output_path, size=(400, 250)):
    """下载图片并调整大小"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # 打开图片
        img = Image.open(io.BytesIO(response.content))
        
        # 调整大小
        img = img.resize(size, Image.Resampling.LANCZOS)
        
        # 保存图片
        img.save(output_path, optimize=True, quality=85)
        
        print(f"成功下载并保存: {output_path}")
        return True
    except Exception as e:
        print(f"下载失败 {url}: {str(e)}")
        return False

def update_games_json_with_thumbnails():
    """更新games.json中的缩略图路径"""
    try:
        with open('games.json', 'r', encoding='utf-8') as f:
            games_data = json.load(f)
        
        for game in games_data:
            slug = game.get('slug')
            if slug in THUMBNAILS:
                thumbnail_path = f"/assets/images/games/{slug}-thumbnail.jpg"
                game['thumbnail'] = thumbnail_path
                
                # 更新相似游戏缩略图
                if 'similar_games' in game:
                    for similar_game in game['similar_games']:
                        similar_slug = similar_game.get('slug')
                        if similar_slug and similar_slug in THUMBNAILS:
                            similar_game['thumbnail'] = f"/assets/images/games/{similar_slug}-thumbnail.jpg"
        
        with open('games.json', 'w', encoding='utf-8') as f:
            json.dump(games_data, f, ensure_ascii=False, indent=2)
            
        print("成功更新games.json中的缩略图路径")
    except Exception as e:
        print(f"更新games.json失败: {str(e)}")

def main():
    """主函数"""
    downloaded_count = 0
    
    # 下载所有缩略图
    for slug, url in THUMBNAILS.items():
        output_path = os.path.join(TARGET_DIR, f"{slug}-thumbnail.jpg")
        if download_and_resize_image(url, output_path):
            downloaded_count += 1
    
    print(f"总共下载了 {downloaded_count}/{len(THUMBNAILS)} 张缩略图")
    
    # 更新games.json
    update_games_json_with_thumbnails()

if __name__ == "__main__":
    main() 