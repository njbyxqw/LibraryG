using System;
using System.Collections.Generic;
using System.Threading;
using BettaSDK;
using Cysharp.Threading.Tasks;
using DG.Tweening;
using Game.TileV2.Scripts.Config.Effect;
using Game.TileV2.Scripts.Config.Game;
using Game.TileV2.Scripts.Config.Level;
using Game.TileV2.Scripts.Config.LevelDataBase;
using Game.TileV2.Scripts.Config.Tile;
using Game.TileShared.Scripts.GameCore.DomainEvent;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic;
using Game.TileV2.Scripts.GameCore.View.GameView.Services;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Data;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Module.SolutionHint;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Module.Statistic;
using Game.TileV2.Scripts.GameCore.Logic.LevelLogic.Data;
using Game.TileV2.Scripts.GameCore.Logic.Interface;
using Game.TileV2.Scripts.GameCore.View.Config;
using Game.TileV2.Scripts.GameCore.View.Interface;
using Game.TileV2.Scripts.GameCore.View.GameView.Module.ParticleSystem;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.Background;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.Bar;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.Board;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.LevelAnimation.ViewCollection;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.LevelCollect.Interface;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.OverBar;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.Tile;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.TileActionFeedback;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.TileEffect;
using Game.TileV2.Scripts.Proxy.Interface;
using Game.TileShared.Scripts.Util;
using UnityEngine;
using UnityEngine.Serialization;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.Tile.CardBox;


namespace Game.TileV2.Scripts.GameCore.View.GameView
{
    public partial class TileMatchViewController : MonoBehaviour, ITileMatchViewController, IViewEnterAnimation, IDisposable
    {
        private BackgroundView _backgroundView;
        private string _loadedBackgroundPath;

        [Space]

        [SerializeField]
        private BoardView boardView;

        [SerializeField]
        private BarView barView;

        [SerializeField]
        private OverBarView overBarView;

        [SerializeField]
        private List<MonoBehaviour> collectViews;

        private readonly Dictionary<string, CollectView> _collectViews = new ();

        [SerializeField]
        private ViewCollectionAnimation viewsAnimation;

        private List<IView> _views;

        [Space]
        [SerializeField]
        private LevelScalerService levelScalerService;
        [SerializeField]
        private TileViewService tileViewService;
        [SerializeField]
        private EffectViewService effectViewService;
        [SerializeField]
        private ViewRandomService viewRandomService;
        [SerializeField]
        private ResourceLoadService resourceLoadService;
        [SerializeField]
        private InputService inputService;

        [FormerlySerializedAs("ActionFeedbackViewController")]
        [Space]

        [SerializeField]
        private TileActionFeedbackViewController actionFeedbackViewController;

        [Space]

        [SerializeField]
        private ParticlesController particlesController;

        [Space]

        [SerializeField]
        private Camera mainCamera;

        private readonly Dictionary<long, TileView> _tileViews = new ();
        private readonly Dictionary<long, EffectView> _effectViews = new();

        private readonly List<long> _tileViewKeysCache = new();
        private readonly List<long> _effectViewKeysCache = new();

        private List<IViewService> _services;

        private GameConfig _gameConfig;
        private LevelDatabase _levelDatabase;
        private LevelData _currentLevelData;
        private GameData _currentGameData;
        private DataBridge _dataBridge;
        private Statistic _statistic;

        internal GameConfig GameConfig => _gameConfig;
        internal LevelData CurrentLevelData => _currentLevelData;
        internal GameData CurrentGameData => _currentGameData;
        internal LevelDatabase LevelDatabase => _levelDatabase;
        public DataBridge DataBridge => _dataBridge;

        internal Statistic Statistic => _statistic;

        internal Camera MainCamera => mainCamera;
        internal BoardView BoardView => boardView;
        internal BarView BarView => barView;
        internal OverBarView OverBarView => overBarView;


        internal LevelScalerService LevelScalerService => levelScalerService;
        public InputService InputService => inputService;
        internal TileViewService TileViewService => tileViewService;
        internal EffectViewService EffectViewService => effectViewService;
        internal ViewRandomService ViewRandomService => viewRandomService;
        internal ResourceLoadService ResourceLoadService => resourceLoadService;


