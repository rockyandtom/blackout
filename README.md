# Blackout 游戏平台

一个简洁美观的HTML5游戏平台网站，展示和推广各种网页游戏。网站使用现代响应式设计，提供流畅的浏览体验。

## 功能特点

- 响应式网页设计，适配不同设备屏幕尺寸
- 使用Tailwind CSS实现现代化UI界面
- 动态游戏卡片展示游戏缩略图和基本信息
- 详细的游戏页面包含游戏信息、描述和相关游戏推荐
- 简单明了的分类系统
- 黑暗主题设计，突出游戏内容

## 目录结构

```
BLACKOUT/
├── assets/                 # 静态资源
│   └── images/             # 图片资源
│       ├── games/          # 游戏缩略图
│       └── ui/             # UI图标和素材
├── games/                  # 生成的游戏页面
├── templates/              # 模板和脚本
│   ├── game_template.html  # 游戏页面模板
│   ├── blackout_games.json # 游戏数据
│   ├── game_generator.py   # 游戏页面生成脚本
│   ├── download_thumbnails.py  # 缩略图下载脚本
│   ├── create_missing_images.py # 图片检查和修复脚本 
│   └── generate_all.py     # 一键生成脚本
└── index.html              # 首页
```

## 使用方法

### 一键生成

运行以下命令，一键完成所有生成步骤：

```bash
python3 templates/generate_all.py
```

这个脚本会自动执行以下操作：
1. 下载游戏缩略图
2. 检查和填充缺失的图片
3. 生成游戏页面

### 手动步骤

如果需要单独执行某个步骤，可以运行相应的脚本：

1. 下载游戏缩略图:
```bash
python3 templates/download_thumbnails.py
```

2. 检查和填充缺失的图片:
```bash
python3 templates/create_missing_images.py
```

3. 生成游戏页面:
```bash
python3 templates/game_generator.py
```

## 添加新游戏

要添加新游戏，请按以下步骤操作：

1. 在 `templates/blackout_games.json` 文件中添加新游戏的信息
2. 在 `assets/images/games/` 目录中添加相应的游戏缩略图
3. 运行 `python3 templates/game_generator.py` 生成新的游戏页面

## 自定义

- **修改游戏数据**：编辑 `templates/blackout_games.json` 文件
- **修改游戏页面模板**：编辑 `templates/game_template.html` 文件
- **修改首页**：直接编辑 `index.html` 文件

## 需求

- Python 3.6+
- 网络连接（用于下载缩略图）
- requests 库 (`pip install requests`)

## 注意事项

- 确保所有游戏的缩略图都存在于 `assets/images/games/` 目录中
- 游戏页面会根据 `blackout_games.json` 中的数据自动生成
- 网站使用相对路径，可以直接在本地浏览器中打开 `index.html` 文件查看效果
