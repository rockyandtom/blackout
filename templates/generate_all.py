#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)  # 项目根目录

# 脚本文件路径
DOWNLOAD_SCRIPT = os.path.join(current_dir, "download_thumbnails.py")
CREATE_MISSING_SCRIPT = os.path.join(current_dir, "create_missing_images.py")
GAME_GENERATOR_SCRIPT = os.path.join(current_dir, "game_generator.py")

def ensure_directory(directory):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)

def run_script(script_path, description):
    """运行Python脚本并返回结果"""
    print(f"\n{'='*60}")
    print(f"正在{description}...")
    print(f"{'='*60}")
    
    try:
        # 使用subprocess运行脚本并捕获输出
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: 运行脚本失败: {script_path}")
        print(f"错误信息: {e.stderr}")
        return False

def main():
    """主函数"""
    print("Blackout游戏平台生成器 v1.0")
    print("="*60)
    print("该脚本将执行以下步骤:")
    print("1. 下载游戏缩略图")
    print("2. 检查和填充缺失的图片")
    print("3. 生成游戏页面")
    print("="*60)
    print("开始执行...")
    
    # 确保必要的目录存在
    ensure_directory(os.path.join(root_dir, "games"))
    ensure_directory(os.path.join(root_dir, "assets", "images", "games"))
    
    # 运行下载缩略图脚本
    if not run_script(DOWNLOAD_SCRIPT, "下载游戏缩略图"):
        print("警告: 缩略图下载可能不完整，但将继续执行...")
    
    # 运行创建缺失图片脚本
    if not run_script(CREATE_MISSING_SCRIPT, "检查和创建缺失的图片"):
        print("错误: 创建缺失图片失败")
        sys.exit(1)
    
    # 运行游戏页面生成脚本
    if not run_script(GAME_GENERATOR_SCRIPT, "生成游戏页面"):
        print("错误: 生成游戏页面失败")
        sys.exit(1)
    
    print("\n"+"="*60)
    print("所有操作已完成!")
    print("您可以在浏览器中打开index.html查看您的游戏网站")
    print("="*60)

if __name__ == "__main__":
    main() 