# 映射和资源清单

`lanhu_unity.py` 只读写显式选择的资源。不要直接在 YAML 中做全局字符串替换。

## 位置与嵌套映射

```json
{
  "version": 1,
  "boards": {"main": "Tools/Lanhu/Sources/main.json"},
  "prefabs": [{
    "path": "Assets/UI/Main.prefab",
    "referenceSize": [1080, 2340],
    "nestedPrefabs": [{
      "instance": 123456,
      "source": "Assets/UI/SharedTimer.prefab"
    }],
    "mappings": [{
      "target": "Main/Root/Title",
      "source": {"board": "main", "layer": 4785},
      "sourceOffset": [-310, 0],
      "sprite": "Assets/UI/Title.png",
      "style": {"m_Type": 0, "m_PreserveAspect": 0}
    }, {
      "target": "Main/Root/Timer/Text",
      "rect": [498, 350, 160, 56],
      "reason": "保留项目字体行高和实际时间宽度",
      "style": {"m_fontSize": 36, "m_enableAutoSizing": 1}
    }]
  }]
}
```

- `target` 包含根 GameObject 名，必须唯一。源图层 ID 必须存在且可见。隐藏图层只有提供 `allowHiddenReason` 才能使用。
- `rect` 是 `[左, 上, 宽, 高]`，单位为根画布参考像素，必须写 `reason`。当与 `source` 同时出现时，`rect` 覆盖源矩形，source 保留溯源作用；`sourceScale` 和 `sourceOffset` 会继续作用于显式 rect，通常不要混用。
- `sourceScale` 默认为 1；先缩放全部四值，再给 x/y 加 `sourceOffset`。
- `layout` 可显式指定 `m_AnchorMin`、`m_AnchorMax`、`m_Pivot` 两维数值（0～1），必须同时提供 reason 和目标矩形；先改变锚点再计算矩形。只用于已确认的适配策略。
- 先映射父级，再映射子级。最终整批坐标若被后续父级修改破坏，预演会拒绝。
- `nestedPrefabs` 要用实际 PrefabInstance fileID 和经 meta GUID 核验的源路径。只展开一层实例中的直接节点；更深层实例不展开，旧的无目标覆盖不清理。
- `imageEnabled: false` 仅改 Image 的启用位；`graphicAlpha: 0` 仅改当前 UI Graphic 颜色 alpha；两者必须提供 reason。原 GameObject、交互组件及业务状态不变，但仍需验证视觉行为。
- 字体样式白名单：`m_fontSize`、`m_fontSizeBase`、`m_fontSizeMin`、`m_fontSizeMax`、`m_enableAutoSizing`、`m_HorizontalAlignment`、`m_VerticalAlignment`、`m_characterSpacing`、`m_TextWrappingMode`。图片白名单：`m_Type`、`m_PreserveAspect`、`m_FillMethod`、`m_FillOrigin`、`m_PixelsPerUnitMultiplier`。

## 原样导入切图

```json
{
  "metaTemplate": "Assets/UI/ExistingSingleSprite.png.meta",
  "sprites": [{
    "source": "Export/title@3x.png",
    "target": "Assets/UI/Lanhu/Title.png",
    "pixels": [898, 282],
    "border": [0, 0, 0, 0]
  }]
}
```

`source` 相对命令的 `--source-root`，target 和模板相对项目。`border` 顺序为左、下、右、上，必须在原图范围内。只复制原始 PNG，不裁图/重绘。模板应由目标 Unity 项目生成，必须是单图 Sprite；现有目标文件若内容不同就拒绝覆盖。GUID 按目标路径稳定生成，只用于新资产，不能覆盖已有 GUID。目录 meta 自动创建，不替换现有目录 meta。

## 报告与恢复

报告包含 `plan.json`、`proposed/`、`diffs/`；应用后有 `before/` 和 `result.json`。文件哈希和未列出字段保留检查是写入前置条件。`verify` 只确认当前文件等于计划输出，不证明 Unity 编译、加载、运行或画面相同。

若需独立几何复核，重新读取实际 Prefab、展开同一实例，调用 `geometry()`，把左下角转换回左上角：`[lower.x, H-lower.y-height, width, height]`。不要只复用预演内存对象作为落盘证据。
