---
title: TileScape GM 工具
date: 2026-08-26
type: index
status: current
project: TileScape
lifecycle: current
verification: static-index
tags: [TileScape, GM, Debug, 工具]
source: "TS 当前工作区静态代码审计（2026-08-26）与对话整理"
---

# TileScape GM 工具

> 新增、排查和验证 GM 命令的专题入口。这里记录可复用的规则与每个新工具的独立说明；代码总链路仍见 [[02-PROJECTS/TileScape/代码框架/梳理-GM工具注册与扩展链路|GM 工具注册与扩展链路]]。

## 使用入口

1. 新增命令前，先读 [[规范-GM工具新增与使用规则|GM 工具新增与使用规则]]。
2. 再打开所属业务域的工具文档，确认命令、状态、影响范围和验证边界。
3. 未列入专题的既有命令，按代码总链路中的 Tab 与 owner 定位。

## 当前规则与工具

- [[规范-GM工具新增与使用规则|GM 工具新增与使用规则]] — 门控、注册位置、命名、副作用与验证约束。
- [[工具-屏蔽关卡动更开关|屏蔽关卡动更开关]] — `Tile` Tab 的本机动态关卡屏蔽开关；当前处于 Unity 运行验证中。

## 边界

- 本目录只记录已确认的 GM 机制与具体工具；方案或未实施演进标注为建议，不作为现行规则。
- 关卡、配置、Profile、DLC、SDK 等副作用仍以其业务 owner 的代码事实为准，GM 仅是调试入口。
- 每新增一项具有持久化、网络、缓存或数据修改副作用的工具，都应新增独立文档并从本页挂入口。

## 关联

- [[02-PROJECTS/TileScape/_MOC|TileScape 知识库 MOC]]
- [[02-PROJECTS/TileScape/代码框架/梳理-GM工具注册与扩展链路|GM 工具注册与扩展链路]]
