---
title: TileV2 编辑器概览
date: 2026-06-25
type: knowledge
tags:
  - knowledge
  - tilev2
  - editor
---
[[分析-关卡编辑器界面与功能逻辑梳理-v1|关卡编辑器界面与功能逻辑梳理]]
# TileV2 编辑器概览

> TileMatch 关卡编辑器，基于 UGUI Canvas + Prefab 构建

## 核心概念

### 多阶段白盒工作流

| 阶段 | 内容 | 说明 |
|------|------|------|
| Phase 1 | tile 空间布局 | 确定牌的位置和层级 |
| 后续阶段 | 花色/Effect/Pile/难度调控 | 在布局基础上添加游戏元素 |

### FirstNHighlight 策略
- **参数**: Count=3
- **作用**: 控制初始高亮的花色数量

### 子牌保护逻辑
- 防止关键牌在早期被消除

## LocalExtensions 本地扩展

### 已完成功能
1. **TileSelectionView 花色加载 V1**
   - 从 LevelConfig.TileTypes 动态读取并渲染独立 TileType 类别的花色
2. **ShortcutBindingManager 功能本地化**
   - 快捷键绑定管理

### 技术方案
- 反射注入 + `[InitializeOnLoad]`
- 零存储动态绑定
- 不修改主代码

### 目录规范
- `.workbuddy/` — 工作空间配置
- `workbuddy_archives/` — 归档产物

## 工具链

### LevelFileMigrationTool (v3.3)
- QueryLevels 性能优化
- 首屏加载 < 1秒

### TileTypeGroupConfig
- Protobuf 配置序列化
- 修复了 .bytes 损坏问题

## 相关文档

### 编辑器分析
- [[分析-关卡编辑器界面与功能逻辑梳理-v1|关卡编辑器界面与功能逻辑梳理]]
- [[分析-编辑器快捷键系统-v1|编辑器快捷键系统]]
- [[分析-TileSelectionView花色加载方案-v1|TileSelectionView花色加载方案]]

### 规范
- [[规范-本地扩展开发|本地扩展开发规范]]

### 报告
- [[报告-关卡文件管理工具|关卡文件管理工具报告]]
- [[报告-关卡文件追踪工具|关卡文件追踪工具报告]]

### 项目
- [[02-PROJECTS/TileMatch/_项目概览|TileMatch 项目概览]]
- [[03-KNOWLEDGE/Unity/Unity 开发笔记|Unity 开发笔记]]
- [[03-KNOWLEDGE/Game-Logic/游戏逻辑分析|游戏逻辑分析]]
