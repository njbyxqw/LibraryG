using System.Collections.Generic;
using Game.TileV2.Scripts.Config.Game;
using Game.TileV2.Scripts.Config.Record;
using Game.TileV2.Scripts.Config.Record.State;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Module.InLevelDDA;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Module.InLevelDDA.V2;
using Game.TileV2.Scripts.GameRecord;
using Game.TileV2.Scripts.GameRecord.Module;
using Game.TileShared.Scripts.UILogic.Interface;
using UnityEngine;

namespace Game.TileV2.Scripts.Entry
{
    public partial class TileMatchGame
    {
        [SerializeField] private TileMatchGameReconnectorWhiteList whiteList;

        private void InitializeRecordController()
        {
            _recordController = new TileMatchRecordController(
                _proxy,
                _recordMemoryString,
                _currentLevelConfig,
                _customData
            );
        }

        private void UpdateRecordController()
        {
            if (_customData.GameMode != GameMode.Bot)
            {
                TileMatchGameRecordBinaryPersister.ClearBotRecordPath();
            }

            _recordController.UpdateRecordController(
                _levelLogic,
                _gameLogic,
                _viewController,
                _application
            );

            _recordController.StartRecording();

            bool useRealTime = _customData.GameMode != GameMode.Bot;
            bool needVirtualTime = _customData.GameMode == GameMode.Bot ||
                                   _recordController.RecordControllerState == TileMatchGameRecordControllerState.Reconnecting;
            _recordController.SetTimeMode(useRealTime, needVirtualTime);

            _recordController.SetBasicInfo(
                _currentLevelConfig,
                _gameLogic.GetRandomSeed(),
                _viewController.GetRandomSeed());

            _recordController.SetDataBridgeInfo(_dataBridge);

            var ddaType = (byte)_gameLogic.GetDDAType();
            var v1Config = BuildDDAV1RecordConfig();
            var v2Config = BuildDDAV2RecordConfig(ddaType);
            _recordController.SetDDAConfigInfo(ddaType, v1Config, v2Config);

            _recordController.AddTileRandomResult(_gameLogic.GetTileTypes());

            _recordController.SetWhiteList(whiteList);
        }

        private DDAV1RecordConfig BuildDDAV1RecordConfig()
        {
            var v1 = _gameLogic.GetDDAV1Config();
            var maxRegulationDarkTimes = _currentLevelConfig.LevelExcelInfo.maxExchangeDarkTimes;
            return new DDAV1RecordConfig(
                v1?.RegulationComplexityConfig ?? _proxy.RegulationComplexityConfig,
                v1?.RegulationComplexityStep ?? _proxy.RegulationComplexityStep,
                v1?.CumulativeComplexityConfig ?? _proxy.CumulativeComplexityConfig,
                v1?.RegulationProbabilityConfig ?? _proxy.RegulationProbabilityConfig,
                maxRegulationDarkTimes);
        }

        private DDAV2RecordConfig BuildDDAV2RecordConfig(byte ddaType)
        {
            if (ddaType != 1) return null;
            var v2 = _gameLogic.GetDDAV2Config();
            if (v2 == null) return null;
            int[] propTypeKeys = null;
            int[] propValues = null;
            if (v2.PropValue != null && v2.PropValue.Count > 0)
            {
                propTypeKeys = new int[v2.PropValue.Count];
                propValues = new int[v2.PropValue.Count];
                int idx = 0;
                foreach (var kv in v2.PropValue)
                {
                    propTypeKeys[idx] = (int)kv.Key;
                    propValues[idx] = kv.Value;
                    idx++;
                }
            }
            return new DDAV2RecordConfig(
                v2.UseDiamondSpendAsPropLimit,
                v2.StageThresholds,
                InLevelDDAV2RegulationStrategyTypeConverter.ToIntArray(v2.StrategyTypes),
                v2.EarlyStageProbabilities,
                v2.MidStageProbabilities,
                v2.LateStageProbabilities,
                v2.AfterFailProbabilities,
                propTypeKeys,
                propValues,
                v2.PropLimitValue,
                v2.AfterPropProbabilities,
                v2.AfterPropLimitProbabilities);
        }

        public TileMatchGameRecordControllerState GetRecordControllerState()
        {
            if (_recordController != null)
            {
                return _recordController.RecordControllerState;
            }
            return TileMatchGameRecordControllerState.None;
        }

        private static string _recordMemoryString = "";
        private static string _pendingLevelDiffString = "";

        public static void SetRecordString(string recordString)
        {
            _recordMemoryString = recordString;
        }

        public static void SetPendingLevelDiffString(string s)
        {
            _pendingLevelDiffString = s ?? string.Empty;
        }

        public static string GetPendingLevelDiffString()
        {
            return _pendingLevelDiffString;
        }

        public static string GetAndClearPendingLevelDiffString()
        {
            var s = _pendingLevelDiffString;
            _pendingLevelDiffString = string.Empty;
            return s;
        }

