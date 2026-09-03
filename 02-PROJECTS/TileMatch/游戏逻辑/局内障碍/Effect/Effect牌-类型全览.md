---
tags: [TileMatch, 游戏逻辑, Effect牌]
type: reference
status: draft
date: 2026-07-01
cat_order: 001
---

# Effect 牌类型全览

Effect 是**挂载在 Tile 上的装饰/阻挡层**，不独立占据棋盘格子。用于遮挡棋子、扣血、改变交互行为。

## 核心属性速查

| Effect | Type | HP | 遮挡 | 尺寸 | 伤害源 | 核心机制 |
|--------|------|-----|------|------|--------|---------|
| [[Effect-Golden|Golden 金砖]] | 10 | 4 | ❌ | 1×1 | `4` (AddToBar) | 4层金砖，消除后收集计数 |
| [[Effect-Crate|Crate 木箱]] | 20 | 1 | ✅ | 1×1 | `4` (AddToBar) | 单层护盾，死局自毁 |
| [[Effect-Ice|Ice 冰块]] | 30 | 3 | ❌ | 1×1 | `4` (AddToBar) | 3层冰块，挂在Board层 |
| [[Effect-Cirrus|Cirrus 云层]] | 40 | 2 | 动态 | 2×1 | `1` (Tap) | 可见后去遮→点击送入Bar |
| [[Effect-Curtain|Curtain 帷幕]] | 50 | 1 | 切换式 | 1×1 | `4` (AddToBar) | 攻击切换开/闭状态 |
| [[Effect-Chain|Chain 锁链]] | 60 | — | ❌ | 1×1 | — | 链接攻击传递 |
| [[Effect-Grass|Grass 草丛]] | 70 | 2 | ❌ | 1×1 | `2` | 邻居清空或死局时自毁 |
| [[Effect-Stone|Stone 石板]] | 80 | 2 | ✅ | 1×1 | `8` (Match) | 石板护盾，死局自毁 |
| [[Effect-Cloud|Cloud 云朵]] | 90 | 1 | ✅ | 1×1 | `64` | 可见后自动消失 |
| [[Effect-GiftBox|GiftBox 礼盒]] | 100 | 1 | ✅ | 1×1 | `64` | 可见后自动打开消失 |
| [[Effect-Cookie|Cookie 饼干]] | 120-121 | 2 | ✅ | 2×1/1×2 | `4` (AddToBar) | 覆盖2格，全部揭开后自毁 |
| [[Effect-Jelly|Jelly 透明果冻]] | 170-173 | 2 | ❌ | 1×2 | — | 透明半覆盖，棋子消除后自毁 |
| [[Effect-Jelly|Jelly 果冻]] | 180-183 | 2 | ✅ | 1×2 | — | 不透明半覆盖，棋子消除后自毁 |
| [[Effect-Pig|Pig 小猪护盾]] | 190-192 | 1/2/3 | ✅ | 1×1 | `8` (Match) | 多层护盾+血量动画，死局自毁 |
| [[Effect-Ice2x2|Ice2x2 冰块2×2]] | 200 | 4 | ❌ | 2×2 | `4` (AddToBar) | 4层4格冰块 |
| [[Effect-Mystery|Mystery 神秘盒]] | 201 | 1 | ✅ | 1×1 | — | 点击揭开，转发点击到底层 |

## Direction 变体说明

| 变体 | Suffix | 方向 | 示例 |
|------|--------|------|------|
| Up | `_Up` | 朝上 | JellyUp = 上格遮挡 |
| Down | `_Down` | 朝下 | JellyDown = 下格遮挡 |
| Left | `_Left` | 朝左 | JellyLeft = 左格遮挡 |
| Right | `_Right` | 朝右 | JellyRight = 右格遮挡 |
| Horizontal | `_Horizontal` | 水平 | CookieHorizontal = 2×1 |
| Vertical | `_Vertical` | 垂直 | CookieVertical = 1×2 |

## DamageSourceType 含义

| 值 | 含义 | 使用 Effect |
|----|------|------------|
| `1` | Tap（点击） | Cirrus |
| `2` | — | Grass |
| `4` | AddToBar（进Bar消除） | Golden, Crate, Ice, Curtain, Cookie, Ice2x2 |
| `8` | Match（匹配消除） | Pig, Stone |
| `64` | — | Cloud, GiftBox |

## 关联
- [[局内障碍知识库_MOC]]
- [[障碍牌-类型全览]]
- [[局内障碍知识库_MOC]]
