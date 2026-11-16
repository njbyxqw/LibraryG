---
name: lanhu-unity-import
description: "将蓝湖原始图层标注与手动下载切图接入现有 Unity UGUI 界面。用于蓝湖到 Unity 资源导入、位置尺寸还原、批量界面换皮及保留业务绑定的正式 Prefab 更新；支持映射预演、嵌套预制体局部覆盖、备份、静态验证和受保护回滚。"
---

# 蓝湖到 Unity 资源与布局接入

使用原始图层数据、显式节点映射和本目录 Python 工具修改已有 UGUI 预制体。工具使用 Python 3.9+ 标准库，不要求 MCP 服务、第三方 Python 包或运行时依赖。这是独立实现的工作流，不能声称安装或执行了 UnityLanhuImporter。

正文维护在 LibraryG 共享技能库；设备发现目录可链接到这里。项目只保存任务清单、设计快照与验证产物。脚本路径相对本 SKILL.md，项目数据使用项目相对路径，设备路径作为命令参数传入。

## 实现顺序建议

1. **Step1 → 确认输入与基线。** 读取项目规则和当前 Git 状态，保存修改前 Prefab；尊重已有授权，不重复请求许可。记录设计页 URL/image_id、画板版本、尺寸、图层 ID、手动切图来源和倍率。同名页面可能不同版本。缺少原始标注只能做明确记录的适配，不能声称像素级还原；不能把截图坐标猜成原始数据。
2. **Step2 → 追踪业务与布局。** 阅读实际加载路径、生成绑定、动态文本、按钮、Slider、头像落点、动画、LayoutGroup、ContentSizeFitter、安全区和容器锚点。枚举完整业务界面与设计稿对应关系；区分弹窗、主界面气泡和画板备注。动态示例值不能写死；发现设计和玩法冲突时继续独立工作，针对冲突请求用户选择。
3. **Step3 → 导入与显式映射。** 按 `references/manifest.md` 建资源和节点清单。原样复制批准的 PNG，校验原生像素尺寸，配置单图 Sprite 和九宫边界；复用项目资源前核对 GUID。父节点映射先于子节点。同时校正依附的点击区、头像落点和奖励容器，记录所有设计适配。不要让正式资产依赖 Editor 验证资源。
4. **Step4 → 预演后应用。** 用 `plan` 检查全批次，阅读差异。先对代表性界面应用并回读，再处理同类界面。已有实施授权时直接 `apply`。计划后任何输入变化会拒绝写入；重新检查当前差异并预演，不绕过检查。备份和报告放项目明确忽略的持久目录，不只放 Unity 会清理的 Temp。
5. **Step5 → 验证。** 执行 `verify`，重新解析文件投影到画板坐标；重复 `plan` 应字节不变。核对原 ID、层级、脚本、事件、本地化、动态文字及未映射字段保留。工具变更运行 `scripts/test_lanhu_unity.py`。若改 C#，遵守项目受控编译流程。静态通过后必须另查 Unity 导入、Prefab 实际显示、动画结束态、交互、多分辨率和安全区；没有运行工具时明确记为待验，不用静态拼图冒充截图。
6. **Step6 → 交付。** 逐界面写明已接入、设计缺口、字体替代、手工适配、静态结果和运行验证边界，附复现/回滚命令。遵循项目既有文档与知识库路由，不自动 Git 暂存、提交或发布。

## 使用工具

命令中的 `$LANHU_SKILL` 是当前设备本技能目录，`$PROJECT` 是项目目录。

```bash
python3 "$LANHU_SKILL/scripts/lanhu_unity.py" inspect-board --input board.json
python3 "$LANHU_SKILL/scripts/lanhu_unity.py" inspect-prefab --input panel.prefab --size 1080 2340
python3 "$LANHU_SKILL/scripts/import_sprites.py" --project "$PROJECT" --source-root "$DOWNLOADS" --manifest imports.json --report imports-report.json
python3 "$LANHU_SKILL/scripts/lanhu_unity.py" plan --project "$PROJECT" --manifest mapping.json --report report-directory
python3 "$LANHU_SKILL/scripts/lanhu_unity.py" apply --project "$PROJECT" --report report-directory
python3 "$LANHU_SKILL/scripts/lanhu_unity.py" verify --project "$PROJECT" --report report-directory
python3 "$LANHU_SKILL/scripts/lanhu_unity.py" rollback --project "$PROJECT" --report report-directory
```

运行 `plan` 时 manifest 必须位于项目内。每次预演使用新报告目录。`apply` 检查 manifest、源标注、原资产、嵌套源和图片/meta 哈希，保存原文件后逐文件写入；多文件写入不是原子事务。若中途失败，检查实际写入范围；`rollback` 接受原文件或本次输出，遇到后续手改即拒绝。

## 能力边界

- 支持 Unity 文本 Prefab、未旋转的正缩放 RectTransform、拉伸锚点、pivot、显式单层嵌套实例中的直接节点。变更嵌套实例覆盖，不改共享源 Prefab。
- 深层实例、Variant、旋转、负缩放、无法解析的父级以及布局/动画驱动的目标需用 Unity API 或单独适配；不能通过放松检查猜算。未映射的深层实例和旧覆盖按原字节保留。
- 顶层根节点尺寸由 `referenceSize` 定义。画板中心裁切和设备缩放分别处理；例如 1700 宽画板映射到 1080 宽槽位若采用原比例裁切，x 偏移为 -310，尺寸不缩放。切图 @3x 不必然要再除以 3。
- 不新增/删除/改名 GameObject，不改现有 GUID/fileID、脚本、业务事件、Raycast、动态文案或语言键。仅映射明确列出的矩形、经确认的锚点/pivot、单图 Sprite、视觉样式；可显式关闭旧 Image 或调整 Graphic alpha，但必须写原因并确认它不是交互所依赖的可见性状态。
- 文字保留项目字体时，文字框与 glyph bounds 不是同一口径。需记录字形、行高、描边、宽度和旋转差异；自动缩小不构成字体还原。
- 不收集浏览器 Cookie、Token 或密码；使用已授权且可用的浏览器/连接器读取，或用户提供的原始导出与切图。
