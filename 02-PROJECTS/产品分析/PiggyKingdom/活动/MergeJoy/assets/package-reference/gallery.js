(() => {
  const stage = document.getElementById('joy-stage');
  const viewport = document.getElementById('joy-viewport');
  const original = document.getElementById('joy-original');
  if (!stage || !viewport) return;
  const zones = {
    '1': {kicker:'01 / 活动身份与生命周期',title:'标题和倒计时回答“我在玩什么、还剩多久”',copy:'Merge Joy 标题叠在秋日橙色飘带上。倒计时表达当前活动剩余时间；帮助说明玩法，右上关闭在正常活动期保存并返回，结束分支另有挽留和补领。这里的 6d 22h 是参照截图的示意文案。',metrics:['适配参考 1080 × 2338 UI','标题 Rect 505.55 × 97.30 UI','原图飘带 806 × 239 px']},
    '2': {kicker:'02 / 主链成长与首次奖励',title:'把已解锁物品、后续目标和礼包放在同一条成长线上',copy:'彩色代表已解锁，剪影代表后续目标；礼物节点连接主链 Lv.8～12 的首次解锁奖励。进度取历史最大值，继续合成不会回退。礼物用于预览与达标反馈，首次进度奖由解锁逻辑触发，不另加提交或消耗目标物品。',metrics:['滚动窗口 903.5 × 130.9 UI','目标图标 Rect 146 × 146 UI','主链共 12 级']},
    '3': {kicker:'03 / 独立 BP 入口',title:'Progress 是物品解锁型双轨奖励',copy:'主题区右侧的册子入口打开 BP。Joy 以解锁主链 Lv.2～11 推进 10 档，免费和付费分别记录领取；不是按累计投放次数推进。复刻只演示入口的位置与职责，不执行支付或发奖。',metrics:['秋日样式 MergePassPanel_3','列表窗口 987 × 820.82 UI','单档模板 933 × 260.9 UI']},
    '4': {kicker:'04 / 棋盘与空间解锁',title:'同一张棋盘，逐步打开空间',copy:'6 列 × 8 行。全覆盖 10000 由合成落点的上下左右相邻格一次解除；露出半覆盖 11000 后，要拖入同ID自由物品，与底物二合。底物不能直接拿走，半覆盖也不会被一次邻接伤害连带清除。点击左侧棋子可查看示意格状态。',metrics:['单格 142 × 142 UI','盘面 852 × 1136 UI','外框 888 × 1172 UI']},
    '5': {kicker:'05 / 两种底部状态',title:'有内容就投放，耗尽后引导回主线打关',copy:'待投放气泡角标 = 基础投放次数 coins + 暂存件数。点击时优先取暂存末项；暂存为空才花 1 次基础投放，随机空格生成主链 Lv.1。满盘不先扣除。两者都为零且在期、终奖未领时显示 Play。上方控件可对照两种展示状态。',metrics:['投放点击区 200 × 200 UI','气泡装饰 240 × 240 UI','Play Rect 465.4 × 202.5 UI']}
  };
  function chooseZone(id, cellText='') {
    const z = zones[id];
    document.getElementById('zone-kicker').textContent = z.kicker;
    document.getElementById('zone-title').textContent = z.title;
    document.getElementById('zone-copy').textContent = z.copy;
    const metrics = document.getElementById('zone-metrics');
    metrics.replaceChildren(...z.metrics.map(text => {const span=document.createElement('span');span.textContent=text;return span;}));
    document.getElementById('zone-cell').textContent = cellText;
    document.querySelectorAll('.zone-nav [data-zone]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.zone===id)));
    document.querySelectorAll('[data-outline]').forEach(e=>e.classList.toggle('selected',e.dataset.outline===id));
  }
  document.querySelectorAll('[data-zone]').forEach(b=>b.addEventListener('click',()=>chooseZone(b.dataset.zone)));
  document.querySelectorAll('.jr-cell').forEach(b=>b.addEventListener('click',()=>chooseZone('4',b.dataset.description)));
  document.getElementById('show-measures').addEventListener('change',e=>stage.classList.toggle('show-measures',e.target.checked));
  document.getElementById('bottom-state').addEventListener('change',e=>{stage.dataset.bottom=e.target.value;chooseZone('5');});
  document.querySelectorAll('[data-replica-view]').forEach(b=>b.addEventListener('click',()=>{
    const isReplica=b.dataset.replicaView==='replica';
    viewport.hidden=!isReplica;original.hidden=isReplica;
    document.querySelectorAll('[data-replica-view]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
    document.getElementById('bottom-state').disabled=!isReplica;
    document.getElementById('show-measures').disabled=!isReplica;
    document.getElementById('replica-caption').textContent=isReplica?'静态资源复刻；棋盘与物品摆放参照 S01。文字、按钮装饰及部分部件位置为示意，未运行 Spine 动画，不是游戏实拍或像素级还原。':'用户原始实拍 S01，1080 × 2376 px；拍摄时间、客户端版本和期号未知。此处没有用复刻替换或修改原图。';
    if(isReplica) scaleStage();
  }));
  function scaleStage(){stage.style.setProperty('--stage-scale',String(viewport.clientWidth/1080));}
  new ResizeObserver(scaleStage).observe(viewport);scaleStage();chooseZone('4');
  const filter=document.getElementById('dimension-filter');
  if(filter) filter.addEventListener('input',()=>{const value=filter.value.toLowerCase().trim();document.querySelectorAll('#sprite-dimensions tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(value));});
})();
