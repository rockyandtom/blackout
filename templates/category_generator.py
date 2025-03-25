#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import shutil
from pathlib import Path

# 获取当前脚本所在目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)  # 项目根目录

# 路径定义
JSON_PATH = os.path.join(CURRENT_DIR, "blackout_games.json")
CATEGORIES_DIR = os.path.join(ROOT_DIR, "categories")
GAMES_HTML_PATH = os.path.join(ROOT_DIR, "games.html")

# 分类模板文件路径
CATEGORY_TEMPLATE_PATH = os.path.join(CURRENT_DIR, "category_template.html")
ALL_GAMES_TEMPLATE_PATH = os.path.join(CURRENT_DIR, "all_games_template.html")

# 确保分类目录存在
os.makedirs(CATEGORIES_DIR, exist_ok=True)

def load_games():
    """从JSON文件加载游戏数据"""
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"错误: 无法加载游戏数据: {e}")
        return []

def get_category_template():
    """获取分类页面模板"""
    try:
        # 如果模板文件不存在，尝试从现有分类页面复制一个作为模板
        if not os.path.exists(CATEGORY_TEMPLATE_PATH):
            # 从现有分类页面复制一个作为模板
            sample_category_path = os.path.join(CATEGORIES_DIR, "action.html")
            if os.path.exists(sample_category_path):
                shutil.copy(sample_category_path, CATEGORY_TEMPLATE_PATH)
                print(f"已从 {sample_category_path} 创建分类模板")
            else:
                print("错误: 无法找到模板文件且无现有分类页面可复制")
                return None

        with open(CATEGORY_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"错误: 无法加载分类模板: {e}")
        return None

def get_all_games_template():
    """获取所有游戏页面模板"""
    try:
        # 如果模板文件不存在，尝试从现有games.html页面复制一个作为模板
        if not os.path.exists(ALL_GAMES_TEMPLATE_PATH):
            if os.path.exists(GAMES_HTML_PATH):
                shutil.copy(GAMES_HTML_PATH, ALL_GAMES_TEMPLATE_PATH)
                print(f"已从 {GAMES_HTML_PATH} 创建所有游戏模板")
            else:
                print("错误: 无法找到games.html模板文件")
                return None

        with open(ALL_GAMES_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"错误: 无法加载所有游戏模板: {e}")
        return None

def organize_games_by_category(games):
    """将游戏按分类组织"""
    categories = {
        "action": [],
        "adventure": [],
        "strategy": [],
        "casual": [],
        "multiplayer": []
    }
    
    for game in games:
        # 从游戏的category字段或tags字段确定分类
        game_category = game.get("category", "").lower()
        game_tags = [tag.lower() for tag in game.get("tags", [])]
        
        # 根据category字段分类
        if game_category in categories:
            categories[game_category].append(game)
        
        # 根据tags字段分类
        for tag in game_tags:
            if tag in categories and game not in categories[tag]:
                categories[tag].append(game)
    
    return categories

def generate_game_card_html(game):
    """生成游戏卡片的HTML"""
    tags_html = ""
    for tag in game.get("tags", [])[:2]:  # 最多显示两个标签
        tags_html += f'<span class="px-2 py-1 text-xs rounded-full bg-purple-900 text-purple-200 mr-2">{tag}</span>'
    
    categories_attr = " ".join(tag.lower() for tag in game.get("tags", []))
    if game.get("category"):
        categories_attr += f" {game['category'].lower()}"
    
    return f"""
    <!-- {game['title']} Game Card -->
    <div class="game-card bg-gray-800 rounded-lg overflow-hidden shadow-lg transition transform hover:-translate-y-1 hover:shadow-xl" data-category="{categories_attr}">
        <a href="{game['url']}" class="block">
            <div class="relative pb-9/16 overflow-hidden">
                <img src="{game['thumbnail']}" alt="{game['title']}" class="absolute inset-0 h-full w-full object-cover transform hover:scale-105 transition duration-300">
            </div>
            <div class="p-4">
                <h3 class="text-lg font-semibold text-white mb-1">{game['title']}</h3>
                <p class="text-gray-400 text-sm mb-2">{game['description']}</p>
                <div class="flex">
                    {tags_html}
                </div>
            </div>
        </a>
    </div>
    """

