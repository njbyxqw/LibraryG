---
title: Tile 超彩 匹配充能框架设计
date: 2026-10-08
type: design
status: draft
tags: [TileMatch, TileV2, 局内道具, Tile超彩, 充能机制, 框架设计]
---

# Tile 超彩 匹配充能框架设计

> 需求：每完成 1 次成功匹配消除获得 1 点充能，累计 6 点触发效果；充能状态机参考染色炸弹；**具体效果待定**，本期只冻结转框架与接线。
>
> 代码事实来源：`/Users/dean/Downloads/meatloaf_client/client`，分支 `tile/tile_dyeingbomb`。当前工作区 `TileScape` 未包含染色炸弹模块，所有行号均指向上述仓库，落地前需在目标分支复查。

## 结论摘要

1. 超彩可以复用的不是染色炸弹的「效果规则」，而是它的**五段职责骨架**：能量累积 → 处理锁 → 目标决策 → Logic Action → ViewAction → 完成回调解锁。
2. 与染色炸弹最大的结构差异：**染色炸弹的充能在 View 层产生**（能量牌收集动画播完发布事件），超彩的充能必须**在 Logic 层的匹配结算点产生**。
3. 由此引出框架的第一个硬约束：匹配结算是 Logic 内部的同步流程，**触发不能在充能点原地执行**，必须「充能点只做标记，触发在安全点 flush」。
4. 效果未定 → 用 **Effect 插槽（`ISuperColorEffect`）+ Noop 默认实现**，让 `0→6→触发→完成回调` 全链路先跑通，效果确定后只新增实现类，不动状态机与接线。
5. 阶段一必须先做的一件事：在当前目标分支定位「成功匹配消除一次」的**唯一结算入口**并验证计数口径。这一项定不下来，后面所有接线都是建在沙上。

## 一、需求整理

### 1.1 已冻结（本期框架按这些实现）

| 项目 | 规则 | 验收口径 |
|---|---|---|
| 充能来源 | 每完成 1 次成功匹配消除结算，+1 充能 | 一次匹配结算恰好 +1；仅选牌、移动、道具展示不充能 |
| 充能粒度 | 一次结算内消除的多张 Tile 只计 1 次 | 三连消除 = +1，不是 +3 |
| 触发门槛 | 6 | 第 6 次结算后触发 1 次；前 5 次不触发 |
| 机制骨架 | 参考染色炸弹的能量累积 / 处理锁 / Action / ViewAction / 完成回调链路 | 触发期间不重入；表现完成后可继续结算与充能 |
| 状态归属 | 门槛与效果参数属**配置**（只读）；本局能量与处理锁属**运行时**（仅超彩系统写）；默认跨局不持久化 | 重开/退出关卡不继承本局能量 |
| 效果 | 暂定，本期不实现效果规则 | 只保留 EffectSpec 插槽 |

### 1.2 待决（直接影响框架接口，需在阶段二前拍板）

| 待决项 | 选项 | 未定时的框架处置 |
|---|---|---|
| 触发后能量 | A 清零 / B 扣 6 并结转溢出 / C 满能停留等待主动释放 | 状态机把扣除动作收敛到 `ConsumeCharge()` 单一方法，策略可换 |
| 触发时机 | A 当次结算完全结束后立即 / B 安全帧（tick）延迟 / C 玩家主动点击 | 框架默认 B，A/C 均为插槽替换（见 §6） |
| 效果规格 | 目标范围、改什么状态、对 Bar/OverBar/障碍/Effect 的合法性、无目标时的降级 | 用 `NoopEffect` 占位，链路可跑通 |
| 门槛配置来源 | 固定 6 / 关卡配置 / 活动 / AB | 先单一配置字段，不预建 AB 体系 |
| 前置门槛 | 是否需要「解锁条件」（染色炸弹有胜场与开关门槛） | 先不做，但保留 `IsEnabled` 位 |
| 充能可视化 | 是否显示能量条、满能提示、飘字、音效 | 效果确定后与 ViewAction 一并设计 |
| 统计 | 充能 / 满能 / 触发 / 命中 / 中断事件的字段契约 | 效果与运营目标确认后补 |

## 二、与染色炸弹的对位

