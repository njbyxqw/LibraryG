using System.Collections.Generic;
using Game.TileV2.Scripts.Config.Level;
using UnityEngine.Scripting;

namespace Game.TileV2.Scripts.Config.Game
{
    [Preserve]
    public class CustomData
    {
        public static CustomData GetDefault()
        {
            return new CustomData();
        }

        public GameMode GameMode { get; private set; } = GameMode.Game;
        
        // LevelInfo
        public string LevelName { get; private set; }
        
        // DataBridge
        public int WinStreakTimes { get; private set; }
        
        public bool IsSelectAddOne { get; private set; }
        public bool IsSelectMagicWand { get; private set; }
        
        public bool IsCanShowRocket { get; private set; }
        public int RocketMode { get; private set; }   // 0=默认火箭效果, 3=闪电球特效(RocketVL)
        public bool IsCanCollectGold { get; private set; }
        
        public int GoldCountOverride { get; private set; } = -1;

        public int LevelIdOverride { get; private set; }
        
        public int LevelRegulationHard { get; private set; }
        public int RocketLuckyProbability { get; private set; }
        
        public int RandomStep { get; private set; }
        public int RandomTimes { get; private set; }

        public Dictionary<string, string> StrategyOptions { get; private set; } = new ();
    
        public LevelConfig LevelConfig { get; private set; }
        
        public int LogicRandomSeed { get; private set; }

        /// <summary> 机器人跑关使用的 DDA 版本："V1" 或 "V2"，由 BotParam.ddaVersion 传入。 </summary>
        public string DDAVersion { get; private set; } = "V2";
        
        [Preserve]
        public CustomData()
        {
            ResetData();
        }
        
        private void ResetData()
        {
            GameMode = GameMode.Game;
            LevelName = string.Empty;
            WinStreakTimes = 0;
            IsSelectAddOne = false;
            IsSelectMagicWand = false;
            IsCanShowRocket = false;
            RocketMode = 0;
            IsCanCollectGold = false;
            GoldCountOverride = -1;
            LevelIdOverride = 0;
            RocketLuckyProbability = 0;
            RandomStep = -1;
            RandomTimes = -1;
            LevelConfig = new LevelConfig();
        }
        
        public void SetGameMode(GameMode mode)
        {
            GameMode = mode;
        }
        
        public void SetLevelName(string levelName)
        {
            LevelName = levelName ?? string.Empty;
        }
        
        public void SetWinStreakTimes(int count)
        {
            WinStreakTimes = count;
        }
        
        public void SetIsAddOne(bool result)
        {
            IsSelectAddOne = result;
        }
        
        public void SetIsMagicWand(bool result)
        {
            IsSelectMagicWand = result;
        }
        
        public void SetIsCanCollectGold(bool result)
        {
            IsCanCollectGold = result;
        }
        
        public void SetIsRocket(bool result)
        {
            IsCanShowRocket = result;
            if (!result)
            {
                RocketMode = 0;
            }
        }

        public void SetRocketMode(int mode)
        {
            RocketMode = mode;
            if (mode > 0)
            {
                IsCanShowRocket = true;
            }
        }
        
        public void SetGoldCountOverride(int count)
        {
            GoldCountOverride = count;
        }

        public void SetLevelIdOverride(int levelId)
        {
            LevelIdOverride = levelId;
        }

        public void SetRocketLuckyProbability(int probability)
        {
            RocketLuckyProbability = probability;
        }
        
        public void SetRandomStep(int count)
        {
            RandomStep = count;
        }
        
        public void SetRandomTimes(int count)
        {
            RandomTimes = count;
        }

        public void SetLevelConfig(LevelConfig levelConfig)
        {
            LevelConfig = levelConfig;
        }

        public void SetLogicRandomSeed(int seed)
        {
            LogicRandomSeed = seed;
        }

        public void SetDDAVersion(string ddaVersion)
        {
            DDAVersion = string.IsNullOrEmpty(ddaVersion) ? "V2" : ddaVersion;
        }
    }
}
