---
title: 产品分析 MOC
date: 2026-10-21
type: index
status: current
lifecycle: current
tags:
  - 产品分析
  - MOC
  - 竞品
aliases:
  - 产品分析总入口
  - 竞品调研总入口
---

# 产品分析 MOC

> 独立承载竞品与外部产品的资源使用、功能逻辑、活动结构和版本差异分析。分析默认覆盖图片、动效、音效与逻辑，并保留静态证据、运行时验证和远端缺失的边界。

## 任务路由

| 需求 | 入口 |
|---|---|
| 长期任务、三条主线与持续队列 | [[02-PROJECTS/产品分析/任务-竞品调研体系建设与持续维护|竞品调研体系建设与持续维护]] |
| 模块/功能分析方法与维护范例 | [[02-PROJECTS/产品分析/方法-竞品模块分析与持续维护|包体＋运行存储＋代码与资源对位方法]] |
| Royal Match 产品级导航 | [[02-PROJECTS/产品分析/Royal Match/_MOC|Royal Match MOC]] |
| 当前产品列表 | [[#产品入口|产品入口]] |
| 大文件资源保存规则 | [[02-PROJECTS/产品分析/资源目录规范|产品分析资源目录规范]] |
| APK / XAPK 静态分析方法 | [[02-PROJECTS/Agent/工具/指南-REA休闲游戏APK静态分析接入与边界|REA APK 分析指南]] |
| MuMu 运行后存储与配置补全 | [[02-PROJECTS/产品分析/评估-MuMu运行后存储采集与REA分析-2026-10-26|MuMu 沙盒采集可行性与 Windows 预检]] |
| Royal Match 资源与逻辑总览 | [[02-PROJECTS/产品分析/Royal Match/资源与逻辑分析总览-38911|Royal Match 38911 总览]] |
| Royal Match 系统活动、关卡与主场景 | [[02-PROJECTS/产品分析/Royal Match/系统活动关卡与主场景框架-38911|Royal Match 38911 大体框架]] |
| Royal Match 弹窗规则 | [[02-PROJECTS/产品分析/Royal Match/系统拆解-弹窗框架-38911|Royal Match 38911 弹窗框架与展示规则]] |
| Royal Match 设备分辨率适配 | [[02-PROJECTS/产品分析/Royal Match/系统拆解-设备分辨率与横竖屏适配-38911|Royal Match 38911 设备分辨率与横竖屏适配]] |
| Royal Match 活动清单 | [[02-PROJECTS/产品分析/Royal Match/活动清单与简述-38911|Royal Match 38911 活动清单与简述]] |
| Royal Match 逐活动深入分析 | [[02-PROJECTS/产品分析/Royal Match/活动/_MOC|活动档案与分析进度]] · [[02-PROJECTS/产品分析/Royal Match/活动/Lava Quest/README|Lava Quest 规则、配置、资源详细拆解]] |
| Royal Match Lava Quest / Ancient Adventure | [[02-PROJECTS/产品分析/Royal Match/活动定位-Lava Quest与Ancient Adventure-38911|两项连胜活动的规则、配置、分组协议与关卡回调边界]] |
| Royal Match 本地资源路径 | [[02-PROJECTS/产品分析/Royal Match/资源路径索引|Royal Match 资源路径索引]] |
| Match Villains 资源与逻辑总览 | [[02-PROJECTS/产品分析/Match Villains/资源与逻辑分析总览-7307|Match Villains 7307 总览]] |
| Match Villains 活动系统 | [[02-PROJECTS/产品分析/Match Villains/活动系统总览-7307|Match Villains 7307 活动总览]] |
| Match Villains 活动数值与策略 | [[02-PROJECTS/产品分析/Match Villains/活动数值与策略配置-7307|Match Villains 7307 活动数值与策略]] |
| Match Villains 本地资源路径 | [[02-PROJECTS/产品分析/Match Villains/资源路径索引|Match Villains 资源路径索引]] |
| Tile Kingdom 资源与逻辑总览 | [[02-PROJECTS/产品分析/Tile Kingdom/资源与逻辑分析总览-1.58|Tile Kingdom 1.58 总览]] |
| Tile Kingdom 本地资源路径 | [[02-PROJECTS/产品分析/Tile Kingdom/资源路径索引|Tile Kingdom 资源路径索引]] |
| Tile Temple 活动 | [[02-PROJECTS/产品分析/Tile Kingdom/活动拆解-Tile Temple-1.58|Tile Temple 活动拆解]] |
| Tile Kingdom 弹窗逻辑 | [[02-PROJECTS/产品分析/Tile Kingdom/系统拆解-弹窗框架-1.58|Tile Kingdom 1.58 弹窗框架]] |

## 产品入口

资源与文档采用双层结构：原始包和大体积产物进入当前设备 LG 根目录下的 `06-PRODUCT-ASSETS/<Product>/<Version>/`（Windows：`D:\LibraryG`；Mac：`/Users/dean/LibraryG`）；正文与索引维护在本项目目录。大文件不默认跨设备同步。详见 [[02-PROJECTS/产品分析/资源目录规范|资源目录规范]]。

### Royal Match

产品级稳定入口：[[02-PROJECTS/产品分析/Royal Match/_MOC|Royal Match MOC]]。以下保留既有专题快捷入口；后续模块优先归入产品 MOC，不持续扩张总目录。

- [[02-PROJECTS/产品分析/Royal Match/资源与逻辑分析总览-38911|38911 资源与逻辑分析总览]] — 包体、Android 启动、Unity 资源、三消棋盘、活动 Bundle 与难度随机入口的静态基线
- [[02-PROJECTS/产品分析/Royal Match/系统活动关卡与主场景框架-38911|38911 系统活动、关卡与主场景框架]] — 活动分层与回流、关卡处理主链、Home Flow 和场景切换的大体结构
- [[02-PROJECTS/产品分析/Royal Match/系统拆解-弹窗框架-38911|38911 弹窗框架与展示规则]] — 全屏/普通弹窗、活动状态触发、礼包规则、Flow 串行与同界面多级弹窗
- [[02-PROJECTS/产品分析/Royal Match/系统拆解-设备分辨率与横竖屏适配-38911|38911 设备分辨率与横竖屏适配]] — 比例分档、相机视口、安全区、横竖屏广播，以及 Home、活动弹窗和关卡棋盘的局部适配
- [[02-PROJECTS/产品分析/Royal Match/活动清单与简述-38911|38911 活动清单与简述]] — `EventsHelper` 中央 36 项活动，以及常驻、旧版和活动相关外围模块
- [[02-PROJECTS/产品分析/Royal Match/活动定位-Lava Quest与Ancient Adventure-38911|Lava Quest 与 Ancient Adventure 活动规则]] — Lava 的模拟分组协议、7 连胜与奖池结算；Ancient 的阶段/奖励配置；两者的关卡回调和局内调控边界
- [[02-PROJECTS/产品分析/Royal Match/资源路径索引|资源路径索引]] — 原始包、拆包、图片/音频导出与 IL2CPP 产物位置

### Match Villains

- [[02-PROJECTS/产品分析/Match Villains/资源与逻辑分析总览-7307|7307 资源与逻辑分析总览]] — 包体、图片、动效、音频、关卡、DDA 与逻辑的静态基线
- [[02-PROJECTS/产品分析/Match Villains/活动系统总览-7307|7307 活动系统总览]] — 七层活动框架、三类系统角色、49 个具体模块及统一下钻入口
- [[02-PROJECTS/产品分析/Match Villains/活动数值与策略配置-7307|7307 活动数值与策略配置]] — 计分、概率、阶梯、失败补偿、Power Cards 与 DDA 本地基线
- [[02-PROJECTS/产品分析/Match Villains/资源路径索引|资源路径索引]] — 原始包、拆包、Unity 导出与 IL2CPP 产物位置

### Tile Kingdom

- [[02-PROJECTS/产品分析/Tile Kingdom/资源与逻辑分析总览-1.58|1.58 资源与逻辑分析总览]] — 图片、动效、音效、逻辑四维总览与验证状态
- [[02-PROJECTS/产品分析/Tile Kingdom/资源路径索引|资源路径索引]] — 原始包、解包输出、导出资源、逻辑证据和工具位置
- [[02-PROJECTS/产品分析/Tile Kingdom/活动拆解-Tile Temple-1.58|Tile Temple 活动拆解]] — 活动入口、状态、计分、淘汰、奖励、动效和音效使用链
- [[02-PROJECTS/产品分析/Tile Kingdom/系统拆解-弹窗框架-1.58|1.58 弹窗框架静态拆解]] — 状态栈、打开/关闭生命周期、遮罩点击、默认动效、通用弹窗与自动展示边界

## 固定分析口径

| 维度 | 关注内容 |
|---|---|
| 图片 | Sprite/Texture/Atlas、Prefab/UI 消费者、材质依赖和触发界面 |
| 动效 | Animator、AnimationClip、ParticleSystem、Spine/Tween、控制组件和触发条件 |
| 音效 | AudioClip、SoundKey、调用方法、触发事件、循环和 Mixer/配置绑定 |
| 逻辑 | 入口、状态机、数据、判定、奖励、失败、埋点和远端配置 |
| 数值与策略 | 模拟人数、概率、重试/保底、连胜关联、AB、关卡内外调节；沿条件与消费者验证，不只看字段名 |
| 证据覆盖 | 安装包/分包、运行落盘、资源与代码版本、保存状态、实际生效和服务端未知分开标明 |

统一证据链：`资源 → Prefab/组件 → 控制逻辑 → 触发条件 → 表现结果`。

长期维护采用 [[02-PROJECTS/产品分析/方法-竞品模块分析与持续维护|范例方法]]：新发现更新现有主题章节，必要时合并和重排，过程留 Daily/证据。Lava Quest 是首个新方法范例，不是全部模块的固定规则模板。

## 关联

- [[HOME|LibraryG 主入口]]
- [[AI总MOC|AI 总 MOC]]
- [[02-PROJECTS/Agent/工具/指南-REA休闲游戏APK静态分析接入与边界|REA APK 分析指南]]
- [[02-PROJECTS/产品分析/资源目录规范|产品分析资源目录规范]]