| 环节 | 染色炸弹现状（分支实查） | 超彩的差异 | 处置 |
|---|---|---|---|
| 充能来源 | 能量牌点击 → `LevelCollect` 收集动画播完 → `DomainEventBus` 发 `DyeingBombEnergyCollected` → `AddEnergy()`。入口在 **View 层** | 无能量牌、无飞行收集动画；充能来自匹配结算，入口在 **Logic 层** | 必须换入口，不复用收集链路 |
| 触发时机 | 由 View 回调驱动（`TileMatchGameLogic.Event.cs:144`），此时不在匹配流程内，天然安全 | 充能点位于匹配结算流程内部（`BarActions.cs:271-355`），同步触发会重入 | 引入「标记 + 安全点 flush」 |
| 目标选择 | `CustomTargetFilterType.DyeingBomb` → `DyeingBombTargetFilter` | 抽取方式一致 | 复用 `TargetFilter` 抽象，新增一个注册项 |
| 逻辑改写 | `TileService.ModifyTile(target, TileType.DyedSuit)` 硬编码 1002 | 效果未定，不能预设改哪种 TileType | 走 Effect 插槽，禁止硬编码 |
| 表现 | `DyeingBombViewAction` 换 Icon + 全屏 `Dyeing_card` 特效 | 未知 | 只定骨架与完成契约，资源后置 |
| 完成回调解锁 | `DyeingBombAnimationFinished` → `OnDyeingComplete()` | 机制相同 | 复用该契约模式 |
| 开关 | `CustomData.IsCanShowDyeingBomb` + Record flag bit 5 + 活动开关 + GM | 需要新的开关位 | 新增 flag bit 6 |
| 计数一致性 | **View 与 Logic 各持一份计数**：`DyeingBombCollectView._collectedEnergy` 与 `DyeingBombSystem._currentEnergy` 独立累加，仅触发时 Logic 扣减、View 满值清零 | 容易长期偏离 | 超彩采用**单一数据源**：Logic 持有权威能量，View 只读显示 |
| 表现层目录 | `View/GameView/...` 与 `View/Headless/...` 双份 | 同 | 新增文件必须双份同步 |

### 不要照搬的已知缺陷

| 位置 | 问题 | 超彩的要求 |
|---|---|---|
| `DyeingBombSystem.cs:60-63` | `Board == null` 时提前 return，`_isDyeing` 已置 true 却永不复位 → **永久锁死** | 任何提前返回分支都必须复位处理锁 |
| `DyeingBombSystem.cs:43` + `:69/:91` | 失败路径 `DeductEnergy()` 被调用两次 → **能量双扣** | 扣除只发生在一个地方（成功进入触发流程后） |
| `DyeingBombCollectView.cs:101` | View 自行累加计数，与 Logic 可能不一致 | Logic 为唯一写者 |

## 三、框架分层

### 3.1 流程主线

```text
成功匹配消除结算（唯一入口，阶段一确认）
  → SuperColorSystem.AddCharge(1)          【只记账 + 只标记，不触发】
  → 安全点 FlushPendingTrigger()            【tick / 结算末尾】
  → 达 6 点 → ConsumeCharge() + 上处理锁
  → ISuperColorEffect.ResolveTargets()      【效果插槽，默认 Noop】
  → ISuperColorEffect.Apply()               【统一走既有 Service 改逻辑状态】
  → ActionResult(ActionType.SuperColor, SuperColorActionData)
  → SuperColorActionInvoker
  → SuperColorViewAction（表现，播完回调）
  → ToLogicEventType.SuperColorFinished
  → SuperColorSystem.OnTriggerComplete()    【解锁 + 再 flush，处理触发期间累积的能量】
```

### 3.2 职责边界

| 层 | 拥有什么 | 明确不做什么 |
|---|---|---|
| Logic / SuperColorSystem | 本局能量、门槛判定、处理锁、触发请求 | 不播表现、不选具体 TileType、不碰 View |
| Logic / ISuperColorEffect | 效果的目标规则与逻辑状态变更 | 不播表现、不持运行时状态 |
| Logic / TargetFilter | 从各牌池选目标 | 不改状态 |
| Application / ActionInvoker | 把 ActionResult 路由到 View | 不改逻辑状态 |
| View / SuperColorViewAction | 播放表现，报告完成/失败 | 不写逻辑数据、不做计数 |