        internal IRecordController RecordController { get; private set; }

        public static TileMatchViewController Instance { get; private set; }

        internal ITileMatchProxy Proxy { get; private set; }

        private CancellationTokenSource _cancellationTokenSource;

        private bool _initialized;

        public void Initialize(
            ITileMatchProxy proxy,
            LevelData levelData,
            GameData gameData,
            GameConfig gameConfig,
            LevelDatabase levelDatabase,
            DataBridge dataBridge,
            Statistic statistic,
            IRecordController recordController,
            LayoutParam layoutParam)
        {
            LayoutParam = layoutParam;

            _cancellationTokenSource = new CancellationTokenSource();

            Instance = this;

            Proxy = proxy;

            _currentLevelData = levelData;
            _currentGameData = gameData;

            _levelDatabase = levelDatabase;
            _gameConfig = gameConfig;
            _dataBridge = dataBridge;
            _statistic = statistic;

            RecordController = recordController;

            if (_currentGameData == null)
            {
                LogUtil.LogError(nameof(TileMatchViewController), "GameData不能为空");
                return;
            }

            InitializeServices();

            InitializeView();

            if (mainCamera != null)
            {
                mainCamera.cullingMask |= (1 << LayerMask.NameToLayer("Default"));
            }

            levelScalerService?.ReAdapterViewPos();

            _initialized = true;

            DomainEventBus.PublishForEnumKey(ToLogicEventType.LevelViewInitialized);

            inputService.SetRayCastEnable(false);
            RegisterEventHandlers();

        }

        private void InitializeServices()
        {
            _services = new List<IViewService>();

            if (levelScalerService)
                _services.Add(levelScalerService);
            if (inputService)
                _services.Add(inputService);
            if (tileViewService)
                _services.Add(tileViewService);
            if (effectViewService)
                _services.Add(effectViewService);
            if (viewRandomService)
                _services.Add(viewRandomService);
            if (resourceLoadService)
                _services.Add(resourceLoadService);

            resourceLoadService.Init(_levelDatabase);
            CallServiceInit();
        }

        private void InitializeViewsList()
        {
            _views = new List<IView>();

            if (_backgroundView)
                _views.Add(_backgroundView);
            if (boardView)
                _views.Add(boardView);
            if (barView)
                _views.Add(barView);
            if (overBarView)
                _views.Add(overBarView);

            foreach (var view in collectViews)
            {
                if (view is CollectView collectView)
                {
                    _views.Add(collectView);
                    _collectViews.Add(collectView.CollectKey, collectView);
                }
            }
        }

        private void CallServiceInit()
        {
            foreach (var service in _services)
            {
                service.OnServiceInit();
            }
        }

        private void InitializeViewActions()
        {
            foreach (var kvp in _viewActions)
            {
                if (kvp.Value != null)
                {
                    kvp.Value.OnControllerInit();
                }
            }
        }

        private void Update()
        {
            if (!_autoTickEnable)
            {
                return;
            }

            TickTimer(Time.deltaTime);
        }

        private void TickTimer(float deltaTime)
        {
            if (!_initialized)
            {
                return;
            }

            _elapsedTime += deltaTime;
            _timerTickEventData.Update(deltaTime, _elapsedTime);

            DomainEventBus.PublishForEnumKey(GameLogicEventType.GameTimerTick, (int)EntityType.All, _timerTickEventData);
            DomainEventBus.PublishForEnumKey(ToLogicEventType.LevelTimerTick, (int)EntityType.All, _timerTickEventData);

            CallServiceUpdate(deltaTime, _elapsedTime);
            CallViewTimerTick(deltaTime, _elapsedTime);
        }

        private void CallServiceUpdate(float deltaTime, float elapsedTime)
        {
            foreach (var service in _services)
            {
                service.OnServiceUpdate(deltaTime, elapsedTime);
            }
        }

