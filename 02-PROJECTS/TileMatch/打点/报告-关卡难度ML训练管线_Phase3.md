---
title: 报告-关卡难度ML训练管线_Phase3
tags: [TileMatch, ML, 训练管线, 模型训练]
type: report
status: draft
date: 2026-07-24
---

# 关卡难度 ML 训练管线 — Phase 3 方案

> 前置依赖：Phase 1 SQL 宽表 + Phase 2 关卡静态特征 CSV 均已就绪。

## 一、数据准备

### 1.1 输入

| 来源 | 内容 | 粒度 |
|---|---|---|
| `SQL_ML训练宽表_step1.sql` | user×level 宽表（y + 四维特征） | user×level |
| `level_static_features.csv` | 关卡静态特征（Phase 2 提取） | level |

### 1.2 拼接

```
wide_table = SQL输出 JOIN level_static_features ON lv_name
```

### 1.3 数据清洗

| 步骤 | 内容 |
|---|---|
| 缺失值 | COALESCE 为 0 的历史特征（首次关卡无历史） |
| 异常值 | total_attempts > 50 → 截断（可能是挂机/异常） |
| 样本量过滤 | 每关至少 30 个样本，每用户至少 5 关 |
| 类型转换 | category 列 → int/factor；lv_name → str（后续做 embedding） |

## 二、特征工程

### 2.1 编码策略

| 特征类型 | 编码方式 |
|---|---|
| 数值连续（card_total, avg_props_before…） | StandardScaler 标准化 |
| 数值离散（board_x, board_y, elements_per_level） | 保持原值或分箱 |
| 类别（theme_id, activityid, ab_group1） | Label Encoding + Embedding 或 OneHot（低基数） |
| 文本（lv_name, comment） | 暂不做 NLP，仅作为 key |
| 比例（clear_rate, random_ratio） | 保持原始 0-1 值 |

### 2.2 目标变量（y）处理

| y | 原始值 | 处理 | 指标 |
|---|---|---|---|
| is_clear | 0/1 | 不变 | AUC, F1 |
| total_attempts | 1-N | log(attempts+1) 变换 → 回归 | RMSE, MAE |
| total_props | 0-N | log(props+1) 变换，或分箱为 0/1-3/4+ | RMSE 或 MultiClass |

> log 变换原因：尝试次数和道具消耗都是右偏分布（少数用户极端多），log 后更接近正态，模型训练更稳定。

## 三、训练/验证切分

### 3.1 切分策略：按用户切分

```
train_users : val_users : test_users = 70% : 15% : 15%
```

按用户（非随机行）切分的原因：
- 同一用户的多条样本共享历史特征，随机切分会泄露
- 代码实现：`sklearn.model_selection.GroupShuffleSplit`

### 3.2 对新关卡冷启动的验证

额外增一组"按关卡切分"：

```
train_levels : test_levels = 80% : 20%（按 lv_num 排序后的后 20%）
```

模拟"用已知关卡预测新关卡"场景。

## 四、模型选择

### 4.1 主模型：梯度提升树

| 模型 | 适用 y | 理由 |
|---|---|---|
| LightGBM / XGBoost | is_clear（分类） | 表格数据首选，特征重要度可解释 |
| LightGBM / XGBoost | log(attempts+1)（回归） | 同上 |
| LightGBM / XGBoost | log(props+1)（回归） | 同上 |

备选：TabNet（深度表格模型）若 GBTree 效果不佳。

### 4.2 基准模型

| 基准 | 含义 |
|---|---|
| 群体均值 | 直接用 level_group.difficulty 预测 is_clear |
| 关卡静态线性回归 | 只用 I 类特征 |
| 用户历史线性回归 | 只用 III 类特征 |

新模型必须在验证集上显著优于所有基准，才算有价值。

## 五、特征筛选

### 5.1 第一轮：相关性过滤

- 特征间相关系数 > 0.95 → 保留一个
- 特征与 y 的相关系数 < 0.01（且 p > 0.05）→ 标记为弱特征

### 5.2 第二轮：模型特征重要度

- LightGBM 训练后输出 `feature_importance_`
- 按 Gain / Split 排序
- 累积贡献 < 1% 的特征 → 考虑剔除

### 5.3 第三轮：消融实验

- 逐个剔除特征维度（I→II→III→IV）
- 观察 AUC/RMSE 下降幅度 → 量化各维度贡献

## 六、输出

| 产出 | 格式 |
|---|---|
| 训练好的模型 | `.pkl` (joblib) 或 `.txt` (LightGBM) |
| 特征重要度报告 | CSV（feature / importance / gain / split） |
| 消融实验结果 | CSV（dimension / AUC / RMSE） |
| 预测脚本 | `predict.py` — 输入 (user_id, lv_name) → 输出 3 个预测值 |

## 七、依赖包

```
pandas, numpy, scikit-learn, lightgbm, xgboost, matplotlib, seaborn, joblib
```

---

## 关联

- [[_MOC|TileMatch 知识库 MOC]]


