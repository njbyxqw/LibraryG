---
title: TileMatch 知识库 MOC
tags: [TileMatch, MOC]
type: index
status: finalized
date: 2026-07-03
aliases:
  - TileMatch 知识库_MOC
---

# TileMatch 知识库 — 总入口

> 本文档是 TileMatch 知识库的导航中心。从上到下按「模块 → 子模块 → 具体文档」组织。

---

## 快速入口

- [[_项目概览|项目概览]] — TileMatch 项目基本信息
- [[局内障碍知识库_MOC|局内障碍知识库 MOC]] — 障碍系统总入口
- [[知识库文档顺序索引|知识库文档顺序索引]] — 按 cat_order 集中排序
- [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑分析]] — 高层综述（03-KNOWLEDGE）
- [[03-KNOWLEDGE/TileV2-Editor/TileV2 编辑器概览|TileV2 编辑器概览]] — 编辑器高层综述

---

## 📊 知识库仪表盘（Dataview）

> 需安装并启用 Obsidian **Dataview** 社区插件后生效。启用后下方表格会自动统计 `02-PROJECTS/TileMatch` 下的所有笔记。

### 全部文档（按修改时间）
```dataview
TABLE type, status, date
FROM "02-PROJECTS/TileMatch"
WHERE type
SORT file.mtime DESC
```

### 各分类文档数
```dataview
TABLE length(rows) AS 文档数
FROM "02-PROJECTS/TileMatch"
WHERE type
GROUP BY file.folder
```

### 最近更新（Top 10）
```dataview
TABLE date, status
FROM "02-PROJECTS/TileMatch"
WHERE date
SORT date DESC
LIMIT 10
```

### 草稿待完善（status = draft）
```dataview
TABLE date
FROM "02-PROJECTS/TileMatch"
WHERE status = "draft"
SORT date DESC
```

---

## 游戏逻辑

### Rocket 火箭牌
- [[分析-RocketV2完整逻辑-v2（重构版）|RocketV2 完整逻辑]]
- [[分析-RocketV2技术实现-v1|RocketV2 技术实现]]
- [[分析-火箭牌V2当前逻辑分析（基于代码）-v1|V2 当前逻辑（基于代码）]]
- [[报告-RocketVL闪电球视觉替换|RocketVL 闪电球视觉替换]]

### Effect 牌系统
- [[Effect牌-类型全览|Effect 牌类型全览]]
- [[Effect-Ice|Effect-Ice]]
- [[Effect-Ice2x2|Effect-Ice2x2]]
- [[Effect-Chain|Effect-Chain]]
- [[Effect-Cirrus|Effect-Cirrus]]
- [[Effect-Cloud|Effect-Cloud]]
- [[Effect-Cookie|Effect-Cookie]]
- [[Effect-Crate|Effect-Crate]]
- [[Effect-Curtain|Effect-Curtain]]
- [[Effect-GiftBox|Effect-GiftBox]]
- [[Effect-Golden|Effect-Golden]]
- [[Effect-Grass|Effect-Grass]]
- [[Effect-Jelly|Effect-Jelly]]
- [[Effect-Mystery|Effect-Mystery]]
- [[Effect-Pig|Effect-Pig]]
- [[Effect-Stone|Effect-Stone]]

### 障碍牌系统
- [[障碍牌-类型全览|障碍牌类型全览]]
- [[障碍牌-Rocket|障碍牌-Rocket]]
- [[障碍牌-CandyCube系列|障碍牌-CandyCube 系列]]
- [[障碍牌-Ore系列|障碍牌-Ore 系列]]
- [[障碍牌-ShellBox|障碍牌-ShellBox]]
- [[障碍牌-特殊机制|障碍牌-特殊机制]]
- [[障碍牌-Flip|Flip]] · [[障碍牌-JokerFlip|JokerFlip]] · [[障碍牌-Switch|Switch]]
- [[障碍牌-CardBox|CardBox]] · [[障碍牌-SlotMachine|SlotMachine]] · [[障碍牌-SuitCase|SuitCase]]
- → [[局内障碍知识库_MOC|全部障碍牌 (21篇)]]

