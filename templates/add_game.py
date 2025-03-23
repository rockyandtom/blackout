#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from pathlib import Path

def clear_screen():
    """清除终端屏幕"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_games():
    """加载现有的游戏数据"""
    json_path = "templates/games.json"
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，创建一个空列表
        return []
    except json.JSONDecodeError:
        print("错误: games.json 文件格式错误！")
        sys.exit(1)

def save_games(games):
    """保存游戏数据到JSON文件"""
    json_path = "templates/games.json"
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(games, file, ensure_ascii=False, indent=2)
    print(f"✅ 游戏数据已保存到 {json_path}")

def create_slug(name):
    """根据游戏名创建URL友好的slug"""
    # 转小写并替换空格为连字符
    slug = name.lower().replace(' ', '-')
    # 移除非字母数字连字符的字符
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    return slug

def get_input(prompt, default=None):
    """获取用户输入，支持默认值"""
    if default:
        result = input(f"{prompt} [{default}]: ")
        return result if result else default
    else:
        while True:
            result = input(f"{prompt}: ")
            if result:
                return result
            print("请输入有效内容！")

def get_multiline_input(prompt):
    """获取多行文本输入"""
    print(f"{prompt} (输入空行结束):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    return "\n".join(lines)

def get_list_input(prompt, min_items=1):
    """获取列表输入"""
    items = []
    print(f"{prompt} (输入空行结束，至少需要 {min_items} 项):")
    while True:
        item = input(f"第 {len(items)+1} 项: ")
        if not item:
            if len(items) >= min_items:
                break
            print(f"请至少输入 {min_items} 项！")
            continue
        items.append(item)
    return items

def get_categories():
    """获取游戏分类"""
    categories = []
    predefined_categories = [
        {"name": "Action", "url": "/categories/action.html"},
        {"name": "Adventure", "url": "/categories/adventure.html"},
        {"name": "Strategy", "url": "/categories/strategy.html"},
        {"name": "Puzzle", "url": "/categories/puzzle.html"},
        {"name": "Casual", "url": "/categories/casual.html"},
        {"name": "Multiplayer", "url": "/categories/multiplayer.html"},
        {"name": "Platform", "url": "/categories/platform.html"}
    ]
    
    print("\n可用分类:")
    for i, cat in enumerate(predefined_categories):
        print(f"{i+1}. {cat['name']}")
    
    print("\n选择游戏分类 (输入分类编号，多个分类用逗号分隔):")
    selection = input("选择: ")
    
    try:
        indices = [int(i.strip()) - 1 for i in selection.split(",")]
        for idx in indices:
            if 0 <= idx < len(predefined_categories):
                categories.append(predefined_categories[idx])
    except ValueError:
        print("无效的选择，将使用默认分类 (Action)")
        categories.append(predefined_categories[0])
    
    return categories

def get_controls():
    """获取游戏控制按键"""
    controls = []
    print("\n输入游戏控制按键 (输入空行结束，至少需要1项):")
    while True:
        key = input("按键 (例如 'WASD', 'Space'): ")
        if not key and len(controls) > 0:
            break
        
        if not key:
            print("请至少输入1组控制按键！")
            continue
            
        action = input(f"'{key}' 的功能: ")
        controls.append({"key": key, "action": action})
    
    return controls

def ask_yes_no(question, default="yes"):
    """询问是/否问题"""
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"无效的默认值: '{default}'")
    
    while True:
        choice = input(f"{question}{prompt}").lower()
        if choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("请回答 'yes' 或 'no' (或 'y' 或 'n')")

def add_new_game():
    """添加新游戏的主函数"""
    clear_screen()
    print("=" * 50)
    print("游戏添加向导")
    print("=" * 50)
    print("请按照提示填写游戏信息。按Ctrl+C可随时退出。\n")
    
    # 加载现有游戏
    games = load_games()
    
    # 基本信息
    name = get_input("游戏名称")
    slug = create_slug(name)
    print(f"自动生成的URL名称: {slug}")
    
    iframe_url = get_input("游戏iframe URL")
    description_short = get_input("简短描述 (显示在游戏卡片上)")
    
    # 创建一个新的游戏数据结构
    new_game = {
        "name": name,
        "slug": slug,
        "description_short": description_short,
        "iframe_url": iframe_url,
        "thumbnail": f"/assets/images/games/{slug}-thumbnail.jpg"
    }
    
    # 详细描述
    print("\n填写游戏详细描述 (支持HTML格式):")
    print("提示: 可以使用以下HTML标签: <p>, <strong>, <em>, <ul>, <li> 等")
    description_parts = []
    
    description_part = get_multiline_input("第一段详细描述")
    description_parts.append(f'<p class="mb-6 text-lg">{description_part}</p>')
    
    if ask_yes_no("添加更多段落?"):
        description_part = get_multiline_input("第二段详细描述")
        description_parts.append(f'<p class="mb-6 text-lg">{description_part}</p>')
    
    new_game["description_full"] = "".join(description_parts)
    
    # 游戏分类
    new_game["categories"] = get_categories()
    
    # 游戏时长
    duration_examples = ["5-10 min per match", "1-2 hours", "15-30 min per level"]
    new_game["duration"] = get_input("游戏时长", duration_examples[0])
    
    # 玩家类型
    player_type_examples = ["Single Player", "Multiplayer", "Co-op", "1-4 Players"]
    new_game["player_type"] = get_input("玩家类型", player_type_examples[0])
    
    # 难度
    difficulty_examples = ["Easy", "Medium", "Hard", "Easy to Hard"]
    new_game["difficulty"] = get_input("游戏难度", difficulty_examples[0])
    
    # 游戏玩法
    new_game["how_to_play"] = get_input("游戏玩法说明")
    
    # 控制按键
    new_game["controls"] = get_controls()
    
    # 游戏特性
    new_game["features"] = get_list_input("游戏特性/功能", min_items=3)
    
    # 为什么玩这个游戏
    new_game["why_play"] = get_input("为什么玩这个游戏的简短推荐语")
    
    # 额外部分
    new_game["extra_sections"] = {}
    if ask_yes_no("添加游戏技巧部分?"):
        tips_title = get_input("技巧部分标题", "Tips and Strategies")
        tips_content = f'<p class="mb-3">以下是一些帮助您的技巧:</p><ul class="list-disc pl-6 mb-6 space-y-1">'
        tips = get_list_input("游戏技巧", min_items=3)
        for tip in tips:
            tips_content += f"<li>{tip}</li>"
        tips_content += "</ul>"
        
        new_game["extra_sections"]["tips"] = {
            "title": tips_title,
            "content": tips_content
        }
    
    # 相似游戏
    new_game["similar_games"] = []
    if ask_yes_no("添加相似游戏推荐?"):
        # 使用现有游戏作为推荐
        if len(games) > 0 and ask_yes_no("从现有游戏中选择相似游戏?"):
            print("\n现有游戏:")
            for i, game in enumerate(games):
                print(f"{i+1}. {game['name']}")
            
            print("\n选择相似游戏 (输入游戏编号，多个游戏用逗号分隔):")
            selection = input("选择: ")
            
            try:
                indices = [int(i.strip()) - 1 for i in selection.split(",")]
                for idx in indices:
                    if 0 <= idx < len(games):
                        similar_game = {
                            "name": games[idx]["name"],
                            "slug": games[idx]["slug"],
                            "thumbnail": games[idx]["thumbnail"],
                            "categories": ", ".join([cat["name"] for cat in games[idx]["categories"][:2]])
                        }
                        new_game["similar_games"].append(similar_game)
            except ValueError:
                print("无效的选择，将不添加相似游戏")
        else:
            # 手动添加相似游戏
            print("\n手动添加相似游戏:")
            for i in range(3):
                if i > 0 and not ask_yes_no(f"添加第 {i+1} 个相似游戏?"):
                    break
                
                similar_name = get_input(f"相似游戏 {i+1} 名称")
                similar_slug = create_slug(similar_name)
                similar_thumbnail = f"/assets/images/games/{similar_slug}-thumbnail.jpg"
                similar_categories = get_input(f"相似游戏 {i+1} 分类 (用逗号分隔)")
                
                similar_game = {
                    "name": similar_name,
                    "slug": similar_slug,
                    "thumbnail": similar_thumbnail,
                    "categories": similar_categories
                }
                new_game["similar_games"].append(similar_game)
    
    # 确认并保存
    clear_screen()
    print("=" * 50)
    print(f"游戏信息预览: {name}")
    print("=" * 50)
    print(f"名称: {name}")
    print(f"URL名称: {slug}")
    print(f"简短描述: {description_short}")
    print(f"iframe URL: {iframe_url}")
    print(f"缩略图路径: {new_game['thumbnail']}")
    print(f"分类: {', '.join([cat['name'] for cat in new_game['categories']])}")
    print(f"游戏时长: {new_game['duration']}")
    print(f"玩家类型: {new_game['player_type']}")
    print(f"难度: {new_game['difficulty']}")
    print(f"特性数量: {len(new_game['features'])}")
    print(f"控制按键数量: {len(new_game['controls'])}")
    print(f"相似游戏数量: {len(new_game['similar_games'])}")
    print("=" * 50)
    
    if ask_yes_no("是否保存这个游戏?"):
        # 添加到游戏列表
        games.append(new_game)
        save_games(games)
        
        # 提醒上传缩略图
        print(f"\n⚠️ 请记得上传游戏缩略图到: {new_game['thumbnail']}")
        print("建议图片尺寸: 16:9 比例，例如 1280x720 像素")
        
        # 询问是否运行生成脚本
        if ask_yes_no("现在运行生成脚本创建游戏页面?"):
            try:
                os.system("python templates/game_generator.py")
                print("✅ 游戏页面生成完成！")
            except Exception as e:
                print(f"❌ 生成脚本运行失败: {e}")
                print("请手动运行: python templates/game_generator.py")
        else:
            print("\n稍后可以手动运行生成脚本: python templates/game_generator.py")
    else:
        print("已取消添加游戏。")

if __name__ == "__main__":
    try:
        add_new_game()
    except KeyboardInterrupt:
        print("\n\n操作已取消。")
        sys.exit(0) 