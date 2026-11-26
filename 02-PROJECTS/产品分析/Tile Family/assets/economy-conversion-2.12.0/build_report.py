from pathlib import Path
from fractions import Fraction as F
import csv, json, hashlib, html

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').exists())
BASE = ROOT / '06-PRODUCT-ASSETS/TileFamily/2.12.0/05-Runtime/2026-11-04/decoded/initial-config/Config'
OUT = HERE.parent.parent / '游戏逻辑'
TITLE = '经济换算-金币道具与美元系数-2.12.0'
def read(name):
    with (BASE / name).open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    return [dict(zip(rows[0], row), _csv_record=i+1) for i, row in enumerate(rows) if i >= 3 and row and row[0]]
files = ['config_server_iap.csv','config_server_coin.csv','config_server_asset.csv','config_server_shop.csv','config_server_game.csv']
data = {n: read(n) for n in files}
iap = data[files[0]]
coin = data[files[1]]
assets = {r['AssetId']: r for r in data[files[2]]}
shops = {r['GroupId']: r for r in data[files[3]]}
game = {r['Key']:r for r in data[files[4]]}
def rewards(r):
    return [(a, F(n)) for a,n in (s.split('_') for s in r['AssetList'].split(';') if s)]
def total(r):
    d = {}
    for a,n in rewards(r): d[a] = d.get(a,F(0)) + n
    return d
