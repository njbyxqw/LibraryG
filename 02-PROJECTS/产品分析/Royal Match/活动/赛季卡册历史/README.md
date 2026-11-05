# 赛季卡册历史

维护对象为 Seasonal Card Collection，各季按 seasonId 索引，各轮另记。Grand Science 和 Grand Holiday 分别是对应季的后续轮次。2026-11-03 已在本机恢复两个相邻赛季的完整卡目录。

| 内部季号 | 正式标题 | 已取得的内容 |
|---|---|---|
| 15 | Science Collection / Grand Science Collection | 39781 实例 0 于 10-28 的外部存储备份，season15localization 的 Badge4028/4029EquipWarningText 明确给出两轮标题。season15section 提供 16 组配置。[144 张逐卡目录](season15-cards.json)。 |
| 16 | Holiday Collection / Grand Holiday Collection | 38911 实例 1 于 11-03 采集，Badge4030/4031EquipWarningText 确认两轮标题。[活动主档](../Holiday%20Collection/README.md)。 |

逐个比对 144 个 (setId, cardId)，两季每个位置的星级和卡种均一致。第 15 季组名按次序为 Dimensions、Memory、Optics、Earth、Exploration、Meteorology、Experiment、Botany、Computer、Mechanics、Research、Quantum、Momentum、Robotics、Cosmos、Discovery。第 1 组第 1 张为 Ruler，第 16 季相同位置为 Hoodie，均是一星银卡。此对位只覆盖这两个样本。恢复脚本位于产品资产 39781/05-Runtime/20261028-desktop-backup/recover_season15.py，只读 03-external-data.tar 两个目标资源。

## 更早的期次

[社区换卡历史总索引](https://www.reddit.com/r/RoyalMatchGame/comments/1f4kflm/central_hub_links_for_card_exchange_megathreads/) 记录 2024 年 Royal / Summer / Fall / Winter Collection，2025 年 Journey / Nature / Space / Hobby Collection，各主题下可回查当时的换卡记录。公开年份和主题已定位，暂不以排序推定内部 seasonId。

[Google Play 对 Space Collection 的介绍](https://play.google.com/store/apps/editorial?hl=en_US&id=mc_games_editorialevergreen_royal_match_all_about_collection_postinstall_fcp) 记载 18 套、每套 9 张、共 162 张；页面描述的规模不能直接当作已核实的首轮毕业数。

第 16 季本地化仍列有 4000～4031 共 32 个徽章名。4028 明称 Robot Badge，而对应卡册叫 Science Collection；因此将徽章名视作定位线索。其余旧期的主题、完整卡面、投注权重与投放配置需分别取证。