## 四、新增文件清单

所有枚举与字典注册均为 **add-only**，不改既有语义。

| 层 | 文件 | 动作 | 参考位置 |
|---|---|---|---|
| Logic | `Logic/GameLogic/Module/SuperColor/SuperColorSystem.cs` | 新增：充能状态机 | `Module/DyeingBomb/DyeingBombSystem.cs` |
| Logic | `Logic/GameLogic/Module/SuperColor/SuperColorConfig.cs` | 新增：`MaxCharge=6` 等参数（只读） | `DyeingBombConfig.cs` |
| Logic | `Logic/GameLogic/Module/SuperColor/SuperColorActionData.cs` | 新增：Logic→View 载荷 | `DyeingBombActionData.cs` |
| Logic | `Logic/GameLogic/Module/SuperColor/ISuperColorEffect.cs` | 新增：效果插槽 + `NoopSuperColorEffect` | 无 |
| Logic | `Logic/GameLogic/Filter/SuperColorTargetFilter.cs` | 效果确定后新增 | `Filter/DyeingBombTargetFilter.cs` |
| 接线 | `Logic/GameLogic/TileMatchGameContext.cs` | 加 `SetSuperColorSystem` / `TryGetSuperColorSystem` | `:175` `:181` |
| 接线 | `Logic/GameLogic/TileMatchGameLogic.cs` | 加 `InitSuperColorSystem()` 并在初始化链调用 | `:140-143` |
| 接线 | `Logic/GameLogic/TileMatchGameLogic.Event.cs` | 注册/注销充能事件与完成事件；`Handle` 增加分支 | `:62-66` `:84-88` `:144-153` |
| 接线 | `Logic/GameLogic/Services/TileTargetSelectService.cs` | filter 字典加一项 | `:15-27` |
| 枚举 | `Config/Behaviours/Action/ActionType.cs` | `+SuperColor` | `:41` |
| 枚举 | `Logic/Interface/LogicEventType.cs` | `+SuperColorFinished`（必需）、`+SuperColorChargeChanged`（表现需要时） | `:36-37` |
| 枚举 | `Logic/GameLogic/Filter/ITargetFilter.cs` | `+SuperColor` | `:21` |
| 枚举 | `View/Interface/ICustomViewActionController.cs` | `+SuperColor` | `:47` |
| Application | `Application/ActionInvoker/Implementation/SpecialActionInvoker.cs` | `+SuperColorActionInvoker`，标 `[Preserve]` | `:327-356` |
| View | `View/GameView/Views/ViewActions/SuperColor/SuperColorViewAction.cs` + `Controller.cs` | 新增 | `Views/ViewActions/DyeingBomb/` |
| View | `View/Headless/Views/ViewActions/SuperColor/…` | 同上一份（双份同步） | 同上 |
| View | `View/GameView/TileMatchViewController.ViewActions.cs` | 字典加一项 | `:36-70` |
| View | `View/Headless/TileMatchViewController.ViewActions.cs` | 同上一份 | 同上 |
| View | 充能槽 HUD 组件（命名待定） | 新增，见 §8 | — |
| Config | `Config/Game/CustomData.cs`、`Config/Record/TileMatchGameRecord*.cs` | 开关位（bit 6） | `:222-227` |

> ActionInvoker 是反射自动注册（`TileMatchApplication.ActionInvoker.cs:24-46` 扫描 `BaseActionInvoker` 子类），只需新建类 + `[Preserve]`，无需手工登记；但 Filter 与 ViewActionController 都是**显式字典**，必须手工加项，容易漏。

## 五、核心接口契约

