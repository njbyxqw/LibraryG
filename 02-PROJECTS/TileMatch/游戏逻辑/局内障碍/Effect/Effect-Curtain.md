---
title: Effect-Curtain 帷幕
type: analysis
tags: [TileMatch, 游戏逻辑, Effect牌]
status: draft
date: 2026-07-01
cat_order: 007
---

# Effect：Curtain 帷幕

详细说明见 [[Effect-Cirrus]]（与 Cirrus/Mystery 并列对比）。

## 快速速查

| 属性 | 值 |
|------|-----|
| EffectType | `50` |
| Priority | `8` |
| 血量 | 1 |
| 切换机制 | Attack(DamageSourceType=4) → 开→闭→开→闭... |
| 死局死法 | 仅打开，不销毁 |
| 视图 | Spine "up"/"down"/"down_Click"/"End" + SFX_curtain_* |
| 死局提示 | ❌ `CanJoinDeadlockHint=false` |

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect-Cirrus]]
- [[Effect牌-类型全览]]
