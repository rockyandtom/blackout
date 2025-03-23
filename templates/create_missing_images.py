#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from pathlib import Path

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)  # 项目根目录

# 图片目录
IMAGES_DIR = os.path.join(root_dir, "assets", "images", "games")

# 需要检查的图片文件名列表
REQUIRED_IMAGES = [
    "blackout-thumbnail.jpg",
    "fruit-thumbnail.jpg",
    "smc-thumbnail.jpg",
    "metro-thumbnail.jpg",
    "celeste-thumbnail.jpg",
    "hollow-knight-thumbnail.jpg",
    "slope-thumbnail.jpg",
    "mc-thumbnail.jpg",
    "supersmash-thumbnail.jpg"
]

def ensure_directory(directory):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)

def check_and_fix_images():
    """检查并修复缺失的图片"""
    ensure_directory(IMAGES_DIR)
    
    # 获取现有图片列表
    existing_images = os.listdir(IMAGES_DIR)
    existing_images = [f for f in existing_images if f.endswith('.jpg') and not f.startswith('.')]
    
    if not existing_images:
        print("错误: 没有找到任何图片")
        return
    
    # 获取第一个可用的图片作为备用
    fallback_image = os.path.join(IMAGES_DIR, existing_images[0])
    
    print(f"现有图片: {existing_images}")
    print(f"备用图片: {fallback_image}")
    
    # 检查并修复缺失的图片
    for image_name in REQUIRED_IMAGES:
        image_path = os.path.join(IMAGES_DIR, image_name)
        if not os.path.exists(image_path):
            print(f"创建缺失的图片: {image_name}")
            shutil.copy(fallback_image, image_path)
        else:
            print(f"已存在: {image_name}")

def main():
    """主函数"""
    print("开始检查缺失的图片...")
    check_and_fix_images()
    print("图片检查和修复完成!")

if __name__ == "__main__":
    main() 