```csharp
// Logic/GameLogic/Module/SuperColor/SuperColorSystem.cs
public class SuperColorSystem
{
    private TileMatchGameContext _ctx;
    private int  _charge;          // 唯一权威能量
    private bool _isProcessing;    // 处理锁
    private bool _pendingTrigger;  // 充能点只置位，不触发

    internal void SetContext(TileMatchGameContext ctx) => _ctx = ctx;

    /// <summary>充能点调用。只记账 + 置标记 + 通知表现，绝不在此触发。</summary>
    internal void AddCharge(int count = 1)
    {
        if (_ctx == null || !IsEnabled) return;
        if (count <= 0) return;

        _charge += count;
        if (_charge > MaxCharge) _charge = MaxCharge;  // 上限策略见待决项
        _pendingTrigger = true;

        _ctx.EventDispatchService.PublishChargeChanged(_charge, MaxCharge); // 表现用
    }

    /// <summary>安全点调用（tick 或结算末尾）。所有触发入口都收敛到这里。</summary>
    internal void FlushPendingTrigger()
    {
        if (_isProcessing || !_pendingTrigger) return;
        if (_charge < MaxCharge) return;

        _pendingTrigger = false;
        ConsumeCharge();          // 唯一扣减点
        _isProcessing = true;

        if (!TryDispatchEffect()) // 无目标 / 无效果 → 降级
        {
            _isProcessing = false;
            TryDispatchNextAfterFailure();   // 防御：把扣掉的能量按策略回滚或按规则丢弃
        }
    }

    /// <summary>View 表现完成回调。必须"一次且仅一次"。</summary>
    internal void OnTriggerComplete()
    {
        _isProcessing = false;
        FlushPendingTrigger();    // 处理期间累积的能量在此结算，对齐 OnDyeingComplete
    }

    /// <summary>关卡开始 / 重开时复位。</summary>
    internal void OnLevelStart() { _charge = 0; _isProcessing = false; _pendingTrigger = false; }

    private void ConsumeCharge()
    {
        // 待决项在此落地：
        // A 清零：_charge = 0;
        // B 结转：_charge -= MaxCharge; if (_charge < 0) _charge = 0;
        _charge -= MaxCharge;
        if (_charge < 0) _charge = 0;
    }
}
```

```csharp
// Logic/GameLogic/Module/SuperColor/ISuperColorEffect.cs
public interface ISuperColorEffect
{
    /// 效果的目标规则：拿到可用牌池，返回目标集合（为空表示降级）
    List<Tile> ResolveTargets(TileMatchGameContext ctx);

    /// 逻辑状态变更：必须经由既有 Service（TileService / MatchTileService 等），禁止直改数据
    void Apply(TileMatchGameContext ctx, List<Tile> targets, List<ActionResult> outputs);

    /// 交给 View 的载荷
    object BuildActionData(List<Tile> targets);
}

/// 效果未定期间的默认实现：不选目标、不改状态，仅让全链路可跑通（表现播占位特效）
public sealed class NoopSuperColorEffect : ISuperColorEffect { /* … */ }
```

设计要点：`ConsumeCharge()` 是唯一扣减点（修掉染色炸弹的双扣）；`TryDispatchEffect()` 的失败分支必须先解锁再决定能量去留（修掉永久锁死）。

## 六、充能入口与安全点

### 6.1 充能入口

阶段一需确认的候选位置（分支实查证据）：

| 候选 | 位置 | 评价 |
|---|---|---|
| ① `AfterBarMatch` 广播 | `BarActions.cs:355`，是匹配结算流程的末尾广播 | **推荐**。一次 match 恰好一次；`TileMatchGameLogic.Event.cs:66` 已有 `BarMatched` 订阅位，扩展成本最低；不改 `BarActions` 主流程 |
| ② `BarMatch` ActionResult 入队处 | `BarActions.cs:327` | 语义最明确，但需改匹配主流程 |
| ③ `TileDestroyed` / `AfterTileDestroyed` | 牌生命周期 | **不要用**。一次匹配会触发多张牌销毁 → 多充能；被道具/攻击销毁的牌也会误充能 |

落点建议：在 `TileMatchGameLogic.Event.cs` 增加 `EventType.AfterBarMatch` 的注册与 `AddCharge(1)` 分支，与现有 `BarMatched`、`AddingToBarByClick` 订阅并列。

### 6.2 安全点（防重入的关键）

`AfterBarMatch` 是**在匹配结算流程内部同步发布**的，所以 `AddCharge` 只能标记。触发时机三选一：

| 方案 | 实现位置 | 优点 | 代价 |
|---|---|---|---|
| A. Logic tick flush | `GameTimerTick`（`Event.cs:48` 已注册）里调 `FlushPendingTrigger()` | 改动最小、天然防重入、可覆盖任何来源的充能 | 触发滞后 ≤1 帧 |
| B. 结算末尾 flush | `AfterBarMatch` 分支末尾直接 flush | 当次结算后立即触发，体感最好 | 需证明此处已脱离匹配嵌套；道具/连锁路径要单独验证 |
| C. 玩家主动释放 | HUD 按钮 → `ToLogicEventType.SuperColorReleaseRequest` | 交互可控 | 需产品确认 |

