#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import shutil
import re
from pathlib import Path

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)  # 项目根目录

# 配置路径
TEMPLATE_PATH = os.path.join(current_dir, "game_template.html")
JSON_PATH = os.path.join(current_dir, "blackout_games.json")
OUTPUT_DIR = os.path.join(root_dir, "games")
INDEX_PATH = os.path.join(root_dir, "index.html")

def ensure_directory(directory):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)

def load_template():
    """加载HTML模板文件"""
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"错误: 模板文件未找到: {TEMPLATE_PATH}")
        sys.exit(1)

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

def render_template(template, game):
    """使用游戏数据渲染模板"""
    # 替换普通字段
    for key, value in game.items():
        if isinstance(value, str):
            template = template.replace('{{' + key + '}}', value)
    
    # 处理标签列表
    if 'tags' in game and isinstance(game['tags'], list):
        tags_html = ""
        for tag in game['tags']:
            tags_html += f'<span class="tag text-xs px-2 py-1 rounded-full">{tag}</span>\n'
        
        # 替换标签模板部分
        template = re.sub(r'{{#tags}}.*?{{/tags}}', tags_html, template, flags=re.DOTALL)
    
    return template

def generate_game_pages(games):
    """为每个游戏生成HTML页面"""
    template = load_template()
    
    for game in games:
        # 生成游戏HTML
        game_html = render_template(template, game)
        
        # 确定输出文件路径
        output_path = os.path.join(OUTPUT_DIR, f"{game['id']}.html")
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(game_html)
        
        print(f"生成游戏页面: {output_path}")

def main():
    """主函数"""
    print("开始生成游戏页面...")
    
    # 确保输出目录存在
    ensure_directory(OUTPUT_DIR)
    
    # 加载游戏数据
    games = load_games()
    
    # 生成游戏页面
    generate_game_pages(games)
    
    print(f"完成! 生成了 {len(games)} 个游戏页面到 {OUTPUT_DIR} 目录")

if __name__ == "__main__":
    main()