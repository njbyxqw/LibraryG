---
title: Royal Match 分层与AB实验配置
date: 2026-10-28
status: current
tags: [产品分析, RoyalMatch, 运营配置]
---

# Royal Match 分层与AB实验配置

来源见 [[02-PROJECTS/产品分析/Royal Match/运营配置/排期与配置总览|总览]]。分清三件事：已下发的多套表、账号保存的组值、实际执行的分支。两账号同时存在版本/历史/时间差异，不把相关性写成分层因果。

## 已获取的分层配置

| 模块 | 已取得 | 边界 |
|---|---|---|
| Book/Madness | Config1/2各25阶段；两号同为2203版；当前号multiplierTokenOverride有5项，历史号为空 | 基础目标与奖励选择见Book主文档；同版本号不保证JSON正文一致；覆盖差异原因未确认 |
| TeamTreasure | 6个segment，三个目标档及对应奖励 | 可读全6段目标，不证明当前团队属于哪一段 |
| Pinata | 历史325版有6个segments及butlerMultiplierAbSegment | 备用AB配置存在不等于启用 |
| BalloonRise | 10个t、10个butlerMultiplierAbTargets及10个奖励 | 两套目标均可读，实际选择待对位 |
| RoyalPass | 普通steps/Butler AB各32项；当前96/历史97 | 有版本差异，不只账号差异 |
| ArcheryArena | 历史20阶段、20个AB替代阶段、10个排名奖励、5个streak项 | 事件缓存已过期 |
| OceanOdyssey | 当前20阶段，历史15阶段 | 实际正文不同；可能受版本、账号或期配置影响，原因未确认 |
| Journey/Starfall | 历史segment分别6/1 | 仅取得选中层，没取得所有segment奖励表 |
| SLBMoveConfig | c/d/f/g/h交错数值数组，合计306对 | 原始数组长度92/222/168/106/24，不能误报为612个关卡；并非当前全量生效 |
| SeasonalCardCollection | 动态卡包权重、紫包规则因子、两套事件奖励覆盖 | 权重不直接等于最终抽中概率，需消费者与条件分母 |
| TrainJourney | 历史公共/用户配置及跨活动奖励覆盖 | 不能把LastEventId当活动时间 |

TeamTreasure六层实值：

| segment | 三段目标t |
|---|---|
| 1 | [400, 800, 1200] |
| 2 | [750, 1500, 2500] |
| 3 | [1500, 3000, 5000] |
| 4 | [2500, 4500, 8000] |
| 5 | [3000, 6000, 9000] |
| 6 | [4000, 8000, 12000] |

Pinata完整分段原值：

```json
{
  "segments": [
    {
      "s": 1,
      "t": [
        40,
        60,
        60
      ]
    },
    {
      "s": 2,
      "t": [
        40,
        60,
        60
      ]
    },
    {
      "s": 3,
      "t": [
        40,
        60,
        60
      ]
    },
    {
      "s": 4,
      "t": [
        40,
        60,
        60
      ]
    },
    {
      "s": 5,
      "t": [
        40,
        60,
        60
      ]
    },
    {
      "s": 6,
      "t": [
        40,
        60,
        60
      ]
    }
  ],
  "butlerMultiplierAbSegment": {
    "s": 0,
    "t": [
      40,
      60,
      60
    ]
  }
}
```

Balloon普通/AB目标：

```json
{"t": [5, 10, 15, 15, 15, 30, 30, 40, 40, 50], "butlerMultiplierAbTargets": [10, 10, 20, 20, 30, 35, 35, 40, 50, 100]}
```

## 账号分层与AB记录

两号UserOfferSegment/DynamicOfferSegment原值均0，不能把0直接解释成低付费或无分层；对应版本当前1183/1383、历史1182/1382。历史还有UserSpecialOfferSegment=0、版本50。版本不是组值。

当前56条、历史66条，共81个AB ID，交集41个。其中共同ID只有238的原值不同（当前8、历史3），38911常量名为DukesTreatsOldUserAbId。其他不同记录很多属于新/老用户不同ID，不能按“缺少相同ID”判无实验。

38911常量表对位到38个ID，补读39781的AbTestHelper字段后合计43个ID有名称，剩余38个保留未知。新增定位包含ElementHunt252、WebStore256、ConsecutiveEvents260、SuperfavorOffer262等；历史原值分别5/6/4/7，不能仅凭名称推导实际活动连开规则或礼包优惠幅度。组值保存与AB启用不同：A/B/C等枚举只是基础值域，各消费方法还可能比较、映射或组合多个ID。表中分别保留两版常量名称；名称核对不等于已审计全部消费者。

超级光球相关：当前原始AB226=4，38911 GetSlbLevelChangeAbGroup对2～4有+4映射，因此该入口可返回内部8；最终选择还经过SetAbValues/历史组及教程状态。不能直接把4当成内部D组门槛，更不能直接写成当前已使用高目标表。前次当前阶段保存位仍为Config1。

完整原始组值和名称证据：[AB分组对照JSON](附件/AB分组对照.json)。下表“—”表示该样本未保存此ID，不表示已确认关闭。

