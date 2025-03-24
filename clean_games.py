#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理游戏页面，只保留指定的5个游戏
"""

import os
import glob
import shutil
import json

def main():
    print("=== 开始清理游戏页面 ===")
    
    # 要保留的游戏ID列表
    keep_games = [
        "fruit-ninja",
        "super-mario-construct",
        "soccer-skills",
        "cookie-clicker",
        "super-smash-bros"
    ]
    
    # 1. 清理游戏页面文件夹
    games_dir = "games"
    if os.path.exists(games_dir):
        # 获取所有HTML文件
        html_files = glob.glob(os.path.join(games_dir, "*.html"))
        
        for html_file in html_files:
            filename = os.path.basename(html_file)
            game_id = os.path.splitext(filename)[0]
            
            # 检查是否在保留列表中
            if game_id not in keep_games:
                os.remove(html_file)
                print(f"删除游戏页面: {html_file}")
    else:
        print(f"目录不存在: {games_dir}")
        os.makedirs(games_dir)
        print(f"创建目录: {games_dir}")
    
    # 2. 删除不再使用的图片（可选）
    # 由于图片可能在其他地方被使用，所以这一步是可选的，小心执行
    images_dir = os.path.join("assets", "images", "games")
    if os.path.exists(images_dir):
        # 获取相关的图片文件
        required_images = [
            "fruit-thumbnail.jpg",
            "smc-thumbnail.jpg", 
            "soccer-thumbnail.jpg",
            "cookie-thumbnail.jpg",
            "supersmash-thumbnail.jpg"
        ]
        
        for image_file in os.listdir(images_dir):
            if image_file not in required_images:
                # 保险起见，只打印而不实际删除
                print(f"发现不需要的图片: {os.path.join(images_dir, image_file)}")
    else:
        print(f"目录不存在: {images_dir}")
    
    print("=== 游戏页面清理完成 ===")

if __name__ == "__main__":
    main() 