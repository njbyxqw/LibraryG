# Daily Logs 同步流程

> 建立日期：2026-07-01
> 目的：将 meatloaf_client01 的工作日志同步到 Obsidian Daily Notes

---

## 问题现状

### 缺失情况
- **meatloaf_client01** 有 18 个 Daily Logs（2026-05-22 ~ 2026-07-01）
- **Obsidian Daily Notes** 只有 1 个（2026-06-25.md）
- **缺失**：17 个日志需要同步

### 格式差异
| 项目 | meatloaf_client01 格式 | Obsidian 格式 |
|------|---------------------|---------------|
| Frontmatter | 无 | 有（date/weekday/tags） |
| 标题 | `# 2026-07-01 工作日志` | `# 2026年07月01日 星期二` |
| 时区 | 无 | weekday 字段（英文） |

---

## 同步方案

### 方案A：手动同步（一次性）
适用于：首次同步历史日志

**步骤**：
1. 读取 `meatloaf_client01/.workbuddy/memory/YYYY-MM-DD.md`
2. 转换格式（添加 frontmatter，修改标题）
3. 写入 `LibraryG/01-DAILY/YYYY-MM-DD.md`

**工具**：使用 WorkBuddy Write 工具

### 方案B：自动化同步（后续）
适用于：日常自动同步

**实现方式**：
1. **Obsidian CLI**：`obsidian daily:create` 命令
2. **Python 脚本**：定时任务（每天23:00执行）
3. **WorkBuddy Automation**：创建自动化任务

---

## 实施方案

### 第一步：首次同步（手动）
同步 17 个缺失的历史日志：

| 日期 | 状态 | 备注 |
|------|------|------|
| 2026-05-22 | ⏳ 待同步 | |
| 2026-05-25 | ⏳ 待同步 | |
| 2026-06-01 | ⏳ 待同步 | |
| 2026-06-02 | ⏳ 待同步 | |
| 2026-06-03 | ⏳ 待同步 | |
| 2026-06-08 | ⏳ 待同步 | |
| 2026-06-10 | ⏳ 待同步 | |
| 2026-06-12 | ⏳ 待同步 | |
| 2026-06-15 | ⏳ 待同步 | |
| 2026-06-16 | ⏳ 待同步 | |
| 2026-06-17 | ⏳ 待同步 | |
| 2026-06-18 | ⏳ 待同步 | |
| 2026-06-23 | ⏳ 待同步 | |
| 2026-06-24 | ⏳ 待同步 | |
| 2026-06-25 | ✅ 已同步 | 格式需要确认 |
| 2026-06-26 | ⏳ 待同步 | |
| 2026-06-30 | ✅ 已同步 | |
| 2026-07-01 | ✅ 已同步 | |

### 第二步：建立自动化（进行中）
创建每日自动同步机制：

**选项1：Obsidian CLI + 定时任务**
```bash
# 每天23:00执行
obsidian daily:append content="$(cat D:/meatloaf_client01/.workbuddy/memory/$(date +%Y-%m-%d).md)"
```

**选项2：WorkBuddy Automation**
- 创建 automation：每天23:00执行
- 动作：读取当日日志，同步到 Obsidian

**选项3：Python 脚本 + Windows 任务计划**
- 脚本：`sync_daily_logs.py`（已创建）
- 触发器：每天23:00
- 操作：执行 Python 脚本

---

## 同步脚本

### 脚本路径
`D:/meatloaf_client01/local_py_script/sync_daily_logs.py`

### 功能
1. 读取 `meatloaf_client01/.workbuddy/memory/` 下的所有日志
2. 转换格式为 Obsidian daily note 格式
3. 写入 `LibraryG/01-DAILY/`
4. 跳过已存在的文件

### 使用方法
```bash
cd D:/meatloaf_client01/local_py_script
python sync_daily_logs.py
```

### 注意事项
- **权限问题**：需要确保 `D:/LibraryG/01-DAILY/` 可写
- **编码问题**：使用 UTF-8 编码
- **格式问题**：确认 Obsidian frontmatter 格式正确

---

## 后续工作

### 1. 完成首次同步
- [ ] 同步剩余 15 个历史日志
- [ ] 验证同步结果（在 Obsidian 中打开确认）

### 2. 建立自动化
- [ ] 选择自动化方案（Obsidian CLI / WorkBuddy Automation / Python脚本）
- [ ] 配置定时任务
- [ ] 测试自动化流程

### 3. 文档更新
- [ ] 更新 WorkBuddy 记忆（记录同步流程）
- [ ] 更新 Obsidian 知识库（添加同步流程文档）

---

## 附录：格式转换示例

### 转换前（meatloaf_client01 格式）
```markdown
# 2026-07-01 工作日志

## 输出

- 生成 `Effect牌-类型全览.md`
...
```

### 转换后（Obsidian 格式）
```markdown
---
date: 2026-07-01
weekday: Tuesday
tags:
  - daily
---

# 2026年07月01日 星期二

## 输出

- 生成 `Effect牌-类型全览.md`
...
```

---

*本文档由 WorkBuddy 自动生成，记录 Daily Logs 同步流程*
