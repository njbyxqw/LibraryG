# TS 道具礼包设计附件

本目录为2026-11-18功能与美术设计附件。`Item_11.png`、`Item_12.png`、`Item_13.png`、`Item_14.png`直接复制TS当前本机`Assets/Game/TileV2/Res/Game/Texture/TileUI/Common/`资源，分别为撤回、风车、磁铁、手套。来源、文件摘要、关键代码行号见`source-evidence.json`。

图标用于设计文档里的可切换Banner结构示意。共用底板、购买按钮和货币符号为HTML结构占位，不是正式美术交付；A档数量沿用TF迁移讨论稿，购买货币及售价待定。HTML已内嵌四张图，无远程脚本、字体或图像依赖。

设计主档为`../../方案-强需求道具礼包功能与美术设计.md`；阅读版为`../../TS_Prop_Offer_Design.html`。`build_design.py`记录本机导出方法，依赖先将正式Markdown去frontmatter、展开wikilink标签，再用PowerShell `ConvertFrom-Markdown`导出`D:/workspace/ts-prop-offer-fragment.html`；后续修订以正式Markdown为准，勿只改HTML。代码与图片来源根目录按当前设备适配。

核验边界：完成文件存在性、引用、源摘要、内嵌资源和四类奖励数据一致性检查；TS道具原图已查看。未在浏览器做页面渲染验收，未在Unity验证商店排版或支付流程。