        private void CallViewTimerTick(float deltaTime, float elapsedTime)
        {
            foreach (var kvp in _viewActions)
            {
                if (kvp.Value != null)
                {
                    kvp.Value.OnControllerUpdate(deltaTime, elapsedTime);
                }
            }

            _tileViewKeysCache.Clear();
            foreach (var key in _tileViews.Keys)
            {
                _tileViewKeysCache.Add(key);
            }

            foreach (var key in _tileViewKeysCache)
            {
                if (_tileViews.TryGetValue(key, out var tileView) && tileView)
                {
                    tileView.OnTimerTick(deltaTime, elapsedTime);
                }
            }

            _effectViewKeysCache.Clear();
            foreach (var key in _effectViews.Keys)
            {
                _effectViewKeysCache.Add(key);
            }

            foreach (var key in _effectViewKeysCache)
            {
                if (_effectViews.TryGetValue(key, out var effectView) && effectView != null && effectView.gameObject)
                {
                    effectView.OnTimerTick(deltaTime, elapsedTime);
                }
            }

            foreach (var view in _views)
            {
                view.OnTimerTick(deltaTime, elapsedTime);
            }
        }

        private void CallViewOnCreated()
        {
            foreach (var view in _views)
            {
                view.OnCreated();
            }

            foreach (var kvp in _viewActions)
            {
                if (kvp.Value != null)
                {
                    kvp.Value.OnControllerInit();
                }
            }
        }

        private void CallViewOnDisposed()
        {
            foreach (var kvp in _effectViews)
            {
                if (kvp.Value)
                {
                    kvp.Value.OnDisposed();
                }
            }

            foreach (var kvp in _tileViews)
            {
                if (kvp.Value)
                {
                    kvp.Value.OnDisposed();
                }
            }

            foreach (var view in _views)
            {
                view.OnDisposed();
            }

            foreach (var kvp in _viewActions)
            {
                if (kvp.Value != null)
                {
                    kvp.Value.OnControllerDispose();
                }
            }
        }

        private void CallServiceDispose()
        {
            if (_services != null)
            {
                foreach (var service in _services)
                {
                    service.OnServiceDispose();
                }

                _services.Clear();
            }
        }

        private float _elapsedTime;

        // Reuse reference payload for timer tick to avoid boxing/GC.
        private readonly TimerTickEventData _timerTickEventData = new TimerTickEventData();

        private void InitializeView()
        {
            levelScalerService.OnServiceInit();

            particlesController.Initialize();

            LoadBackgroundView();

            InitializeViewsList();

            CallViewOnCreated();

            ClearAllTileViews();
            ClearAllEffectViews();

            InitializeViewActions();

            CreateTileViewsFromData();
            CreateEffectViewsFromData();

            PreloadConfig();

            _elapsedTime = 0;
        }

        private void LoadBackgroundView()
        {
            var bgPrefabPath = GetBackgroundPath(
                _currentGameData.LevelConfig.LevelId,
                _currentGameData.LevelConfig.LevelType,
                _currentGameData.LevelConfig.LevelHard);
            Transform backgroundParent = transform;
            DestroyBackgroundView();

            GameObject backgroundObject = TileResourceHub.LoadAsset<GameObject>(bgPrefabPath, gameObject);
            if (!backgroundObject)
            {
                LogUtil.LogError(nameof(TileMatchViewController), $"背景Prefab加载失败: {bgPrefabPath}");
                _loadedBackgroundPath = null;
                return;
            }

            backgroundObject.transform.SetParent(backgroundParent, false);
            _backgroundView = backgroundObject.GetComponent<BackgroundView>();
            if (!_backgroundView)
            {
                LogUtil.LogError(nameof(TileMatchViewController), $"背景Prefab缺少BackgroundView组件: {bgPrefabPath}");
                Destroy(backgroundObject);
                _loadedBackgroundPath = null;
                return;
            }

            _loadedBackgroundPath = _backgroundView ? bgPrefabPath : null;
        }

        private void DestroyBackgroundView()
        {
            if (_backgroundView == null)
            {
                return;
            }

            Destroy(_backgroundView.gameObject);
            _backgroundView = null;
            _loadedBackgroundPath = null;
        }

