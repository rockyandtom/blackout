#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除Blackout游戏和相关资源的脚本
"""

import os
import json
import shutil

def main():
    print("=== 开始删除Blackout游戏和相关资源 ===")
    
    # 1. 删除Blackout游戏页面
    blackout_html = os.path.join("games", "blackout.html")
    if os.path.exists(blackout_html):
        os.remove(blackout_html)
        print(f"已删除: {blackout_html}")
    else:
        print(f"文件不存在: {blackout_html}")
    
    # 2. 从JSON数据文件中移除Blackout游戏
    json_file = os.path.join("templates", "blackout_games.json")
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 过滤掉Blackout游戏
            filtered_data = [game for game in data if game.get("id") != "blackout"]
            
            # 如果有变化，保存回文件
            if len(filtered_data) < len(data):
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(filtered_data, f, ensure_ascii=False, indent=2)
                print(f"已从{json_file}中移除Blackout游戏数据")
            else:
                print(f"{json_file}中没有找到Blackout游戏数据")
        except Exception as e:
            print(f"处理{json_file}时出错: {e}")
    else:
        print(f"文件不存在: {json_file}")
    
    # 3. 可选：移除Blackout相关图片
    blackout_image = os.path.join("assets", "images", "games", "blackout-thumbnail.jpg")
    if os.path.exists(blackout_image):
        os.remove(blackout_image)
        print(f"已删除: {blackout_image}")
    else:
        print(f"文件不存在: {blackout_image}")
        
    print("=== Blackout游戏和相关资源删除完成 ===")

if __name__ == "__main__":
    main() 