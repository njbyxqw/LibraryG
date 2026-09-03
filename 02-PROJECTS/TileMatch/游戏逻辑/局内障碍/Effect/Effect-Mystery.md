---
title: Effect-Mystery 神秘盒
type: analysis
tags: [TileMatch, 游戏逻辑, Effect牌]
status: draft
date: 2026-07-01
cat_order: 014
---

# Effect：Mystery 神秘盒

详细说明见 [[Effect-Cirrus]]（与 Cirrus/Curtain 并列对比）。

## 快速速查

| 属性 | 值 |
|------|-----|
| EffectType | `201` |
| Priority | `10`（最高） |
| 血量 | 1 |
| HandleClick | ✅（唯一处理 EffectClick 的 Effect） |
| 点击动作 | PreCheck → ClickAnim → DestroyAnim → DestroyEffect → **HandleForwardTileClick** → ReserveBarSpace |
| 视图 | Spine "Click" + "Idle" + TileScaleAnimation(1.2x) |
| 死局提示 | ❌ |

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect-Cirrus]]
- [[Effect牌-类型全览]]