        private void CreateTileViewsFromData()
        {
            if (_currentGameData?.BoardData == null)
            {
                LogUtil.LogError(nameof(TileMatchViewController), "BoardData不能为空");
                return;
            }

            var boardData = _currentGameData.BoardData;
            var tileDataList = boardData.Tiles;

            foreach (var tileData in tileDataList)
            {
                var tileView = CreateOneTileView(tileData);

                if (tileView)
                {
                    _ = boardView.AddTile(tileView, true);
                }

            }

            LogUtil.Log(nameof(TileMatchViewController), $"视图初始化完毕: 创建了 {_tileViews.Count} 个TileView");
        }

        public TileView CreateOneTileView(TileData tileData)
        {
            var tileViewObj = CreateTileViewGameObject(tileData);
            if (tileViewObj)
            {
                var tileView = tileViewObj.GetComponent<TileView>();

                _tileViews[tileData.Id] = tileView;
                tileView.OnCreated();

                return tileView;
            }
            return null;
        }

        private GameObject CreateTileViewGameObject(TileData tileData)
        {
            if (tileViewService == null)
            {
                LogUtil.LogError(nameof(TileMatchViewController), "CreateTileViewService未设置");
                return null;
            }

            return tileViewService.CreateTileViewFromData(tileData);
        }

        private void ClearAllTileViews()
        {
            foreach (var kvp in _tileViews)
            {
                if (kvp.Value)
                {
                    boardView.RemoveTile(kvp.Value);
                    barView.RemoveTile(kvp.Value);
                    overBarView.RemoveTile(kvp.Value);

                    kvp.Value.OnDisposed();
                    Destroy(kvp.Value.gameObject);
                }
            }

            _tileViews.Clear();
        }

        public TileView GetTileView(long tileId)
        {
            _tileViews.TryGetValue(tileId, out var tileView);
            return tileView;
        }

        public ITileView GetITileView(long tileId)
        {
            _tileViews.TryGetValue(tileId, out var tileView);
            return tileView;
        }

        public TileView GetTileView(Vector3Int position, bool clickable = false)
        {
            foreach (var kvp in _tileViews)
            {
                if (kvp.Value && kvp.Value.TileData.Position == position)
                {
                    if (clickable)
                    {
                        if (!kvp.Value.Clickable())
                        {
                            continue;
                        }
                    }
                    return kvp.Value;
                }
            }

            return null;
        }

        public Dictionary<long, TileView> GetAllTileViews()
        {
            return _tileViews;
        }

        public bool IsTileInBar(long tileId)
        {
            return barView != null && barView.ContainsTile(tileId);
        }

        public async UniTask AddTileToBar(long tileId, bool instant = false, BarAddType barAddType = BarAddType.Click)
        {
            if (_tileViews.TryGetValue(tileId, out var tileView))
            {
                boardView.RemoveTile(tileView);
                overBarView.RemoveTile(tileView);
                tileView.SetCustomControl(null);
                await barView.PlayAddToBarAnim(tileView, instant, barAddType);
            }
        }

        public UniTask ShowSolutionHint(SolutionHintViewData data)
        {
            const string logTag = "SolutionHint";
            int count = data?.PathTileIds != null ? data.PathTileIds.Count : 0;
            LogUtil.Log(logTag, $"View ShowSolutionHint trigger={data?.TriggerType} duration={data?.Duration} pathCount={count}");
            return PlaySolutionHintAsync(data);
        }

        public void ClearSolutionHint()
        {
            ClearCurrentSolutionHintPresentation();
        }

        public void ScheduleClearSolutionHint(float fallbackDelay)
        {
            ScheduleCurrentSolutionHintPresentationClear(fallbackDelay);
        }

        public async UniTask MatchAnimation(IReadOnlyList<TileData> dataList)
        {
            await barView.MatchAnimation(dataList);
        }

        public async UniTask AddTileToOverBar(TileData tileData, bool instant, bool ignoreOverBarCapacity = false)
        {
            if (_tileViews.TryGetValue(tileData.Id, out var tileView))
            {
                boardView.RemoveTile(tileView);
                barView.RemoveTile(tileView);
                tileView.SetCustomControl(null);
                await overBarView.PlayAddToOverBarAnim(tileView, instant, ignoreOverBarCapacity);
            }
        }

