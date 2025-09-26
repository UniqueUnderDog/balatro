# Balatro Game Project

这是一个基于Python实现的Balatro风格卡牌游戏项目。

## 项目结构

```
├── card/
│   ├── Tarot/         # 塔罗牌相关实现
│   ├── joker/         # 小丑牌相关实现
│   └── poker/         # 扑克牌相关实现
├── utils/             # 工具函数
├── environment.py     # 游戏环境
├── player.py          # 玩家类
└── forward.py         # 游戏流程控制
```

## 功能特点

- 扑克牌池管理（无放回发牌）
- 小丑牌系统（可购买和出售）
- 塔罗牌系统（特殊效果卡牌）
- 商店系统（卡牌购买和出售）
- 玩家状态管理

## 如何运行

```bash
python environment.py
```

## 游戏机制

- 玩家可以从商店购买小丑牌和塔罗牌
- 小丑牌购买后可以出售并放回全局牌池
- 塔罗牌可以重复出现在商店中
- 系统支持向下取整计算（使用math.floor）