def generate_category_page(category_name, games, template):
    """生成分类页面"""
    if not template:
        return False
    
    # 将分类名称首字母大写
    category_title = category_name.capitalize() + " Games"
    
    # 生成游戏卡片HTML
    game_cards_html = ""
    for game in games:
        game_cards_html += generate_game_card_html(game)
    
    # 替换模板中的占位符
    page_content = template
    page_content = page_content.replace("<!-- PAGE_TITLE -->", category_title)
    page_content = page_content.replace("<!-- CATEGORY_DESCRIPTION -->", f"Experience the best {category_name} games online!")
    page_content = page_content.replace("<!-- GAME_CARDS -->", game_cards_html)
    
    # 使当前分类在导航菜单中高亮显示
    for cat in ["action", "adventure", "strategy", "casual", "multiplayer"]:
        if cat == category_name:
            # 高亮当前分类
            page_content = page_content.replace(
                f'href="/categories/{cat}.html" class="block px-4 py-2 text-sm text-gray-700',
                f'href="/categories/{cat}.html" class="block px-4 py-2 text-sm text-apple-blue bg-apple-gray'
            )
            page_content = page_content.replace(
                f'href="/categories/{cat}.html" class="block py-2 hover:text-apple-blue',
                f'href="/categories/{cat}.html" class="block py-2 text-apple-blue'
            )
    
    # 写入文件
    output_path = os.path.join(CATEGORIES_DIR, f"{category_name}.html")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"已生成: {output_path}")
        return True
    except Exception as e:
        print(f"错误: 无法写入分类页面 {category_name}: {e}")
        return False

def update_all_games_page(games, template):
    """更新所有游戏页面"""
    if not template:
        return False
    
    # 生成所有游戏卡片HTML
    game_cards_html = ""
    for game in games:
        game_cards_html += generate_game_card_html(game)
    
    # 替换模板中的占位符
    page_content = template
    page_content = page_content.replace("<!-- GAME_CARDS -->", game_cards_html)
    
    # 写入文件
    try:
        with open(GAMES_HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"已更新: {GAMES_HTML_PATH}")
        return True
    except Exception as e:
        print(f"错误: 无法更新所有游戏页面: {e}")
        return False

def create_category_templates_if_needed():
    """创建分类模板文件（如果不存在）"""
    # 如果当前没有模板文件，创建基本模板
    if not os.path.exists(CATEGORY_TEMPLATE_PATH):
        # 尝试从现有分类页面复制
        for category in ["action", "adventure", "strategy", "casual", "multiplayer"]:
            category_path = os.path.join(CATEGORIES_DIR, f"{category}.html")
            if os.path.exists(category_path):
                with open(category_path, 'r', encoding='utf-8') as f:
                    template = f.read()
                    
                # 替换特定内容为占位符
                template = template.replace(f'<title>{category.capitalize()} Games - GameHub</title>', '<title><!-- PAGE_TITLE --> - GameHub</title>')
                
                # 查找并替换分类描述
                import re
                desc_pattern = r'<p class="text-xl text-apple-darkgray mb-6">(.*?)</p>'
                template = re.sub(desc_pattern, '<p class="text-xl text-apple-darkgray mb-6"><!-- CATEGORY_DESCRIPTION --></p>', template)
                
                # 查找游戏卡片部分并替换
                cards_pattern = r'<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">(.*?)</div>\s*</section>'
                template = re.sub(cards_pattern, '<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5"><!-- GAME_CARDS --></div>\n</section>', template, flags=re.DOTALL)
                
                # 保存模板
                with open(CATEGORY_TEMPLATE_PATH, 'w', encoding='utf-8') as f:
                    f.write(template)
                print(f"已从 {category_path} 创建分类模板")
                break

    # 为所有游戏页面创建模板
    if not os.path.exists(ALL_GAMES_TEMPLATE_PATH) and os.path.exists(GAMES_HTML_PATH):
        with open(GAMES_HTML_PATH, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # 查找游戏卡片部分并替换
        import re
        cards_pattern = r'<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5" id="games-grid">(.*?)</div>\s*</section>'
        template = re.sub(cards_pattern, '<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5" id="games-grid"><!-- GAME_CARDS --></div>\n</section>', template, flags=re.DOTALL)
        
        # 保存模板
        with open(ALL_GAMES_TEMPLATE_PATH, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"已从 {GAMES_HTML_PATH} 创建所有游戏模板")

def main():
    """主函数"""
    print("=" * 60)
    print("游戏分类页面生成器")
    print("=" * 60)
    
    # 创建模板文件（如果需要）
    create_category_templates_if_needed()
    
    # 加载游戏数据
    games = load_games()
    if not games:
        print("错误: 无游戏数据，无法生成页面")
        return
    
    # 按分类组织游戏
    games_by_category = organize_games_by_category(games)
    
    # 获取模板
    category_template = get_category_template()
    all_games_template = get_all_games_template()
    
    if not category_template or not all_games_template:
        print("错误: 无法加载模板文件")
        return
    
    # 生成分类页面
    for category, category_games in games_by_category.items():
        if category_games:  # 只为有游戏的分类生成页面
            generate_category_page(category, category_games, category_template)
    
    # 更新所有游戏页面
    update_all_games_page(games, all_games_template)
    
    print("=" * 60)
    print("分类页面生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main() 