        public void RemoveTileView(TileData tileData)
        {
            if (!_tileViews.TryGetValue(tileData.Id, out var tileView))
            {
                return;
            }

            if ((tileView.ViewState & ViewState.Animating) != 0)
            {
                RemoveTileViewAfterAnimationAsync(tileData, tileView).Forget();
                return;
            }

            DoRemoveTileView(tileData, tileView);
        }

        private void DoRemoveTileView(TileData tileData, TileView tileView)
        {
            boardView.RemoveTile(tileView);
            barView.RemoveTile(tileView);
            overBarView.RemoveTile(tileView);
            _tileViews.Remove(tileData.Id);
            tileView.OnDisposed();
            Destroy(tileView.gameObject);
        }

        private async UniTaskVoid RemoveTileViewAfterAnimationAsync(TileData tileData, TileView tileView)
        {
            var token = _cancellationTokenSource?.Token ?? CancellationToken.None;
            try
            {
                while (tileView != null && tileView.gameObject != null && _tileViews.ContainsKey(tileData.Id) && (tileView.ViewState & ViewState.Animating) != 0)
                {
                    await UniTask.Yield(PlayerLoopTiming.Update, token);
                }
                if (token.IsCancellationRequested)
                {
                    return;
                }
                if (!_tileViews.ContainsKey(tileData.Id))
                {
                    return;
                }
                if (tileView == null || !tileView.gameObject)
                {
                    _tileViews.Remove(tileData.Id);
                    return;
                }
                DoRemoveTileView(tileData, tileView);
            }
            catch (OperationCanceledException)
            {
                // ignored
            }
        }

        private void CreateEffectViewsFromData()
        {
            if (_currentGameData?.BoardData == null)
            {
                LogUtil.LogError(nameof(TileMatchViewController), "BoardData不能为空");
                return;
            }

            var boardData = _currentGameData.BoardData;
            var effectDataList = boardData.Effects;

            foreach (var tileData in effectDataList)
            {
                CreateOneEffect(tileData);
            }

            LogUtil.Log(nameof(TileMatchViewController), $"视图初始化完毕: 创建了 {_effectViews.Count} 个EffectView");
        }

        private void CreateOneEffect(EffectData effectData)
        {
            var viewGameObject = CreateEffectViewGameObject(effectData);
            if (viewGameObject)
            {
                var effectView = viewGameObject.GetComponent<EffectView>();
                effectView.OnCreated();
                _effectViews[effectData.Id] = effectView;
                _ = boardView.AddEffect(effectView);
            }
        }

        private GameObject CreateEffectViewGameObject(EffectData effectData)
        {
            if (effectViewService == null)
            {
                LogUtil.LogError(nameof(TileMatchViewController), "EffectViewService未设置");
                return null;
            }

            return effectViewService.CreateEffectViewFromData(effectData);
        }

        public async UniTask ChangeEffectLives(EffectData effectData, int deltaLives)
        {
            if (_effectViews.TryGetValue(effectData.Id, out var effectView))
            {
                await effectView.ChangeEffectLives(deltaLives);
            }
        }

        public async UniTask ChangeTileLives(TileData tileData, int deltaLives)
        {
            if (_tileViews.TryGetValue(tileData.Id, out var tileView))
            {
                await tileView.ChangeTileLives(deltaLives);
            }
        }

        public async UniTask ChangeBatchLives(long batchId, int deltaLives)
        {
            //TODO:这里要做动画实现
            await UniTask.CompletedTask;
        }

        public async UniTask ChangeBatchTileState(long tileId, int state, bool instantOn = false)
        {
            if (_tileViews.TryGetValue(tileId, out var tileView)) {
                await tileView.ChangeBatchTileState(state, instantOn);
            }
            await UniTask.CompletedTask;
        }

        public async UniTask ChangeEffectState(EffectData effectData)
        {
            if (_effectViews.TryGetValue(effectData.Id, out var effectView))
            {
                await effectView.ChangeEffectState(effectData.State);
            }
        }