| ID | 设备-1原值 | 历史原值 | 常量名及版本 |
|---|---|---|---|
| 4 | 6 | 6 | 未对位 |
| 9 | 2 | 2 | 未对位 |
| 11 | 4 | 4 | 未对位 |
| 15 | 3 | 3 | 未对位 |
| 17 | 1 | 1 | 未对位 |
| 18 | 3 | 3 | 未对位 |
| 20 | 4 | 4 | 未对位 |
| 22 | 3 | 3 | 未对位 |
| 24 | 4 | 4 | 未对位 |
| 25 | 2 | 2 | 未对位 |
| 26 | 3 | 3 | 未对位 |
| 28 | 3 | 3 | 未对位 |
| 32 | 4 | 4 | 未对位 |
| 42 | 6 | 6 | 未对位 |
| 44 | 2 | 2 | 未对位 |
| 54 | 2 | 2 | 未对位 |
| 56 | 1 | 1 | 未对位 |
| 94 | 3 | 3 | 未对位 |
| 98 | 4 | 4 | 未对位 |
| 104 | 3 | 3 | 未对位 |
| 108 | 2 | 2 | 未对位 |
| 116 | — | 4 | AgeConsentV2NewUserAbId（38911） |
| 118 | — | 1 | 未对位 |
| 125 | 2 | 2 | 未对位 |
| 127 | 2 | 2 | PrivacySettingsRedesignOldUser（38911） |
| 129 | 4 | 4 | RewardReductionOldUserAbId（38911） |
| 131 | 2 | 2 | 未对位 |
| 133 | 3 | 3 | 未对位 |
| 137 | 3 | 3 | PropellerRush3StepOldUserAbId（38911） |
| 141 | 2 | 2 | NewLeagueV2OldUserAbId（38911） |
| 147 | 5 | 5 | AncientAdventureOldUserAbId（38911） |
| 149 | 2 | 2 | SeasonalCardCollectionImprovementOldUserAbId（38911） |
| 153 | 3 | 3 | AncientAdventureV2OldUserAbId（38911） |
| 155 | 2 | 2 | 未对位 |
| 156 | 3 | — | 未对位 |
| 157 | — | 3 | 未对位 |
| 159 | 4 | 4 | RobotRivalsOldUserAbId（38911） |
| 161 | 2 | 2 | MultiplierTokenV2OldUserAbId（38911） |
| 165 | 4 | 4 | DailySkyRaceSpaceMissionOldUserAbId（38911） |
| 171 | 2 | 2 | 未对位 |
| 173 | 2 | — | 未对位 |
| 174 | — | 2 | 未对位 |
| 175 | 2 | — | PrivacySettingsKoreaNewUserAbId（38911） |
| 176 | — | 3 | PrivacySettingsKoreaOldUserAbId（38911） |
| 177 | 2 | — | NotificationReductionNewUserAbId（38911） |
| 178 | — | 2 | NotificationReductionOldUserAbId（38911） |
| 179 | 5 | — | ClashOfChampionsNewUserAbId（38911） |
| 180 | — | 5 | ClashOfChampionsOldUserAbId（38911） |
| 184 | — | 4 | BoosterRewardReductionOldUserAbId（38911） |
| 189 | 4 | — | MergeSmithNewUserAbId（38911） |
| 190 | — | 4 | MergeSmithOldUserAbId（38911） |
| 192 | 2 | 2 | RushEventsReplayableOldUserAbId（38911） |
| 194 | 6 | 6 | SuperchargeOfferOldUserAbId（38911） |
| 200 | 4 | 4 | MultiplePurchaseDynamicOfferOldUserAbId（38911） |
| 208 | 1 | 1 | LadderOfferShopCardOldUserAbId（38911） |
| 209 | 4 | — | AgeConsentV5NewUserAbId（38911） |
| 214 | — | 6 | MultiplierLevelTypeOldUserAbId（38911） |
| 219 | — | 7 | ShortExpeditionEventOldUserAbId（38911） |
| 225 | — | 3 | NextEventCollectibleOldUserAbId（38911） |
| 226 | 4 | — | SuperLightballLevelChangeV2NewUserAbId（38911） |
| 228 | 2 | — | DailyRewardsNewUserAbId（38911） |
| 229 | — | 2 | DailyRewardsOldUserAbId（38911） |
| 232 | — | 3 | 未对位 |
| 233 | 4 | — | 未对位 |
| 234 | — | 4 | 未对位 |
| 238 | 8 | 3 | DukesTreatsOldUserAbId（38911） |
| 243 | 3 | — | Single4PackageNewUserAbId（38911） |
| 244 | — | 3 | Single4PackageOldUserAbId（38911） |
| 245 | 4 | — | StarfallOfferNewUserAbId（38911） |
| 246 | — | 4 | StarfallOfferOldUserAbId（38911） |
| 247 | 3 | — | LiveActivityNewUserAbId（38911） |
| 248 | — | 3 | LiveActivityOldUserAbId（38911） |
| 250 | — | 1 | NewUserNewUxV3OldUserAbId（39781） |
| 252 | — | 5 | ElementHuntOldUserAbId（39781） |
| 253 | 3 | — | 未对位 |
| 254 | — | 3 | 未对位 |
| 256 | — | 6 | WebStoreOldUserAbId（39781） |
| 260 | — | 4 | ConsecutiveEventsOldUserAbId（39781） |
| 262 | — | 7 | SuperfavorOfferOldUserAbId（39781） |
| 263 | 1 | — | 未对位 |
| 264 | — | 3 | 未对位 |

## 待核验与持续维护

下一步优先级：礼包p档到商品SKU的绑定、动态礼包未下发的触发资格；DukesTreats AB238消费者；Ocean20/15阶段与Book倍率覆盖差异；集卡权重的消费公式。逐模块验证后回写现有章节。

本次不修改AB组、不提交购买、不宣称能由本地组值枚举完整服务器分群。新增抓取需保留采样时间/客户端版本/选中组/配置哈希；相同版本不同正文必须保留，不能按版本号去重。

返回 [[02-PROJECTS/产品分析/Royal Match/_MOC|产品MOC]]。
