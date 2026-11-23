# Prop Favor 报告原始素材候选

这六张图片为 TF 2.12.0 包体 Sprite 原样导出（UnityPy 解析图集切片），不是生成图、不是完整界面截图。`source-manifest.json` 记录 bundle、序列化文件、path ID、SHA-256 和尺寸。道具图标依据资源名定位，尚未逐一证明当前 Prop Favor Prefab 的动态资产映射；蓝色背景仅为通用 banner 背景候选，不能当 Prop Favor 确认背景。报告如采用，须保留这层边界。

## 2026-11-18 资源拼装补充

新增 `prop-favor-detail.png` 抓钩详图、`prop-favor-overview.png` 五类同价位对照、`prop-favor-claw-799.png` 透明底纯礼包。包体原图确定性拼装，不是实机截图。已恢复 IAPBannerCell105 → ArtIAPNormalNewCellPrefab → r_six 引用和相对位置；底板、按钮、角标、金币原图在 `composite-parts/`，来源和SHA-256见该目录manifest。道具使用上方商店版本候选，未验证动态图映射。字体、局部网格和材质效果为近似。价格沿用11月4日历史配置，奖励分项和总计已核对。

复现脚本：`06-PRODUCT-ASSETS/TileFamily/2.12.0/04-ReverseEngineering/prop-favor-compose.py`。布局来源及五类数据随附 `composite-layout-evidence.json`。