names = {'100':'金币','200':'体力','300':'无限体力（分钟）','502':'撤回','503':'磁铁','506':'抓钩','508':'局内加一','515':'洗牌','708':'无限加一（分钟）','510':'复活效果510','404':'剧情返场券'}
unit = {rewards(r)[0][0]:F(r['BuyPrice'])/rewards(r)[0][1] for r in coin if r['CoinProductId'] != 'coreplay_retry_buy_extra_space'}
unit['100'] = F(1)
dda = {a:F(r['DDAAssetValue'] or '0') for a,r in assets.items()}
def fmt(n, digits=2): return f'{float(n):,.{digits}f}'
def num(n): return str(int(n)) if n.denominator == 1 else fmt(n)
def val(r, weights): return sum((n*weights.get(a,0) for a,n in rewards(r)),F(0))
def table(headers, rows):
    md.extend(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|'] + ['| '+' | '.join(map(str,row))+' |' for row in rows] + [''])
    web.append('<div class="table"><table><thead><tr>'+''.join('<th>'+html.escape(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>')
def heading(t): md.extend(['## '+t,'']); web.append('<h2>'+html.escape(t)+'</h2>')
def para(t): md.extend([t,'']); web.append('<p>'+html.escape(t)+'</p>')
md = ['---',f'title: {TITLE}','date: 2026-11-24','type: research','status: current','tags: [TileFamily, 经济系统, 道具礼包, 定价]','---','', '# TF：金币、道具与美元的换算系数','']
web = ['<h1>TF：金币、道具与美元的换算系数</h1>']
para('结论：可以建立“金币直购 → 道具金币价格 → 礼包等值”的换算链，但没有一套跨档位、跨礼包通用的固定美元汇率。金币直购约为每美元 502.51–1,000.10 金币；道具零售价格约为 DDAAssetValue 的 2.11–2.17 倍；Prop Favor 多数档位约含每美元 1,450–1,500 金币零售等值。')
para('证据范围：TF 2.12.0，2026-11-04 initial-config 快照；整理日期 2026-11-24。以下价格为 config_server_iap.BuyPrice（字段注明美元），不是当前账号实时支付报价。截图 EUR 8.99 仅证明当时当地展示价，不能直接当成 USD 8.99，也不能用外汇换算替代商店地区定价。Switch=1 仅表示配置总开关开启，不证明所有账号当前可见。')
heading('1. 换算口径与公式')
table(['口径','计算方法','用途与限制'],[
 ['金币直购','金币数量 ÷ 美元价格；反向为美元价格 ÷ 金币数量','客观付费锚点；必须带充值档位'],
 ['道具金币零售价','金币购买价格 ÷ 道具数量','三件包均摊单位价，不表示支持单件购买'],
 ['DDA 权重','直接读取资产表 DDAAssetValue','内部配置权重；金币=1；不是玩家兑换价，不推定所有业务均使用它'],
 ['礼包金币零售等值 V','金币 + Σ（道具实际总数量 × 道具金币零售价）','统一比较礼包中可定价奖励；未定价奖励单列'],
 ['礼包折算系数 K','V ÷ 礼包美元价格','每美元获得的金币零售等值'],
 ['礼包内按权重分摊美元','单件道具金币零售价 ÷ K；每金币=1/K 美元','分析用成本分摊，不是独立道具的官方美元售价']])
heading('2. 纯金币充值：六档美元系数')
pure = sorted([r for r in iap if r['ProductId'].startswith('com.coin.pack.')],key=lambda r:F(r['BuyPrice']))
assert len(pure)==6
table(['商品','美元价','金币','金币 / $1','$ / 1,000 金币'],[[r['ProductId'].replace('com.coin.pack.',''), '$'+r['BuyPrice'],num(total(r)['100']),fmt(total(r)['100']/F(r['BuyPrice'])),fmt(F(r['BuyPrice'])/total(r)['100']*1000,4)] for r in pure])
rates = [F(r['BuyPrice'])/total(r)['100'] for r in pure]
low, high = min(rates),max(rates)
para('六个金币商品的对应组均为 Switch=1。U0/U1/U2 商城模板中可见这六组，RecommendType=3，作为价格锚点使用。最低单位成本来自 $99.99 档，最高来自 $1.99 档；“$1≈1,000 金币”只能当大额充值档附近的分析基准，不能覆盖全部用户。')
heading('3. 核心道具：金币系数、内部权重与美元等值')
core = ['502','506','515','503','508']
table(['道具 / 资产ID','金币购买配置','金币 / 件','DDA / 件','零售价 ÷ DDA','美元 / 件：六档充值区间'],[[names[a]+' / '+a, f'{num(unit[a]*3)} 金币 / 3件',fmt(unit[a]),fmt(dda[a],0),fmt(unit[a]/dda[a],3),f'${fmt(unit[a]*low,4)}–${fmt(unit[a]*high,4)}'] for a in core])
para('美元区间是假设金币全部通过纯金币包购得后的单位成本均摊；不包含免费获得的金币，也不代表从零金币开始购买该道具的最低即时支付金额。金币充值是离散档位，可能产生余额。例如三件磁铁需要3,900金币，按Small档均摊成本为$6.2322，但实际一次购买Small金币包需支付$7.99，剩余1,100金币。')
table(['道具 / 件']+['$'+r['BuyPrice']+'充值档' for r in pure],[[names[a]]+[fmt(unit[a]*q,4) for q in rates] for a in core])
para('道具相对价值：金币零售价为撤回 : 抓钩/洗牌 : 磁铁/加一 = 19 : 29 : 39，约为 1 : 1.526 : 2.053；DDA 权重为 300 : 450 : 600，即 1 : 1.5 : 2。两套体系的相对高低接近，但不能把DDA的300直接写成撤回的金币售价。')
heading('4. Prop Favor：保留“主道具 + 金币 + 赠品”的逐档拆分')
para('四种赠品固定指撤回502、抓钩506、洗牌515、磁铁503。主道具与赠品分开显示；计算总价值时将两处奖励都计入一次。例如磁铁主奖励×3，赠品中另有磁铁×1，实际到账磁铁共4个。')
props = [r for r in iap if r['GroupId'] in ['prop_favor_undo','prop_favor_propeller','prop_favor_shuffle','prop_favor_magneto','prop_favor_space']]
props.sort(key=lambda r:(core.index(rewards(r)[0][0]), F(r['BuyPrice'])))
assert len(props)==20 and all(shops[r['GroupId']]['Switch']=='1' for r in props)
prop_rows=[]
for r in props:
    rr=rewards(r); a,n=rr[0]; price=F(r['BuyPrice']); v=val(r,unit); d=val(r,dda)
    assert len(rr)==6 and [x[0] for x in rr[2:]]==['502','506','515','503']
    assert len(set(x[1] for x in rr[2:]))==1
    prop_rows.append([names[a], '$'+r['BuyPrice'], num(n),num(rr[1][1]),'四种各'+num(rr[2][1]),fmt(v),fmt(v/price),fmt(d),fmt(d/price)])
table(['目标道具','美元价','主道具数','金币','另赠道具','金币零售等值 V','金币等值 / $','DDA 合计','DDA / $'],prop_rows)
para('结果：20个候选中，撤回$7.99档的金币零售等值/$为1,693.78，明显高于其他档；其余19个候选约为1,447.27–1,503.72。DDA口径全体约为923.79–957.74/$，同价位奖励总权重接近。这支持“先按相对权重配平、再结合整数数量调整”的解释，但尚不能证明TF实际使用了某个固定美元公式自动生成礼包。')
heading('5. 礼包里的单件道具，如何分摊为美元')
example = next(r for r in props if r['ProductId']=='com.magneto.favor.03.bundle')
v=val(example,unit); price=F(example['BuyPrice']); k=v/price
para('示例采用配置中的磁铁$7.99档：主磁铁×3 + 金币4,000 + 撤回/抓钩/洗牌/磁铁各×1。金币零售等值=4,000 + 3×1,300 +（633.333…+966.666…+966.666…+1,300）=11,766.666…；每美元=1,472.674…金币等值。')
table(['奖励项','数量','金币等值小计','按零售价权重分摊美元'],[[names[a]+('（主3+赠1）' if a=='503' else ''),num(n),fmt(n*unit[a]),'$'+fmt(n*unit[a]/k,4)] for a,n in total(example).items()])
table(['单位资源','此磁铁$7.99礼包内的分摊美元','Prop Favor 全20候选的分摊美元区间'],[[names[a]+'×1','$'+fmt(unit[a]/k,6 if a=='100' else 4),f'${fmt(min(unit[a]*F(r["BuyPrice"])/val(r,unit) for r in props),6 if a=="100" else 4)}–${fmt(max(unit[a]*F(r["BuyPrice"])/val(r,unit) for r in props),6 if a=="100" else 4)}'] for a in ['100']+core])
para('上述区间是在相同权重下对各礼包进行成本分摊；即使某个礼包不含局内加一，也可以得到其同权重参考值，但不代表该礼包实际出售加一道具。小计计算保留精度，表格展示四舍五入，展示值相加可能有尾差。赠品属于礼包已包含奖励，不因UI称“赠送”就从礼包价值中删除。')
para('不能用“美元总价减金币零售价减赠品零售价，余额就是主道具价格”的方法。若用Small金币包的单价算磁铁$7.99礼包，4,000金币=$6.392、赠品四件约$6.1789，两者已超过礼包价格，倒算主磁铁会得到负数。原因是礼包整体促销，而非主道具有负价值。')
heading('6. 其他商城礼包：统一权重后的比较')
regular=['beginner_bundle','big_bundle','super_bundle','mega_bundle','giant_bundle','champion_bundle']
def bundle_rows(rows):
    out=[]
    for r in rows:
        t=total(r);p=F(r['BuyPrice']);fixed=[t.get(a,F(0)) for a in ['502','506','515','503']]
        gift='四种各'+num(fixed[0]) if len(set(fixed))==1 else '/'.join(num(x) for x in fixed)
        excluded='；'.join(names.get(a,assets.get(a,{}).get('Name',a))+'×'+num(n) for a,n in rewards(r) if a not in unit) or '无'
        out.append([r['ProductId'],'$'+r['BuyPrice'],num(t.get('100',F(0))),gift,excluded,fmt(val(r,unit)/p),fmt(val(r,dda)/p),shops.get(r['GroupId'],{}).get('Switch','无组记录')])
    return out
headers=['商品ID','美元价','金币','常规道具','未计价奖励','金币等值 / $','DDA / $','组开关']
table(headers,bundle_rows([r for g in regular for r in iap if r['GroupId']==g]))
para('上表无限体力与无限加一均按分钟标注，未纳入金币等值，因此只能比较“金币+可定价常规道具”这一部分，不能据此认定整个礼包的全部价值或性价比排名。新手礼包配置LT限购1次，不应当作长期充值汇率。')
table(headers,bundle_rows(sorted([r for r in iap if r['GroupId'].endswith('_bundle_disguise')],key=lambda r:F(r['BuyPrice']))))
para('disguise组是另一组商城配置：同美元价下金币/道具/限时奖励均可能不同。虽然总开关为1，但所检查的U0/U1/U2商城模板未直接列出这些组；不认定它们与常规包同时对所有账号售卖。')
others=[r for r in iap if r['GroupId'] in ['special_deal','newbie_special_offer','no_payment_bundle','weekend_deal','tile_favor']]
table(headers,bundle_rows(sorted(others,key=lambda r:(r['GroupId'],F(r['BuyPrice'])))))
para('上表仅计算AssetList明确列出的基础奖励，不因buy_one_get_one_free界面类型而擅自翻倍。Tile Favor中的510是复活效果，不能按508局内加一道具定价。special_deal组Switch=0，而weekend_deal组Switch=1，两者是不同组；复核发现旧报告将Weekend Deal误记为关闭，已同步更正，组开关仍不等于实际展示资格。')
heading('7. 其他货币、体力和特殊道具：能算到哪一步')
pen=next(r for r in iap if r['ProductId']=='com.story.activity.item.bundle')
table(['资源','可证实的配置','金币转换系数','美元转换系数 / 边界'],[
 ['普通体力200','上限5；补满900金币；自然恢复30分钟/点','从0补至5时=180金币/点','按充值档位均摊=$0.1800–0.3582/点；补满共$0.8999–1.7910'],
 ['普通体力DDA','DDAAssetValue=100','内部权重100，非180金币实际均摊价','不能直接称$0.10/点'],
 ['Merge能量15014','买30能量；金币消耗配置300/600/900；购买开关F','配置隐含10/20/30金币/能量','对应$0.0100–0.0199 / $0.0200–0.0398 / $0.0300–0.0597；开关关闭，非已开放汇率'],
 ['回忆铅笔/剧情返场券404',pen['ProductId']+'；组开关'+shops[pen['GroupId']]['Switch'],'未见金币直购价','$2.99/张；其DDA为0也不代表免费'],
 ['无限体力300、无限加一708','分钟型奖励；常见于混合礼包','无法从当前证据唯一拆出金币/分钟','不把30分钟当30个道具；不按恢复速度直接折算'],
 ['剧情星401、骰子402、活动票券/代币等','资产或混合礼包记录','本次未建立独立兑换路径','礼包总价除该货币数量只是假设全部成本由它承担，非独立售价'],
 ['卡包1001/1002/1003及其他随机奖励','资产定义；概率、内容效用另有机制','本次不设统一金币系数','需概率、卡池与重复收益才能讨论期望值'],
 ['复活效果510、限时增益、活动能量等','用途与生命周期各异；部分DDA=0','本次不跨系统强行映射','DDA=0仅为该字段未赋正权重，不等于没有经济价值']])
para('体力180金币/点只适用于缺5点时补满；若同一900金币费用也允许缺m点时补满，则每点为900/m，实际按钮资格与扣费流程未在本次重追。Merge能量只记录静态三段配置，不推断档位递增、刷新周期及实际开放条件。')
heading('8. 同名/特殊场景道具不能混用系数')
table(['金币商品ID','资产ID','配置购买量','金币价','金币/件','说明'],[[r['CoinProductId'],rewards(r)[0][0],num(rewards(r)[0][1]),r['BuyPrice'],fmt(F(r['BuyPrice'])/rewards(r)[0][1]),'复活场景单件价' if 'retry' in r['CoinProductId'] else ('本报告核心旧道具' if rewards(r)[0][0] in core else '独立ID；仅证明配置存在')] for r in coin])
para('特别注意：旧洗牌515为2,900金币/3件，new_shuffle 519为1,900金币/3件；不能只按中文名称合并。局内加一508普通购买为3,900/3件，retry场景为1,170/件；两种情境分别保留。505的解锁配置为100000，603标注废弃，其他前置增益是否可见仍需按版本与入口验证。')
heading('9. 对TS后续定价的可用结论（分析建议，未定案）')
para('最可借鉴的是“相对价值 + 场景折扣”两层设计：先用TS自己的金币直购价确定各道具相对价值，再以具体金币充值档位建立美元锚点，最后给强需求礼包单独配置整体折算系数。TF的相对权重约1:1.5:2可作对照，但TS道具实际效果、直购价不同，不直接照搬TF的633/967/1300金币。')
para('若需要一张内部简化估值表，可以明确选择某一金币充值档位作为基准，再计算美元值；若选“1,000金币等值=$1”，得到撤回约$0.633、抓钩/洗牌约$0.967、磁铁/加一约$1.300，属于分析假设。若改用DDA权重并假设“1,000 DDA单位=$1”，对应$0.30/$0.45/$0.60，是另一套模型，不能混称TF官方售价。')
heading('10. 来源、复算与验证边界')
para('主要来源：'+str(BASE.relative_to(ROOT)).replace('\\','/')+'。config_server_coin提供金币购买价；iap提供美元价格与有序奖励列表；asset提供ID/类型/DDA；shop提供组开关；game提供体力与能量参数。审计JSON保留原始记录、奖励顺序、聚合数量、未计价资产及源文件SHA-256。')
para('外部价格交叉检查：2026-11-24读取美国App Store官方页，公开内购列表仍列Mini Coin Pack $1.99、Small Coin Pack $7.99、Big Bundle $9.99、Super Bundle $19.99、Prop Favor 02 $12.99。该页不提供对应奖励数量；只能辅助核价，不能用它把11月4日快照升级为当前线上配置。https://apps.apple.com/us/app/tile-family-match-puzzle-game/id6444056676')
para('复算：运行本报告附件目录的build_report.py，仅使用Python标准库。所有中间计算使用Fraction；展示时四舍五入。原始奖励结构保留“主道具+金币+赠品”；20个Prop Favor候选均检查组开关、四种赠品、数量一致性，并核对分摊成本之和等于礼包价格。')
md += ['原始专题：[[02-PROJECTS/产品分析/Tile Family/游戏逻辑/Prop Favor-道具礼包奖励定价与触发-2.12.0]]。','', '审计数据：[[02-PROJECTS/产品分析/Tile Family/assets/economy-conversion-2.12.0/coefficients.json]]。','']
for r in props:
    v=val(r,unit)
    assert sum((n*unit[a]/v*F(r['BuyPrice']) for a,n in rewards(r)),F(0))==F(r['BuyPrice'])
assert val(example,unit)==F(35300,3)
assert unit['515']==F(2900,3) and unit['519']==F(1900,3)
assert [int(total(r)['100']) for r in pure]==[1000,5000,10000,25000,50000,100000]
def serial(x):
    if isinstance(x,F): return {'exact':str(x),'decimal':float(x)}
    raise TypeError(type(x).__name__)
audit={'snapshot':'2026-11-04','version':'2.12.0','generated':'2026-11-24','scope':'historical_config_not_live_prices',
 'sources':{n:{'path':str((BASE/n).relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256((BASE/n).read_bytes()).hexdigest()} for n in files},
 'coin_products':coin,'asset_definitions':list(assets.values()),'shop_groups':list(shops.values()),
 'game_parameters':{k:game[k] for k in ['life_max_count','life_refill_coin_count','life_recover_minute','order_merge_coin_buy_energy_need_coin','order_merge_coin_buy_energy_amount','order_merge_coin_buy_energy_switch']},
 'retail_coin_unit_values':unit,'iap_calculations':[]}
for n in ['config_client_shop_u0_0.csv','config_client_shop_u1_0.csv','config_client_shop_u2_0.csv']:
    audit['sources'][n]={'path':str((BASE/n).relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256((BASE/n).read_bytes()).hexdigest()}
for r in iap:
    if r['GroupId']=='not_in_use': continue
    p=F(r['BuyPrice'])
    audit['iap_calculations'].append({'source':r,'ordered_rewards':rewards(r),'aggregated_rewards':total(r),'retail_coin_value_known_subset':val(r,unit),'dda_value':val(r,dda),'coin_equiv_per_usd':val(r,unit)/p if p else None,'unpriced_assets':[a for a,n in rewards(r) if a not in unit]})
OUT.mkdir(exist_ok=True)
(OUT/(TITLE+'.md')).write_text('\n'.join(md),encoding='utf-8')
(HERE/'coefficients.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2,default=serial),encoding='utf-8')
style='body{font:16px/1.75 system-ui,sans-serif;color:#243548;background:#f3f5f8;margin:0}main{max-width:1400px;margin:auto;padding:32px}h1{font-size:30px}h2{margin-top:44px;border-top:1px solid #d8e0e8;padding-top:24px;font-size:22px}p{max-width:1100px}.table{overflow:auto;margin:20px 0;background:white;border-radius:10px;border:1px solid #dce3eb}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:11px 14px;border-bottom:1px solid #e5eaf0;text-align:left;min-width:85px}th{background:#e8eef6}tr:nth-child(even){background:#f8fafc}td:first-child{font-weight:600}footer{margin-top:32px;color:#657789}@media(max-width:650px){main{padding:16px}h1{font-size:24px}}@media print{body{background:white}main{padding:0}.table{overflow:visible}table{font-size:10px}td,th{min-width:0;padding:5px}}'
(OUT/'TileFamily_Economy_Conversion_2.12.0.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TF 金币、道具与美元换算</title><style>'+style+'</style><main>'+''.join(web)+'<footer>TF 2.12.0 · 历史配置 2026-11-04 · 整理 2026-11-24</footer></main></html>',encoding='utf-8')
print(json.dumps({'report':str(OUT/(TITLE+'.md')),'html':str(OUT/'TileFamily_Economy_Conversion_2.12.0.html'),'prop_favor_rows':len(props),'coin_packs':len(pure),'checks':'passed'},ensure_ascii=True))
