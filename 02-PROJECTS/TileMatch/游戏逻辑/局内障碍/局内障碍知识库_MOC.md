---
title: 局内障碍知识库_MOC
date: 2026-06-25
type: index
status: finalized
tags: [TileMatch, 游戏逻辑, 障碍系统]
cat_order: 001
---

# 局内障碍知识库 MOC

> 障碍系统（障碍Tile + Effect牌）的知识库总入口

---

## 一、障碍系统概述

TileMatch 的障碍系统分为两大类：

### 1.1 障碍Tile（障碍牌）

**定义**: TileType >= 5000 的特殊 Tile，独立占格子

**特点**:
- 有独立生命值（Life）
- 需要消除周围牌或直接使用道具来破坏
- 破坏后占用格子释放

**类型**:
| TileType | 名称 | 特点 |
|----------|------|------|
| 5110 | Flip | 翻转牌（序列容器） |
| 5140 | CardBox | 卡盒（序列容器） |
| 5130-5131 | SuitCase | 手提箱（序列容器） |
| 5010 | MagicBox | 魔法盒 |
| 5030-5033 | ShellBox | 贝壳盒 |
| 5150 | JokerFlip | 百变牌 |
| 5160 | Thief | 小偷 |

### 1.2 Effect 牌

**定义**: 挂载在 Tile/Board 上的装饰层，不占格子

**特点**:
- 不影响棋盘占用
- 通过 ECA（Event-Condition-Action）引擎驱动行为
- 可视化效果为主，部分有游戏逻辑影响

**类型**:
| EffectType | 名称 | HP | 遮挡 | 尺寸 | 核心机制 |
|------------|------|-----|------|------|---------|
| 10 | Golden 金砖 | 4 | ❌ | 1×1 | 4层金砖，消除后收集计数 |
| 20 | Crate 木箱 | 1 | ✅ | 1×1 | 单层护盾，死局自毁 |
| 30 | Ice 冰块 | 3 | ❌ | 1×1 | 3层冰块，挂在Board层 |
| 40 | Cirrus 云层 | 2 | 动态 | 2×1 | 可见后去遮→点击送入Bar |
| 50 | Curtain 帷幕 | 1 | 切换式 | 1×1 | 攻击切换开/闭状态 |
| 60 | Chain 铁链 | — | ❌ | 1×1 | 链接攻击传递 |
| 70 | Grass 草丛 | 2 | ❌ | 1×1 | 邻居清空或死局时自毁 |
| 80 | Stone 石板 | 2 | ✅ | 1×1 | 石板护盾，死局自毁 |
| 90 | Cloud 云朵 | 1 | ✅ | 1×1 | 可见后自动消失 |
| 100 | GiftBox 礼盒 | 1 | ✅ | 1×1 | 可见后自动打开消失 |
| 120-121 | Cookie 饼干 | 2 | ✅ | 2×1/1×2 | 覆盖2格，全部揭开后自毁 |
| 170-173 | Jelly 透明果冻 | 2 | ❌ | 1×2 | 透明半覆盖，棋子消除后自毁 |
| 180-183 | Jelly 果冻 | 2 | ✅ | 1×2 | 不透明半覆盖，棋子消除后自毁 |
| 190-192 | Pig 小猪护盾 | 1/2/3 | ✅ | 1×1 | 多层护盾+血量动画，死局自毁 |
| 200 | Ice2x2 冰块2×2 | 4 | ❌ | 2×2 | 4层4格冰块 |
| 201 | Mystery 神秘盒 | 1 | ✅ | 1×1 | 点击揭开，转发点击到底层 |

> 完整属性对比详见 [[Effect牌-类型全览]]

---

## 二、文档索引

### 2.1 障碍Tile 文档

- [[障碍牌-类型全览|障碍牌-类型全览]] — 全23种障碍牌分类速查（核心入口）
- [[障碍牌-Rocket|障碍牌-Rocket]] — 火箭牌：点击进Bar链式爆炸（5条ECA）
- [[障碍牌-Flip|障碍牌-Flip]] — 翻转牌：Rotate循环左移（6条ECA + blockerdda变更）
- [[障碍牌-JokerFlip|障碍牌-JokerFlip]] — 百变翻转：含Joker序列（花色去重移除）
- [[障碍牌-Switch|障碍牌-Switch]] — 开关牌：ActiveIndex切换（10条ECA + Activation DDA）
- [[障碍牌-CardBox|障碍牌-CardBox]] — 卡盒：6血StayAlive + 两步开盒（8条ECA）
- [[障碍牌-SlotMachine|障碍牌-SlotMachine]] — 老虎机：Shuffle摇牌（6条ECA + TailVisibility）
- [[障碍牌-SuitCase|障碍牌-SuitCase]] — 行李箱：脱盖3张全暴（4条ECA + Activation DDA）
- [[障碍牌-ShellBox|障碍牌-ShellBox]] — 贝壳/魔法盒：EjectSequence弹出 + PreRegulate预调控（4条ECA）
- [[障碍牌-Clock|障碍牌-Clock]] — 时钟：AddToBar攻击扣血（4条ECA）
- [[障碍牌-Volcano|障碍牌-Volcano]] — 火山：死亡PrepareAttack连锁喷发（4条ECA）
- [[障碍牌-CandyBottle|障碍牌-CandyBottle]] — 糖果瓶：低血SelectAndTransformTiles转化（5条ECA）
- [[障碍牌-LightBulb|障碍牌-LightBulb]] — 灯泡：Batch批次共享血量（8条ECA）
- [[障碍牌-Thief|障碍牌-Thief]] — 小偷：BeforeBarMatch自动弹出 + PreRegulate预调控（6条ECA）
- [[障碍牌-Butterfly|障碍牌-Butterfly]] — 蝴蝶：点击自毁 + 生成新蝴蝶到弃牌区（2条ECA）
- [[障碍牌-SodaBox|障碍牌-SodaBox]] — 苏打盒：3×2大型障碍（4条ECA）
- [[障碍牌-TrafficLights|障碍牌-TrafficLights]] — 红绿灯：弃牌区联动保底（5条ECA）
- [[障碍牌-CandyCube系列|障碍牌-CandyCube系列]] — 糖果方块（收集型，可见即收集）
- [[障碍牌-Ore系列|障碍牌-Ore系列]] — 矿石+镐子（ProjectileHit投掷体系）
- [[报告-blockerdda分支调控逻辑变更排查|blockerdda分支调控变更排查]] — tile/tile_blockerdda分支完整变更报告
- [[分析-障碍Tile生成与序列逻辑-v1|障碍Tile生成与序列逻辑]] — 生成规则与序列容器逻辑

