---
title: Toy Story Drop Collection 内容拆解（1.20.0 / 737）
date: 2026-11-09
type: analysis
status: current
tags: [产品分析, Toy Story Drop, Collection, 收集系统]
---

# Toy Story Drop Collection 内容拆解（1.20.0 / 737）

## 样本与结论边界

- 来源：Windows MuMu「产品分析」实例 1，Android 用户 0，包名 `com.bigfishgames.toystorydropgoog`，设备安装版本 `1.20.0 (737)`。安装包 SHA-256：`df7e7f75db490e8fae83edf513855a50f1340a5547a8ed8f491dff41d8678fcd`。
- 工具：REA `inspect_android_package`、`inspect_managed_artifact`、`inspect_managed_members`；APK 中的 `SpaceRanger.dll` 是 Mono/CIL 游戏逻辑。`SpaceRanger.dll` SHA-256：`4a675ad898f46221e36510df396ecce9434dc51116e75e3553858629eb288586`，MVID `10f3520a-23c5-4856-bf91-fb32c37b79c1`。
- 证据状态：下表是**该 APK 内置定义**，不是该账号已解锁或已显示的清单。2026-11-09 运行时游戏产生内存不足崩溃（约 192 MB Java heap 上限），尚未取得 Collection 实拍或账号进度；应用目录中未发现单独名为 `Collection` 的文件。

## Collection 的四个页签

`Match.CollectionDialog` 引用 `Shell/Collection`，构造四个书签，并通过 `SelectBookmark` 切换。四页签分别由独立的 Bookmark 类填充：

| 页签 | 代码入口 | 内容与状态来源 |
|---|---|---|
| Playsets（套组） | `Match.Collection.PlaysetCollectionBookmark` | `Match.Playsets` 静态套组配置；按解锁、完成、新物件状态展示。 |
| Art Gallery（画廊） | `Match.Collection.GalleryCollectionBookmark` | 遍历 `Location.get_Locations`，筛选并排序地点，按拼图地点与玩家完成进度设置图片槽；需要时下载画廊 Bundle。具体可见图片依账号进度和下载状态而变。 |
| Inventory（物品） | `Match.Collection.InventoryCollectionBookmark` | `Match.Collection.Inventory.GetItems` 从碎片类型生成条目，槽位显示当前数量与合成容量；页面字面标题为 `Your Items`。 |
| Achievements（成就） | `Match.AchievementsCollectionBookmark` | `Match.Achievement.List` 与 `AchievementsData` 的累计值、已查看值、当前阶级；支持升级与领取对应阶段奖励。页面字面标题为 `Deeds`。 |

代码锚点：`CollectionDialog` 类型 `0x020000c8`；构造方法 `0x060009bb`、切换方法 `0x060009bc`。REA 证据 `ev_3a77589256a569e1e9cc1a8092edce6de53d16811cb7852706a14342854625f4`。

## Playsets：14 组，59 个部件

下列是 `Match.Playsets..cctor`（方法 `0x06000a02`）按顺序初始化的内置套组及物件名称。`[]` 是代码中本地化调用使用的字符串前缀，表中已去掉；英文保留 APK 原值。是否可见、是否拥有取决于玩家状态。

| 顺序 / 资源 ID | 套组名称 | 部件 |
|---|---|---|
| 01 `01Woody` | Sheriff Woody | Wagon；Sheriff；Bank |
| 02 `02Buzz` | Space Ranger Buzz | Ship；Star Command HQ；Sign |
| 03 `03Jessie` | Cowgirl Jessie | House；Train Depot；Train |
| 04 `04Forky` | Sir Forky | Witch Hut；Potion；Castle |
| 05 `05Trixie` | Archaeologist Trixie | Treasure Map；Explorer's Cap；Tree with Axe；Treasure Chest；Cake |
| 06 `06DuckyBunny` | Ducky and Bunny | Spy Guy Sunglasses and Hats；Combat Carl's firecrackers；Mt. Caboom；Duke Caboom's CA-BOOM TENT；Duke's Motorcycle Ramp |
| 07 `07Potatoheads` | Potatoheads | Dinosaur Statue；Mrs. Potato Head Wanted Poster；Jessie's Telescope；Rex's Disguise；Hamm's Cork/Hamm's Money |
| 08 `08Rex` | Big City Rex | King Pigg's crown；Army Truck；Dinosaur Egg；Water Tower；Business Corporation logo |
| 09 `09BoPeep` | Queen of the Pirates | Duke Caboom's Cannons；Bo's Pirate Flag；Bo's Ship；Alien Net |
| 10 `10Zurg` | The Planet Trap | Zurg's Eternal Power Source；One-Eyed Bart's Catapult；Combat Carl's Laser Generator |
| 11 `11Giggle` | Giggle McDimples | Sheep's Masks；Police Tape；Fire Hydrant；Cage；Money Bag |
| 12 `12CombatCarl` | Last Resort | Carl's Combat Vest；Trixie's Dino Computer；Ray-Gon's machine |
| 13 `13MrShark` | King of the Sea | Conch Shell；Coral Reef；Small Screen for Radar；Snorkel and Fins；Trident；Crown |
| 14 `14TheNewSheriff` | The New Sheriff | Sheriff Star；Teacup；Dinosaur Hat；Produce Cart；Pumpkin；Present |