**框架默认取 A**：先用 tick flush 把链路跑通，产品若要求「当次结算后立即触发」，再切换到 B 并补连锁/道具路径的验证。

## 七、效果插槽

效果待定是本期的核心不确定性，框架用三个层次隔离它：

| 层次 | 效果确定后需要改什么 | 不需要改什么 |
|---|---|---|
| 目标选择 | 新增 `SuperColorTargetFilter` 并注册（或直接在 Effect 内选牌） | 状态机、接线、View 骨架 |
| 逻辑变更 | 新增 `ISuperColorEffect` 实现类的 `Apply` | 同上 |
| 表现 | 替换 `SuperColorViewAction` 内的特效与时间轴；新增资源 | 完成回调契约 |

推荐的三种预置形态（供效果评审时对照）：

| 效果形态 | 复用点 | 注意 |
|---|---|---|
| 选牌改造（类似染色炸弹） | `SuperColorTargetFilter` + `TileService.ModifyTile` | 目标合法性规则需单独评审（障碍、Bar、OverBar、不可见） |
| 范围攻击 / 消除 | `EmitEvent` + `Attack`（`ActionType.PrepareAttack/HandleAttack`） | 需处理目标为空与连锁 |
| 生成道具 / 牌 | `ActionType.CreateTile` | 需处理 Bar/棋盘满位 |

三条都必须覆盖：**无目标、目标不足、触发中再次结算、关卡结束中断**。

## 八、View 层方案

### 8.1 充能槽显示：不要复用 CollectView

染色炸弹的 `DyeingBombCollectView` 属于 `CollectView` 体系，靠 `LevelCollect` 动作 + `CollectKey` 驱动飞行动画；超彩没有能量牌，也就没有 `LevelCollect` 事件源。沿用会导致「有收集器但永远不被驱动」的空壳结构。

推荐：新增独立 HUD 组件，订阅新增的 `EventType.SuperColorChargeChanged`（Logic → View 单向广播）做增量刷新与满能态切换。数据来源是 Logic 的权威能量，HUD 只读。

### 8.2 触发表现与完成契约

- `SuperColorViewAction` 消费 `SuperColorActionData`，播放效果后回调。
- 完成回调必须满足：正常完成、无目标降级、关卡退出/中断 **四种路径都能解锁**。染色炸弹的做法是在 Logic 侧 `OnDyeingComplete()` 统一解锁，View 侧用 `try/finally` 保证资源回收——沿用它，但把「无目标提前返回」也纳入解锁路径。
- 中断时不重复触发（`_isProcessing` 已挡住），退出时 `OnLevelStart()` 复位幂等。

## 九、开关与灰度

参考染色炸弹的四段式：

| 环节 | 参考实现 | 超彩需新增 |
|---|---|---|
| 本局能力位 | `CustomData.IsCanShowDyeingBomb` | `IsCanShowSuperColor` |
| 记录持久化 | `TileMatchGameRecordBinaryPersister.cs:222-227`，flags bit 0-5 已占用 | 使用 **bit 6** |
| 入口开关 | `TileMatchGame.SetPendingDyeingBombEnabled` | 同名 pending 开关 |
| 活动/运营开关 | `ActRocketAndColorData.GetDyeingBombIsOpen` | 按需，本期可不做 |
| GM 调试 | `Module/GM/Scripts/Category/GmCommon.cs` 的 `SetDyeingBombMaxEnergy` / `SetDyeingBombDyeCount` | 加 `SetSuperColorMaxCharge`（便于验证 1→6） |
| 配置缺失 | — | 缺配置时 `IsEnabled=false`，功能安全关闭 |

> 注意 `DyeingBombConfig` 用的是 `public static int MaxEnergy`（GM 直接改静态字段）。多关卡/热重载场景下静态字段有污染风险，超彩建议改为实例配置或只读配置读取，GM 仅作用于当前局。

## 十、实现阶段

