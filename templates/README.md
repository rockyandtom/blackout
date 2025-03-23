# 游戏页面批量生成系统

这个系统允许你通过简单的JSON配置文件批量生成游戏页面，无需为每个新游戏手动编写HTML代码。

## 系统组件

- `game_template.html`: HTML模板文件，包含游戏页面的基本结构和占位符
- `games.json`: 游戏数据配置文件，包含所有游戏的信息
- `game_generator.py`: Python脚本，将JSON数据转换为HTML页面
- `game_example.json`: 示例游戏数据，可作为参考

## 如何添加新游戏

### 1. 准备游戏数据

1. 打开`templates/games.json`文件
2. 按照JSON格式添加新游戏的信息
3. 确保提供所有必要的字段和信息

### 2. 添加游戏缩略图

1. 将游戏缩略图保存到`/assets/images/games/`目录下
2. 图片命名格式建议为：`游戏名-thumbnail.jpg`
3. 在JSON中引用正确的图片路径

### 3. 运行生成脚本

```bash
cd /path/to/your/project
python templates/game_generator.py
```

脚本会自动:
1. 读取JSON数据
2. 生成HTML页面
3. 更新首页的游戏卡片

## JSON数据结构说明

```json
{
  "name": "游戏名称",                 // 游戏的显示名称
  "slug": "game-slug",               // URL友好的短名称，用于生成URL
  "description_short": "简短描述",     // 简短描述，显示在游戏卡片和页面顶部
  "description_full": "<p>...</p>",  // 完整HTML描述，支持HTML标签
  "iframe_url": "https://...",       // 游戏iframe的URL
  "thumbnail": "/path/to/image.jpg", // 缩略图路径
  "categories": [                    // 游戏分类
    {
      "name": "分类名",
      "url": "/categories/..."
    }
  ],
  "duration": "游戏时长",             // 例如 "5-10 min per match"
  "player_type": "玩家类型",          // 例如 "Single Player"
  "difficulty": "难度",              // 例如 "Easy", "Medium", "Hard"
  "how_to_play": "游戏玩法说明",
  "controls": [                      // 游戏控制按键
    {
      "key": "按键名",
      "action": "动作描述"
    }
  ],
  "features": [                      // 游戏特性列表
    "特性1",
    "特性2"
  ],
  "extra_sections": {                // 额外的自定义部分
    "section_id": {
      "title": "部分标题",
      "content": "HTML内容"
    }
  },
  "why_play": "为什么玩这个游戏",      // 简短说明为什么玩家应该尝试这个游戏
  "similar_games": [                 // 类似游戏推荐
    {
      "name": "相似游戏名",
      "slug": "similar-slug",
      "thumbnail": "/path/to/image.jpg",
      "categories": "类别1, 类别2"
    }
  ]
}
```

## 自定义模板

如果需要修改页面布局或样式:

1. 编辑`templates/game_template.html`文件
2. 使用`{{变量名}}`格式的占位符引用JSON数据
3. 运行生成脚本应用更改

## 注意事项

- 确保JSON格式正确，否则生成脚本可能会失败
- 所有HTML内容必须正确转义
- 保持缩略图尺寸一致，建议使用16:9的宽高比
- 更新模板后需要重新生成所有页面

## 将已有游戏iframe添加到系统

如果你有现成的游戏iframe网址想添加到系统:

1. 在`games.json`中添加一个新游戏条目
2. 在`iframe_url`字段中填入游戏iframe的URL
3. 填写其他必要的游戏信息
4. 准备一张适合的游戏缩略图
5. 运行生成脚本创建页面

这样就能快速将现有游戏整合到你的游戏网站中，同时保持统一的页面风格和结构。 