套组字段有 `FolderName`、`Items`、`Tint`、`BonusChapter`；代码另外计算 `UnlockedItems`、`ItemsInUnlockOrder`、`NewItems`、`IsCompleted`、`IsCompletedAndSeen`、`IsAvailableForPlayer`。因此“包内有 14 组”不能推成当前账号全部可用。REA 证据 `ev_3a77589256a569e1e9cc1a8092edce6de53d16811cb7852706a14342854625f4`；静态初始化字符串与顺序来自方法 `0x06000a02`。

## Art Gallery 与 Inventory

**画廊：** `GalleryCollectionBookmark.UpdateContent` 从地点集合筛选、排序并创建画框；`SetupPuzzleSlot` 使用地点文件夹名形成图片路径，区分 Bundle 是否已附加、地点是否为活动地点、玩家是否完成。图片详情页 `GalleryPictureDialog` 支持前后切图，资源路径字面值为 `Shell/Gallery/Pics/`。当前尚未解出该账号的已完成地点，因此无法确定实机画廊的具体张数与内容。锚点：`UpdateContent` `0x060013ce`、`SetupPuzzleSlot` `0x060013d1`、`GalleryPictureDialog`；REA 证据 `ev_3210966a13420b4c15be0bf7bf8f98ccc6a34a971a98ddac0893f00b0e90432d`。

**物品：** `Match.ShardType` 的八类碎片与 `InventoryItem.GetName` 的页面名称按枚举值对应：

| 碎片枚举 | 页面名称 |
|---|---|
| `LifeRefillShard` | `Life` |
| `InfiniteLifeShard` | `InfiniteLife` |
| `EnergyShard` | `Toys` |
| `LightningShard` | `DiscoBall` |
| `KitesShard` | `Kites` |
| `ShovelShard` | `Saucer` |
| `WindShard` | `Claw` |
| `ShuffleShard` | `Etch` |

条目是否出现还经过解锁筛选；碎片数量与容量从 `Match.Shards` 及进度状态读取。页面另有无限生命碎片提示：收集碎片可解锁限时无限生命。锚点：`Inventory.GetItems` `0x060013f9`、`InventoryItem.GetName` `0x060013f8`；REA 证据 `ev_3210966a13420b4c15be0bf7bf8f98ccc6a34a971a98ddac0893f00b0e90432d`。

## Achievements：16 项

`Achievement..cctor`（`0x060000a9`）内置 16 个成就标识：`StepByStep`、`NeedEnergy`、`FireworksMaster`、`SurpriseMe`、`BigBounce`、`EverybodyDance`、`FullSet`、`WatchYourStep`、`PopIt`、`MarbleBalls`、`SpaceFleet`、`Sticky`、`HugeNumbers`、`BigBang`、`TreasureHunter`、`TappingIn`。`AchievementsData` 保存关卡胜利、金币、电池、套组完成、各类特殊块触发/消除、总分、礼盒、地图动效等累计量，以及已查看值和当前阶级。每个 `Achievement` 有第 1、2、3 阶目标和奖励读取器；实际达成与奖励数量尚未核对。REA 证据 `ev_3210966a13420b4c15be0bf7bf8f98ccc6a34a971a98ddac0893f00b0e90432d`。

## 待验证

- 游戏运行时崩溃：设备文件 `.../Crash/crash_2026-11-09_14-21.txt` 报 Java heap OOM；前台回到启动器。需要恢复可运行状态后实拍 Collection，并核对当前账号的四个页签、已解锁套组、画廊图片和物品数量。
- 画廊候选和成就各阶具体目标/奖励尚未逐项解码；本报告只回答当前 APK 的 Collection 内容结构与内置清单。

## 关联

- [[02-PROJECTS/产品分析/_MOC|产品分析 MOC]]
- [[02-PROJECTS/产品分析/Toy Story Drop/资源路径索引|资源路径索引]]
