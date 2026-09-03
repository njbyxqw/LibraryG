---
title: 设计-风车 Shuffle 单组保底-v1
type: game-logic
status: implemented-static-verified
project: TileScape
lifecycle: current
verification: implemented-compile-runtime-pending
date: 2026-08-20
tags: [TileScape, TileV2, 风车, Shuffle, 局内道具]
source: "TS dev 分支 `ShufflePropTargetFilter.cs` 的静态代码与 2026-08-20 实施记录；历史对照为 TileMatch 风车 Shuffle 需求文档"
---

# 风车 Shuffle 单组保底

## 目标

一次风车 Shuffle 最多只对一个 Bar 中未凑满的牌型做定向补齐，保证其达到一组消除所需数量；其余可移动 Tile 仍按原有随机交换处理。

该规则建立在 `66d1c3749` 引入的多类型帮助版本之上：将其「对多个未匹配牌型同时优先帮助」收敛为单一牌型。它不恢复老版本 `LastUnmatchedTile` 的“Bar 最右侧未匹配牌优先”规则。

## 生效条件与候选

1. 从 Bar 读取未匹配牌型及当前数量。
2. 忽略数量无效、找不到 Tile 配置或 `MatchCount <= 0` 的牌型。
3. 对剩余候选牌型随机洗牌；随机源沿用 `RandomService`，因此同一局随机种子下仍可复现。
4. 某牌型需要补入的数量为 `MatchCount - BarCount`。例如 MatchCount 为 3：Bar 为 `AABBCC` 时，A/B/C 各需 1 张；Bar 为 `ABCD` 时，A/B/C/D 各需 2 张。

## 单组定向补齐

按候选随机顺序逐个尝试，并且只会提交第一个能够完整补齐的牌型：

1. 目标位置必须是非高亮区、类型等于候选牌型的可 Shuffle Tile。
2. 与其交换的来源必须是高亮区、类型不同于候选牌型的可 Shuffle Tile，保证这是实际换位而不是同类交换的视觉空操作。
3. 优先选择不破坏序列约束的交换对；若无此对，沿用既有 Shuffle 的兜底选择。
4. 必须一次找齐该牌型所需的全部交换对，才整体提交；中途不足则完全丢弃本次尝试，继续尝试下一个随机候选。
5. 一旦某个牌型提交成功，停止全部后续定向帮助。

高亮区已存在同类型 Tile 不构成保护或成功条件：例如 Bar 为 `AABBCC`、高亮区已有 A，A 仍会与 B/C 同样参与候选随机；若 A 被选中，仍需找到非 A 高亮来源与非高亮 A 进行实际交换。该高亮 A 之后照常参与随机换位，避免多次使用时位置不变。

## 随机收尾与边界

- 已提交定向交换的 Tile 不再参与随机换位。
- 其余可 Shuffle Tile 全部按既有随机成对交换。
- 若没有任何候选可完整补齐，则退化为纯随机 Shuffle，不伪造保底成功。
- 随机收尾可能偶然形成额外可消组；本规则限制的是定向保证数为一个牌型，不限制随机结果。
- 本次未修改 UI、存档、配置、价格或埋点。

## 例子

| Bar | 定向结果 |
| --- | --- |
| `AABBCC` | 随机从 A/B/C 中选择一个可完整执行的类型，仅为它换入 1 张；不会同时给 A、B、C 各补 1 张。 |
| `ABCD` | 随机从可行的 A/B/C/D 中选择一个，仅为它换入 2 张；6 个高亮位置不会被用来给三个类型各补 2 张。 |
| `AABBCC` 且高亮已有 A | 该 A 不锁定。A/B/C 仍随机竞争；若选 A，必须有真实的非 A → A 交换，原高亮 A 随后仍随机移动。 |

## 代码与验证状态

- 实现：`Assets/Game/TileV2/Scripts/GameCore/Logic/GameLogic/Filter/ShufflePropTargetFilter.cs`
- 分支：`dev`，记录时 HEAD 为 `fd4ca2e4a`。
- 静态检查：`git diff --check` 通过。
- 编译：受本机 `Temp/obj/TileMatch.Logic.GameLogic/project.assets.json` 缺失阻塞，未进入 C# 编译；尚需在 Unity/完整依赖环境进行编译与局内回归。

## 历史对照

TileMatch 的旧需求文档记录：老版本以 `LastUnmatchedTile`（Bar 最右侧未匹配牌）作为唯一帮助目标；之后才提出多类型优先帮助与 AB 方案。本设计只限制后者的定向帮助数量，不恢复前者的最右侧优先。当前行为以本项目当前分支代码和本设计为准。

## 关联

- [[02-PROJECTS/TileScape/_MOC|TileScape 知识库 MOC]]
- [[02-PROJECTS/TileScape/游戏逻辑/梳理-局内四道具表现与逻辑-v1|局内四道具表现与逻辑]]
- [[02-PROJECTS/TileMatch/游戏逻辑/局内道具/风车Shuffle优化提需|历史风车 Shuffle 优化需求]]