        public async UniTask ChangeEffectClickOccluder(EffectData effectData)
        {
            if (_effectViews.TryGetValue(effectData.Id, out var effectView))
            {
                await effectView.ChangeEffectClickOccluder(effectData.IsClickOccluder);
            }
        }

        private void ClearAllEffectViews()
        {
            foreach (var kvp in _effectViews)
            {
                if (kvp.Value)
                {
                    // boardView.RemoveEffect(kvp.Value);
                    // barView.RemoveEffect(kvp.Value);
                    // overBarView.RemoveEffect(kvp.Value);

                    kvp.Value.OnDisposed();
                    Destroy(kvp.Value.gameObject);
                }
            }
            _effectViews.Clear();
        }

        public EffectView GetEffectView(long effectId)
        {
            _effectViews.TryGetValue(effectId, out var effectView);
            return effectView;
        }

        public IEffectView GetIEffectView(long effectId)
        {
            _effectViews.TryGetValue(effectId, out var effectView);
            return effectView;
        }

        public EffectView GetEffectView(Vector3Int position)
        {
            foreach (var kvp in _effectViews)
            {
                if (kvp.Value.Position == position)
                {
                    return kvp.Value;
                }
            }
            return null;
        }

        public Dictionary<long, EffectView> GetAllEffectViews()
        {
            return _effectViews;
        }

        public void RemoveEffectView(EffectData effectData)
        {
            if (_effectViews.TryGetValue(effectData.Id, out var effectView))
            {
                if (effectView)
                {
                    boardView.RemoveEffect(effectView);
                    // barView.RemoveEffect(effectView);
                    // overBarView.RemoveEffect(effectView);
                    _effectViews.Remove(effectData.Id);

                    effectView.OnDisposed();
                    Destroy(effectView.gameObject);
                }
            }
        }

        public void Dispose()
        {
            _initialized = false;

            ClearCurrentSolutionHintPresentation();
            UnregisterEventHandlers();

            StopBGM();

            CallViewOnDisposed();
            DestroyBackgroundView();

            ClearAllTileViews();
            ClearAllEffectViews();
            ClearOtherViews();
            particlesController.Clear();

            CallServiceDispose();

            if (_bgmCancellationTokenSource != null)
            {
                _bgmCancellationTokenSource.Cancel();
                _bgmCancellationTokenSource = null;
            }

            _onEntityClicked = null;
            _onOperationFinished = null;

            _currentLevelData = null;
            _currentGameData = null;

            Instance = null;
        }

        private void ClearOtherViews()
        {
            _collectViews.Clear();
            _views.Clear();
        }

        public CollectView GetCollectView(string collectKey)
        {
            return _collectViews.GetValueOrDefault(collectKey, null);
        }

        public IReadOnlyList<CollectView> GetCollectViews()
        {
            return new List<CollectView>(_collectViews.Values);
        }

        private string GetBackgroundPath(int levelId, LevelType levelType, LevelDifficulty levelDifficulty)
        {
            var overridePath = Proxy?.GetOverrideBackground(levelId, (int)levelType);
            if (!string.IsNullOrEmpty(overridePath))
            {
                return overridePath;
            }

            if (levelType == LevelType.Bonus)
            {
                return ConfigData.BonusBackground;
            }

            if (levelType != LevelType.Normal)
            {
                return ConfigData.NormalBackground;
            }

            return ConfigData.BackgroundByDifficulty.GetValueOrDefault(levelDifficulty, ConfigData.NormalBackground);
        }

        public void PlayEnterAnim()
        {
            PlayEnterAnimation().AttachExternalCancellation(_cancellationTokenSource.Token).SafeForget();
        }

        public void PlayEnterBGM()
        {
            PlayBGM().WithGameObject(gameObject).AttachExternalCancellation(_cancellationTokenSource.Token).SafeForget();
        }

