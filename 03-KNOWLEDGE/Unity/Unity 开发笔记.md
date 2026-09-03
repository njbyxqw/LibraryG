---
title: Unity 开发笔记
date: 2026-06-25
type: knowledge
tags:
  - knowledge
  - unity
---

# Unity 开发笔记

> TileMatch 项目中涉及的 Unity 开发知识汇总

## 架构模式

### MVC + Command + Strategy + Observer
- **Model**: 数据模型，通过 Protobuf 序列化
- **View**: UGUI Canvas + Prefab
- **Controller**: 命令模式处理用户操作
- **Strategy**: 策略模式处理不同游戏行为
- **Observer**: 事件驱动的模块间通信

## UGUI 系统

- Canvas + Prefab 构建编辑器界面
- TileSelectionView — 花色选择视图
- 通过 LocalExtensions 实现零存储动态绑定

## Protobuf 配置

- 使用 `.bytes` 文件进行配置序列化
- TileTypeGroupConfig — 花色组配置
- LevelConfig — 关卡配置

## 程序集管理 (asmdef)

- 依赖 BettaFramework / BettaSDK
- 通过 asmdef 管理程序集间的引用关系

## LocalExtensions 扩展系统

- 反射注入 + `[InitializeOnLoad]` 实现零存储动态绑定
- 避免修改主代码
- 已完成: TileSelectionView 花色加载 V1, ShortcutBindingManager 功能本地化

## 相关

- [[02-PROJECTS/TileMatch/_项目概览|TileMatch 项目概览]]
- [[03-KNOWLEDGE/TileV2-Editor/TileV2 编辑器概览|TileV2 编辑器概览]]