### 其他逻辑分析
- [[分析-AssignTileTypeByDepth分池打乱策略-v1|AssignTileTypeByDepth 分池打乱策略]] — **2026-07-20 新建** 完整算法流程、深度映射、提交历史
- [[分析-死局逻辑与改进方案-v1|死局逻辑与改进方案]]
- [[分析-关卡连胜与闪电球逻辑-v1|关卡连胜与闪电球逻辑]]
- [[分析-跑关机器人逻辑分析-v1|跑关机器人逻辑分析]]
- [[分析-障碍Tile生成与序列逻辑-v1|障碍Tile生成与序列逻辑]] — **2026-07-20 更新 V2 分池修复**，分池细节见 [[分析-AssignTileTypeByDepth分池打乱策略-v1|分池打乱策略]]
- [[分析-局内道具逻辑梳理|局内道具逻辑梳理]]
- [[Shuffle改造AB测试方案|Shuffle 改造 AB 测试方案]]
- [[风车Shuffle优化提需|风车(Shuffle)优化提需]]

---

### BUG 记录
- → `游戏逻辑/BUG/` — 代码逻辑 BUG（独立文件）+ [[BUG-临时汇总|临时汇总（按日期追加）]]
  - [[BUG-AssignTileTypeByDepth-单花色越界崩溃-v1|单花色越界崩溃]] — **2026-07-24**

---

## 编辑器

- [[分析-关卡编辑器界面与功能逻辑梳理-v1|关卡编辑器界面与功能逻辑梳理]]
- [[分析-TileSelectionView花色加载方案-v1|TileSelectionView 花色加载方案]]
- [[分析-编辑器快捷键系统-v1|编辑器快捷键系统]]
- [[分析-编辑器统计功能|分析-编辑器统计功能]]
- [[报告-关卡文件管理工具|关卡文件管理工具]]
- [[规范-本地扩展开发|本地扩展开发规范]]
- [[报告-单牌块牌底配置功能实现记录-v1|单牌块牌底配置功能实现记录]] — 13文件+5个踩坑+复建指南
- [[复盘-牌底笔刷功能开发|牌底笔刷功能开发复盘]] — v1~v3 三次失败尝试+7条教训
- [[工具-牌局生成深度显示-v1|牌局生成深度显示工具]] — **2026-07-20 新增** Scene Gizmos + Console 统计，关联 [[分析-AssignTileTypeByDepth分池打乱策略-v1|分池打乱策略]]

---

## 打点

- [[报告-Tile打点事件梳理_2026-06-08|Tile 打点事件梳理]]
- [[分析-Tile打点解析-v1|Tile 打点解析]]
- [[分析-Tile打点事件文档SQL参考-v1|Tile 打点事件文档 SQL 参考]]
- [[报告-关卡难度分析SQL_完整版_2026-07-03|关卡难度分析 SQL]]
- [[分析-SQL审查报告_关卡难度分析|SQL 审查报告]]
- [[分析-关卡间隔时长SQL-v3|关卡间隔时长 SQL]] — **2026-08-28 v3** 用户×区间列透视，m=1 每关一列 `[1,2]…[99,100]`，SEQUENCE 简写配置

---

## 工具

- [[索引-HTML附件与外部链接汇总|HTML附件与外部链接汇总]] — 所有 HTML 文件路径与可共享链接
- [[报告-关卡数据分析工具-V3-2026-07-02|关卡数据分析工具 V3]]
- [[报告-关卡数据分析工具|报告-关卡数据分析工具]]
- [[分析-三工具功能梳理与集成建议|三工具集成分析]]
- [[报告-关卡替换对照表工具|关卡替换对照表]] · [[记录-关卡替换对照表工具-工作记录|工作记录]]
- [[报告-关卡数据对比工具|关卡数据对比工具]] · [[记录-关卡数据对比工具-工作记录|工作记录]]
- [[报告-关卡文件追踪工具|关卡文件追踪工具]]
- [[报告-关卡文件变更追踪-2026-06-26|关卡文件变更追踪]]

---

## 参考

- [[参考-关卡资源路径速查|关卡资源路径速查]] — **2026-07-28 新建** 花色 icon、背景、破碎特效、主题弹窗等全部磁盘路径与加载链路

---

## 规范与标准

- [[规范-知识库文档分类标准|知识库文档分类标准]]
- [[规范-知识库健康检查|知识库健康检查规范]]
- [[规范-本地扩展开发|本地扩展开发规范]]
- [[知识库编号方案_整合v1_2026-07-08|编号方案]]
- [[待办-后续事项|后续待办]] — 知识库剩余改进项
- [[规范-自动化任务设计-v1|自动化设计规范]] — 同步与维护任务终版设计

---

## Git 工作流

- [[记录-gitignore本地忽略配置|gitignore 本地忽略配置]]

---

## 关联
- [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑分析]]
- [[03-KNOWLEDGE/TileV2-Editor/TileV2 编辑器概览|TileV2 编辑器概览]]
- [[_项目概览|返回项目概览]]