        public async UniTask PlayEnterAnimation()
        {
            // 统一的下落动画

            List<UniTask> enterTask1 = new();

            foreach (var view in _views)
            {
                if (view is IViewEnterAnimation enterAnimation)
                {
                    enterTask1.Add(enterAnimation.PlayEnterAnimation());
                }
            }

            if (viewsAnimation == null)
            {
                viewsAnimation = ScriptableObject.CreateInstance<SimpleSpawnAnimation>();
                LogUtil.LogError(nameof(TileMatchViewController), "viewsAnimation is null");
            }
            enterTask1.Add(viewsAnimation.Play(this, true));

            if (enterTask1.Count > 0)
            {
                await UniTask.WhenAll(enterTask1);
            }

            DomainEventBus.PublishForEnumKey(ToLogicEventType.LevelEnterAnimationStepOneFinished);

            // 特殊的自定义动画, 例如魔盒的吐牌
            List<UniTask> enterTask2 = new();

            foreach (var kvp in _tileViews)
            {
                if (kvp.Value.CustomEnterAnimDelay() > 0)
                {
                    var delayTask = DOVirtual.DelayedCall(kvp.Value.CustomEnterAnimDelay(), () => { }).ToUniTask();
                    enterTask2.Add(delayTask);
                }
            }

            foreach (var kvp in _effectViews)
            {
                if (kvp.Value.CustomEnterAnimDelay() > 0)
                {
                    var delayTask = DOVirtual.DelayedCall(kvp.Value.CustomEnterAnimDelay(), () => { }).ToUniTask();
                    enterTask2.Add(delayTask);
                }
            }

            if (enterTask2.Count > 0)
            {
                await UniTask.WhenAll(enterTask2);
            }

            DomainEventBus.PublishForEnumKey(ToLogicEventType.LevelEnterAnimationStepTwoFinished);
        }

        internal Vector3 GetLowestTileViewPosition()
        {
            float lowestY = float.MaxValue;
            Vector3 lowestPos = Vector3.zero;

            foreach (var kvp in _tileViews)
            {
                if (kvp.Value && kvp.Value.transform.position.y < lowestY)
                {
                    lowestY = kvp.Value.transform.position.y;
                    lowestPos = kvp.Value.transform.position;
                }
            }

            return lowestPos;
        }

        public int GetRandomSeed()
        {
            return viewRandomService.GetSeed();
        }

        public void ExchangePair(Tuple<List<TileData>, List<EffectData>> tuple)
        {
            bool hasCardBoxSequence = false;
            var cardBoxContainerIds = new HashSet<long>();

            for (int i = 0; i < tuple.Item1.Count; i+=2)
            {
                var view1 = GetTileView(tuple.Item1[i].Id);
                var view2 = GetTileView(tuple.Item1[i + 1].Id);
                boardView.ExchangePileTile(view1, view2);

                var customControl1 = view1.CustomControl;
                var customControl2 = view2.CustomControl;
                view1.SetCustomControl(customControl2);
                view2.SetCustomControl(customControl1);

                var autoChangeHighlight1 = view1.AutoChangeHighlight;
                var autoChangeHighlight2 = view2.AutoChangeHighlight;
                view1.SetAutoChangeHighlight(autoChangeHighlight2);
                view2.SetAutoChangeHighlight(autoChangeHighlight1);
            }

            foreach (var tileData in tuple.Item1)
            {
                var tileView = GetTileView(tileData.Id);
                if (tileView == null || tileView.TileData.State != TileState.InBoard)
                {
                    continue;
                }

                boardView.UpdateTilePositions(tileView);
                tileView.OnShuffleChange();
            }

            foreach (var effectData in tuple.Item2)
            {
                if (effectData.State == EffectState.WillDestroy)
                {
                    continue;
                }
                var effectView = GetEffectView(effectData.Id);
                // 跟随 Tile 交换的 Effect（如 Golden）需要先完成宿主重绑和位置更新，
                // 再解除显隐延迟；否则会按新可见性刷新到旧 Tile 上，导致穿帮。
                effectView.RebindTileViews();
                boardView.UpdateEffectPositions(effectView);

                // 逻辑换牌阶段对部分 Effect（如 Golden）设置了 DeferVisibilitySync，
                // 此处视图已经完成 Rebind 和位置更新，可以清除标记并刷新一次显隐/高亮。
                effectData.ClearDeferVisibilitySync();
                effectView.UpdateHighlight(true);
            }
        }
    }
}