        public static string GetLevelRecordStringFromDisk(string customPath = null)
        {
            return TileMatchRecordController.GetLevelRecordStringFromDisk(customPath);
        }

        public string GetPreviousLevelRecordStringFromDisk()
        {
            return _previousLevelRecordStringFromDisk ?? string.Empty;
        }

        private void UpdateWhenEnterAnimation()
        {
            _recordController.UpdateWhenEnterAnimation();
        }

        public void TryPlayOldRecord()
        {
            _recordController.TryPlayGameRecord();
        }

        public void TryPauseOldRecord()
        {
            _recordController.TryPauseGameRecord();
        }

        public void TryAccelerateOldRecordPlaySpeed()
        {
            _recordController.TryAcceleratePlaySpeed();
        }

        public void TryDecelerateOldRecordPlaySpeed()
        {
            _recordController.TryDeceleratePlaySpeed();
        }

        public void ResetOldRecordPlaySpeed()
        {
            _recordController.ResetPlaySpeed();
        }

        public string GetOldRecordCurrentPlaySpeed()
        {
            return _recordController.GetCurrentPlaySpeed();
        }

        public TileMatchGameRecord GetCurrentPlayingRecord()
        {
            return _recordController.GetCurrentPlayingRecord();
        }

        public TileMatchGameRecordPlayerState GetCurrentPlayingRecordState()
        {
            if (_recordController != null)
            {
                return _recordController.GetCurrentPlayingRecordState();
            }
            return TileMatchGameRecordPlayerState.Paused;
        }

        public double GetCurrentPlayingRecordTime()
        {
            if (_recordController != null)
            {
                return _recordController.GetCurrentPlayingRecordTime();
            }
            return 0;
        }

        private void UpdateDataBridgeIfNeeded()
        {
            // 优先检查是否有录像需要恢复
            if (_recordController.IsReplayingOrReconnecting())
            {
                var record = _recordController.GetPreviousRecord();
                if (record != null && _dataBridge != null)
                {
                    // 从录像恢复 DataBridge
                    _dataBridge.UpdateDataBridge(
                        record.IsSelectAddOne,
                        record.IsSelectMagicWand,
                        record.IsCanCollectGold,
                        record.IsCanShowRocket,
                        record.WinStreakTimes,
                        record.LevelRegulationHard,
                        record.RocketLuckyProbability);
                    return;
                }
            }

            Debug.Log($"[RocketVL] UpdateDataBridgeIfNeeded: GameMode={_customData.GameMode}, IsCanShowRocket={_customData.IsCanShowRocket}, RocketMode={_customData.RocketMode}");

            // 没有录像时，根据 GameMode 选择数据源
            if (_customData.GameMode == GameMode.Game)
            {
                // 从 Proxy 获取（正常游戏流程）
                _dataBridge?.UpdateDataBridge(
                    _proxy.IsSelectAddOne(),
                    _proxy.IsSelectMagicWand(),
                    _proxy.GetIsCanCollectGold(),
                    _proxy.GetIsCanShowRocket(),
                    _proxy.GetWinStreakNum(),
                    _proxy.GetLevelRegulationHard(),
                    _proxy.GetRocketLuckyProbability());
            }
            else
            {
                // 从 CustomData 获取（Trial/Bot 模式）
                _dataBridge?.UpdateDataBridge(
                    _customData.IsSelectAddOne,
                    _customData.IsSelectMagicWand,
                    _customData.IsCanCollectGold,
                    _customData.IsCanShowRocket,
                    _customData.WinStreakTimes,
                    _customData.LevelRegulationHard,
                    _customData.RocketLuckyProbability,
                    _customData.RocketMode);
                Debug.Log($"[RocketVL] DataBridge updated from CustomData, RocketMode should be {_customData.RocketMode}, actual={_dataBridge.RocketMode}");
            }

            // JungleState 从 SingleFunctionProxies 透传进 DataBridge，统一口径供逻辑层使用。
            if (_dataBridge != null)
            {
                _dataBridge.UpdateJungleState(GetJungleStateFromProxies(_singleFunctionProxies));
            }
        }

        private static int GetJungleStateFromProxies(List<ISingleFunctionProxy> proxies)
        {
            int jungleState = -1;
            if (proxies == null || proxies.Count <= 0)
            {
                return -1;
            }
            for (int i = 0; i < proxies.Count; i++)
            {
                var proxy = proxies[i];
                if (proxy == null)
                {
                    continue;
                }
                var info = proxy.GetActivityInfo();
                if (info == null)
                {
                    continue;
                }
                jungleState = info.GetJungleState();
                if (jungleState != -1)
                {
                    return jungleState;
                }
            }
            return jungleState;
        }

        private void OnApplicationPause(bool pauseStatus)
        {
            _recordController?.OnApplicationPause(pauseStatus);
        }

        private void OnApplicationQuit()
        {
            _recordController?.OnApplicationQuit();
        }
    }
}