### 2.2 Effect 牌文档

- [[Effect牌-类型全览|Effect牌-类型全览]] — 所有 Effect 类型的完整清单（核心入口）
- [[Effect-Golden|Effect-Golden]] — 金砖（4层，消除后收集）
- [[Effect-Crate|Effect-Crate]] — 木箱（单层护盾，死局自毁）
- [[Effect-Ice|Effect-Ice]] — 冰块（3层，含 Ice2x2 2×2变体）
- [[Effect-Ice2x2|Effect-Ice2x2]] — 冰块2×2（4层4格）
- [[Effect-Cirrus|Effect-Cirrus]] — 云层（点击交互）
- [[Effect-Curtain|Effect-Curtain]] — 帷幕（状态切换）
- [[Effect-Chain|Effect-Chain]] — 铁链（攻击传递）
- [[Effect-Grass|Effect-Grass]] — 草丛（邻居清空自毁）
- [[Effect-Stone|Effect-Stone]] — 石板（匹配消除护盾）
- [[Effect-Cloud|Effect-Cloud]] — 云朵（可见后消失）
- [[Effect-GiftBox|Effect-GiftBox]] — 礼盒（可见后打开）
- [[Effect-Cookie|Effect-Cookie]] — 饼干（2格覆盖）
- [[Effect-Jelly|Effect-Jelly]] — 果冻（透明/不透明半覆盖）
- [[Effect-Pig|Effect-Pig]] — 小猪护盾（多层血量动画）
- [[Effect-Mystery|Effect-Mystery]] — 神秘盒（点击揭开）

### 2.3 ECA 引擎文档

- ECA 行为引擎框架（Event-Condition-Action） — 详见各 Effect 文档中的 ECA 规则章节
- `游戏逻辑/Effect/` 目录下的 ECA 相关文档

---

## 三、核心概念

### 3.1 ECA 引擎

**Event（事件）**: 触发条件（如 `TileMatched`、`RocketAttack`）

**Condition（条件）**: 事件触发后的判断（如 `IceCount > 3`）

**Action（行为）**: 条件满足后执行的操作（如 `SpreadIce`、`RemoveIce`）

### 3.2 序列容器

**定义**: 需要多次点击才能完全暴露子牌的障碍Tile

**类型**:
- **A 类**（有去重+保护）: ~~Flip、CardBox、SuitCase~~ → **blockerdda 分支后仅 Flip 保留去重**
- **B 类**（无约束）: MagicBox、ShellBox、JokerFlip、Thief、CardBox、SuitCase

> ⚠️ blockerdda 分支变更：CardBox/SuitCase/JokerFlip 的花色去重和 DDA 保护均已移除，仅 Flip 保留 Prefer 级去重。详见 [[报告-blockerdda分支调控逻辑变更排查]]

**关键行为**:
- 序列子牌动态追加到手牌区
- 共享容器 Position
- SequenceSource 指向父级索引

---

## 四、常见问题

### 4.1 障碍Tile 和 Effect 牌的区别？

| 维度 | 障碍Tile | Effect 牌 |
|------|----------|-----------|
| 占用格子 | ✅ 是 | ❌ 否 |
| 独立生命值 | ✅ 是 | ⚠️ 取决于类型 |
| 可视化 | 占用格子的模型 | 装饰层特效 |
| 交互方式 | 消除周围牌/使用道具 | ECA 引擎驱动 |

### 4.2 如何新增障碍Tile？

1. 在 `TileType` 枚举中定义新类型（>= 5000）
2. 创建对应的 TileConfig JSON（配置 Life/Behavior）
3. 实现对应的行为逻辑（如有特殊行为）
4. 更新文档（`障碍Tile生成与序列逻辑梳理.md`）

### 4.3 如何新增 Effect 牌？

1. 在 `EffectType` 枚举中定义新类型
2. 创建对应的 ECA 配置文件
3. 实现 ECA Action（如有自定义行为）
4. 更新文档（`Effect牌-类型全览.md`）

---

## 关联

- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]] — 返回项目总入口
- [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑分析]] — 高层综述（障碍系统章节）
- [[分析-死局逻辑与改进方案-v1|死局逻辑与改进方案]] — 相关：障碍Tile 对死局的影响

---

## 变更记录

- 2026-06-25: 初始创建
- 2026-07-03: 恢复文件内容（从 daily notes 重建）