| 阶段 | 目标 | 产出 | 可回滚点 |
|---|---|---|---|
| Phase 0 | 定位「一次成功匹配消除」的唯一结算入口 | 结论 + 三连/连续/道具三种路径的计数验证 | 无代码变更 |
| Phase 1 | 配置 + 状态机 + 事件接线（效果 = Noop，表现 = 日志） | `0→6→触发→完成解锁` 可观察 | 摘除充能入口即完全禁用 |
| Phase 2 | 冻结效果规格 → 新增 Filter / Effect 实现 | 目标规则与逻辑变更确定 | 移除新增注册项，既有系统不变 |
| Phase 3 | ViewAction + 充能槽 HUD + 完成回调 | 表现链路闭环 | 仅移除超彩 View 注册与资源 |
| Phase 4 | 开关、埋点、自动化测试、Play Mode/设备验证 | 可发布状态 | 用开关关闭入口 |

## 十一、测试与验收要点

| 类别 | 用例 |
|---|---|
| 计数口径 | 三连消除 +1；连续两次匹配 +2；仅选牌/移动 +0；道具触发的匹配按 Phase 0 确认口径；连锁匹配不重复计数 |
| 门槛与触发 | 第 1–5 次不触发；第 6 次仅触发一次；触发中再次结算不重复启动；一次多张消除只记一次 |
| 状态机健壮性 | 表现未完成、异常中断、关卡退出均不遗留处理锁；扣减只发生一次（对照染色炸弹的双扣缺陷做回归） |
| 效果 | 无目标 / 目标不足 / 目标位于可见·不可见 / Bar / OverBar / 带障碍（以冻结的效果边界为准） |
| 一致性 | HUD 显示值恒等于 Logic 权威能量（不存在两份计数） |
| 兼容 | 无超彩配置的旧资源安全关闭；旧关卡/Record 兼容（新增 flag 位不影响旧存档解析） |
| Unity | 静态检查与 `git diff --check` 不能替代 Play Mode、资源加载与热更新验证，必须单独执行 |

## 十二、风险清单

| 风险 | 影响 | 对策 |
|---|---|---|
| 充能入口挂错（挂在牌销毁/View 回调） | 多充能或漏充能，难定位 | Phase 0 先定位唯一结算点，并用三条路径验证 |
| 在匹配流程内同步触发 | 重入、结算错乱、连锁计数异常 | 充能只标记，触发收敛到安全点 flush |
| 效果未定就写死 TileType | 效果改动推翻已实现逻辑 | Effect 插槽 + Noop 默认实现 |
| 处理锁泄漏 | 后续匹配全部卡死 | 所有提前返回路径先解锁；退出/中断幂等复位 |
| 能量双扣 | 玩家体感「满能了却没触发」 | 扣减收敛到 `ConsumeCharge()` 单点 |
| 双份 View 目录不同步 | Headless 与 GameView 行为不一致 | 新增文件清单按双份登记，评审时逐条核对 |
| 静态配置字段被 GM 污染 | 多关卡参数串味 | 配置实例化或只读；GM 仅影响当前局 |
| 跨局状态 | 重开继承上一局能量 | 默认不持久化；`OnLevelStart` 复位 |

## 十三、待确认清单（需产品/主程拍板）

1. 触发后能量：清零 / 扣 6 结转 / 满能等待主动释放？
2. 触发时机：当次结算后立即（方案 B）/ 安全帧（方案 A）/ 玩家主动（方案 C）？
3. 效果规格六项：目标范围、影响区域、是否改 TileType、降级策略、是否给奖励、是否可跳过？
4. 门槛配置归属：固定 6 / 关卡配置 / AB 下发？
5. 是否需要前置解锁条件（胜场、活动开关）？
6. 充能可视化形态：能量条 / 满能提示 / 飘字 / 音效？
7. 埋点字段契约与运营指标？

## 关联

- [[分析-染色炸弹实现逻辑-v1|染色炸弹实现逻辑]] — 能量与 Action/ViewAction 分层参考
- [[任务-Tile超彩|任务-Tile超彩]] — 本需求的规划与验收口径
- [[分析-局内道具逻辑梳理|局内道具逻辑梳理]] — 局内道具入口与逻辑层背景
- [[02-PROJECTS/TileMatch/_MOC|TileMatch 知识库 MOC]] — 项目总入口
