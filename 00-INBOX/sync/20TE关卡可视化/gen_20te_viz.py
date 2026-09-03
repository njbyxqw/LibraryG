# -*- coding: utf-8 -*-
"""生成 20_TE 关卡可视化 HTML（坐标 + 碾压关系交互视图）"""
import json, io

data = open(r'D:/meatloaf_client01/local_py_script/_20te_data.txt', encoding='utf-8').read().strip()
d = json.loads(data)
tiles_new = d['new']

# 计算统计信息（碾压关系在 JS 里也会算，这里用于页头摘要）
def press_stats(ts):
    covers = []
    for i, b in enumerate(ts):
        c = [j for j, a in enumerate(ts)
             if a['z'] > b['z'] and abs(a['x'] - b['x']) <= 1 and abs(a['y'] - b['y']) <= 1]
        covers.append(c)
    return covers

cov = press_stats(tiles_new)
top_cnt = sum(1 for c in cov if not c)

html = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>20_TE 关卡可视化 - 坐标与碾压关系</title>
<style>
  :root{--bg:#14161c;--panel:#1e2129;--line:#2c303c;--txt:#d7dae2;--sub:#8b90a0;--acc:#4da3ff;}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--txt);font:14px/1.5 "Segoe UI",system-ui,sans-serif;padding:16px}
  h1{font-size:18px;margin-bottom:4px}
  .sub{color:var(--sub);font-size:12px;margin-bottom:12px}
  .toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:var(--panel);
    border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin-bottom:12px}
  .toolbar label{font-size:12px;color:var(--sub)}
  select,button{background:#262a35;color:var(--txt);border:1px solid var(--line);border-radius:6px;
    padding:4px 10px;font-size:13px;cursor:pointer}
  button.active{background:var(--acc);color:#fff;border-color:var(--acc)}
  .legend{display:flex;gap:8px;flex-wrap:wrap;margin-left:auto}
  .legend span{display:inline-flex;align-items:center;gap:4px;font-size:12px;color:var(--sub)}
  .sw{width:14px;height:14px;border-radius:3px;display:inline-block;border:1px solid rgba(255,255,255,.25)}
  .wrap{display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap}
  .board-panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}
  .side{width:260px;display:flex;flex-direction:column;gap:12px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px}
  .card h3{font-size:13px;margin-bottom:8px;color:var(--acc)}
  .card .row{display:flex;justify-content:space-between;font-size:13px;padding:2px 0}
  .card .row b{font-weight:600}
  #tip{font-size:12px;color:var(--sub);min-height:36px}
  #tileInfo{font-size:13px}
  #tileInfo .pos{color:var(--acc);font-weight:600}
  ul.list{list-style:none;max-height:220px;overflow:auto;font-size:12px}
  ul.list li{padding:2px 4px;border-radius:4px;cursor:pointer;display:flex;gap:6px}
  ul.list li:hover{background:#2c313d}
  .zbadge{display:inline-block;width:18px;text-align:center;border-radius:4px;font-weight:700}
  svg text{user-select:none}
  .tile-rect{cursor:pointer;transition:opacity .15s}
</style>
</head>
<body>
<h1>20_TE 关卡可视化</h1>
<div class="sub">棋盘 12×14（半格单位，视觉 7×8 牌位 = 14:16） · 碾压规则：z 更高 且 |dx|≤1 且 |dy|≤1（对应 TileDepthComputer.Overlaps） · 点击牌查看碾压关系</div>

<div class="toolbar">
  <label>版本</label>
  <button id="btnOld">修改前(偏左)</button>
  <button id="btnNew" class="active">修改后(右移+1)</button>
  <label style="margin-left:12px">视图</label>
  <select id="viewMode">
    <option value="stack">叠层总览（z 序渲染）</option>
    <option value="layer">单层查看</option>
  </select>
  <select id="layerSel" style="display:none"></select>
  <button id="btnTop" class="active" title="金框=顶部无压制，可点击">仅高亮可点牌</button>
  <div class="legend" id="legend"></div>
</div>

<div class="wrap">
  <div class="board-panel"><svg id="board" width="620" height="700" viewBox="0 0 620 700"></svg></div>
  <div class="side">
    <div class="card"><h3>关卡统计</h3><div id="statBox"></div></div>
    <div class="card"><h3>选中牌信息</h3><div id="tileInfo">点击棋盘上的牌查看碾压关系</div></div>
    <div class="card"><h3>层分布</h3><ul class="list" id="layerList"></ul></div>
    <div class="card"><div id="tip">提示：叠层总览中，牌透明度越低表示被越多上层牌压制；金色描边为顶部可点牌（MaxIndex=0）。</div></div>
  </div>
</div>

<script>
const DATA = __DATA__;
const U = 40;            // 半格像素
const BW = 14, BH = 16;  // 视觉半格总数（宽14=7牌，高16=8牌）
const LAYER_COLORS = ['#e05c5c','#e08b3a','#d4b13c','#7bb661','#4fb3a9','#4d8fd6','#8a6fd1','#d16fb0'];
let version='new', viewMode='stack', layer=7, selTile=-1, onlyTop=false;

function pressOf(ts){ // ts[i] 被哪些 j 压
  const res=[];
  for(let i=0;i<ts.length;i++){const c=[];
    for(let j=0;j<ts.length;j++){
      if(ts[j].z>ts[i].z && Math.abs(ts[j].x-ts[i].x)<=1 && Math.abs(ts[j].y-ts[i].y)<=1) c.push(j);
    } res.push(c);}
  return res;
}
function pressBy(ts){ // ts[i] 压哪些 j
  const res=Array.from({length:ts.length},()=>[]);
  const pressed=pressOf(ts);
  pressed.forEach((lst,i)=>lst.forEach(j=>res[j].push(i)));
  return res;
}
function cx(x){return 10+x*U;}          // 牌左上角（SVG 坐标）
function cy(y){return 10+(BH-2-y)*U;}   // y=0 在顶部（游戏内 y 大=屏幕下方）
function render(){
  const ts=DATA[version], svg=document.getElementById('board');
  const pressed=pressOf(ts), by=pressBy(ts);
  let s='';
  // 棋盘底
  s+=`<rect x="10" y="10" width="${BW*U}" height="${BH*U}" fill="#181b22" stroke="#3a3f4e" stroke-width="1.5" rx="6"/>`;
  // 中心线（x=6 数据坐标 = 牌中心线 x=7 半格）
  s+=`<line x1="${cx(6)}" y1="10" x2="${cx(6)}" y2="${10+BH*U}" stroke="#4da3ff" stroke-dasharray="6 5" opacity=".5"/>`;
  s+=`<text x="${cx(6)-4}" y="26" fill="#4da3ff" font-size="11" text-anchor="end">中心线x=6</text>`;
  // 半格网格
  for(let i=0;i<=BW;i++) s+=`<line x1="${10+i*U}" y1="10" x2="${10+i*U}" y2="${10+BH*U}" stroke="#22252e" stroke-width="1"/>`;
  for(let i=0;i<=BH;i++) s+=`<line x1="10" y1="${10+i*U}" x2="${10+BW*U}" y2="${10+BH*U}" stroke="#22252e" stroke-width="1"/>`;
  // 牌（z 升序绘制）
  const idx=[...ts.keys()].sort((a,b)=>ts[a].z-ts[b].z);
  for(const i of idx){
    const t=ts[i];
    if(viewMode==='layer' && t.z!==layer) continue;
    const nCover=pressed[i].length;
    const isTop=nCover===0;
    let op=1;
    if(viewMode==='stack') op=isTop?1:Math.max(.18,.9-nCover*.18);
    if(onlyTop && viewMode==='stack' && !isTop) op=Math.min(op,.25);
    const isSel=(i===selTile);
    const col=LAYER_COLORS[t.z];
    // 选中时的关系牌
    let stroke='rgba(255,255,255,.35)', sw=1;
    if(isTop&&viewMode==='stack'){stroke='#f5c542';sw=2;}
    if(isSel){stroke='#fff';sw=3;}
    let extra='';
    if(isSel){
      by[i].forEach(j=>{const q=ts[j];extra+=`<rect x="${cx(q.x)}" y="${cy(q.y)}" width="${2*U}" height="${2*U}" rx="8" fill="none" stroke="#ff6b6b" stroke-width="2.5" stroke-dasharray="7 4"/>`;});
      pressed[i].forEach(j=>{const q=ts[j];extra+=`<rect x="${cx(q.x)}" y="${cy(q.y)}" width="${2*U}" height="${2*U}" rx="8" fill="none" stroke="#4da3ff" stroke-width="2.5" stroke-dasharray="3 3"/>`;});
    }
    s+=`<g class="tile-rect" data-i="${i}">
      <rect x="${cx(t.x)}" y="${cy(t.y)}" width="${2*U}" height="${2*U}" rx="10"
        fill="${col}" fill-opacity="${op*.85}" stroke="${stroke}" stroke-width="${sw}"/>
      <text x="${cx(t.x)+U}" y="${cy(t.y)+U+5}" text-anchor="middle" font-size="15" font-weight="700"
        fill="#fff" opacity="${op}">${t.z}</text>
      ${viewMode==='stack'&&nCover>0?`<text x="${cx(t.x)+2*U-8}" y="${cy(t.y)+2*U-8}" text-anchor="end" font-size="10" fill="#fff" opacity="${op}">▼${nCover}</text>`:''}
    </g>`;
    s=extra+s;
  }
  svg.innerHTML=s;
  svg.querySelectorAll('.tile-rect').forEach(g=>g.addEventListener('click',e=>{
    selTile=+g.dataset.i; render(); showInfo();
  }));
  // 统计
  const nTop=pressed.filter(c=>c.length===0).length;
  const nPress=sum=>sum;
  const totalPress=pressed.reduce((a,c)=>a+c.length,0);
  document.getElementById('statBox').innerHTML=`
    <div class="row"><span>版本</span><b>${version==='new'?'右移+1（当前）':'修改前（偏左）'}</b></div>
    <div class="row"><span>总牌数</span><b>${ts.length}</b></div>
    <div class="row"><span>层数</span><b>8 (z=0~7)</b></div>
    <div class="row"><span>顶部可点牌</span><b style="color:#f5c542">${nTop}</b></div>
    <div class="row"><span>被压牌</span><b>${ts.length-nTop}</b></div>
    <div class="row"><span>碾压关系总数</span><b>${totalPress}</b></div>
    <div class="row"><span>x 使用范围</span><b>${Math.min(...ts.map(t=>t.x))}~${Math.max(...ts.map(t=>t.x))}（棋盘0~12）</b></div>`;
  // 层列表
  const zcnt={};ts.forEach(t=>zcnt[t.z]=(zcnt[t.z]||0)+1);
  document.getElementById('layerList').innerHTML=Object.keys(zcnt).map(z=>{
    const zt=ts.filter((t,i)=>t.z==+z&&pressed[i].length===0).length;
    return `<li data-z="${z}"><span class="zbadge" style="background:${LAYER_COLORS[z]}">${z}</span>
      <span>${zcnt[z]} 张</span><span style="margin-left:auto;color:#f5c542">可点${zt}</span></li>`;
  }).join('');
  document.getElementById('layerList').querySelectorAll('li').forEach(li=>
    li.addEventListener('click',()=>{layer=+li.dataset.z;document.getElementById('viewMode').value='layer';viewMode='layer';syncLayerSel();render();}));
}
function showInfo(){
  const ts=DATA[version],pressed=pressOf(ts),by=pressBy(ts);
  const box=document.getElementById('tileInfo');
  if(selTile<0){box.innerHTML='点击棋盘上的牌查看碾压关系';return;}
  const t=ts[selTile];
  const fmtList=arr=>arr.length?arr.map(j=>{const q=ts[j];
    return `<li data-j="${j}"><span class="zbadge" style="background:${LAYER_COLORS[q.z]}">${q.z}</span> (${q.x},${q.y})</li>`;}).join('')
    :'<li style="color:var(--sub)">无</li>';
  box.innerHTML=`<div class="pos">牌 #${selTile} @ (${t.x}, ${t.y}, z=${t.z})</div>
    <div style="margin:6px 0 2px">被 <b style="color:#4da3ff">${pressed[selTile].length}</b> 张上层牌压制（蓝虚框）</div>
    <div>压制 <b style="color:#ff6b6b">${by[selTile].length}</b> 张下层牌（红虚框）</div>
    <div style="margin-top:6px;color:var(--sub)">压制它的牌：</div><ul class="list">${fmtList(pressed[selTile])}</ul>
    <div style="margin-top:6px;color:var(--sub)">它压制的牌：</div><ul class="list">${fmtList(by[selTile])}</ul>`;
  box.querySelectorAll('li[data-j]').forEach(li=>li.addEventListener('click',()=>{selTile=+li.dataset.j;render();showInfo();}));
}
function syncLayerSel(){
  const sel=document.getElementById('layerSel');
  sel.style.display=viewMode==='layer'?'':'none';
  if(sel.options.length===0){for(let z=0;z<8;z++)sel.add(new Option('z='+z,z));}
  sel.value=layer;
}
function buildLegend(){
  document.getElementById('legend').innerHTML=
    `<span class="sw" style="background:#f5c542"></span>顶部可点`+
    `<span class="sw" style="background:#888;opacity:.4"></span>被压(▼=压数)`+
    `<span class="sw" style="border:2px solid #ff6b6b"></span>选中牌压制`+
    `<span class="sw" style="border:2px solid #4da3ff"></span>压制选中牌`;
}
document.getElementById('btnOld').onclick=e=>{version='old';selTile=-1;toggle(e.target);render();showInfo();};
document.getElementById('btnNew').onclick=e=>{version='new';selTile=-1;toggle(e.target);render();showInfo();};
document.getElementById('btnTop').onclick=e=>{onlyTop=!onlyTop;e.target.classList.toggle('active',onlyTop);render();};
document.getElementById('viewMode').onchange=e=>{viewMode=e.target.value;syncLayerSel();render();};
document.getElementById('layerSel').onchange=e=>{layer=+e.target.value;render();};
function toggle(btn){[document.getElementById('btnOld'),document.getElementById('btnNew')].forEach(b=>b.classList.remove('active'));btn.classList.add('active');}
buildLegend();syncLayerSel();render();showInfo();
</script>
</body>
</html>"""

html = html.replace('__DATA__', data)
out = r'D:/meatloaf_client01/local_py_script/20_TE_visualization.html'
open(out, 'w', encoding='utf-8').write(html)
print('已生成:', out, len(html), '字符')
