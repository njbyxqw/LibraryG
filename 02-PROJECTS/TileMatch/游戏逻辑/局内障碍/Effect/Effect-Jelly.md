---
title: Effect-Jelly 果冻
type: analysis
tags: [TileMatch, 游戏逻辑, Effect牌]
status: draft
date: 2026-07-01
cat_order: 013
---

# Effect：Jelly 果冻 / JellyTransparent 透明果冻

详细说明见 [[Effect-Cookie]]（与 Cookie 饼干并列对比，含完整视图层）。

## 变体速查

| 方向    | Jelly EffectType | JellyTransparent EffectType |
| ----- | ---------------- | --------------------------- |
| Up    | 180              | 170                         |
| Down  | 181              | 171                         |
| Left  | 182              | 172                         |
| Right | 183              | 173                         |

## 快速速查

| 属性 | 值 |
|------|-----|
| Priority | `7` |
| 尺寸 | 1×2 |
| 血量 | 2 |
| TakeOverDestroy | ✅ |
| 遮挡 | Jelly=✅ + OcclusionMask / JellyTransparent=❌ |
| 自毁 | CoveredCountAtMost(FullCover=true, Max=1) |
| 视图 | centerRender+otherRender | Animator "Click" | TransformFollower | SFX_jelly_* |

## 关联
- [[局内障碍知识库_MOC]]
- [[Effect-Cookie]]
- [[Effect牌-类型全览]]
