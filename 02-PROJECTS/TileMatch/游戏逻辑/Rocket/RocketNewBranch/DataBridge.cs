

namespace Game.TileV2.Scripts.GameCore.Logic.GameLogic.Module.Statistic
{
    public class DataBridge
    {
        public bool IsSelectAddOne { get; private set; }  // 战前选择 +1 
        public bool IsSelectMagicWand { get; private set; }  // 战前选择 魔法棒
        public bool IsCanCollectGold { get; private set; }  // 是否能收集金牌
        public bool IsCanShowRocket { get; private set; }  // 是否展示火箭
        public int WinStreakTimes { get; private set; }  // 连胜次数
        public int LevelRegulationHard { get; private set; } // 关卡调控难度
        public int RocketLuckyProbability { get; private set; }
        public int RocketMode { get; private set; }  // 0=默认, 3=RocketVL闪电球
        
        /// <summary>
        /// 百人 7 关活动状态。-1 表示未开启/无效。
        /// </summary>
        public int JungleState { get; private set; } = -1;

        public DataBridge(bool isSelectAddOne, 
            bool isSelectMagicWand, 
            bool isCanCollectGold, 
            bool isCanShowRocket, 
            int winStreakTimes, 
            int levelRegulationHard,
            int rocketLuckyProbability,
            int rocketMode = 0)
        {
            IsSelectAddOne = isSelectAddOne;
            IsSelectMagicWand = isSelectMagicWand;
            IsCanCollectGold = isCanCollectGold;
            IsCanShowRocket = isCanShowRocket;
            WinStreakTimes = winStreakTimes;
            LevelRegulationHard = levelRegulationHard;
            RocketLuckyProbability = rocketLuckyProbability;
            RocketMode = rocketMode;
        }
        
        public void UpdateDataBridge(
            bool isSelectAddOne, 
            bool isSelectMagicWand, 
            bool isCanCollectGold, 
            bool isCanShowRocket, 
            int winStreakTimes, 
            int levelRegulationHard,
            int rocketLuckyProbability,
            int rocketMode = 0)
        {
            IsSelectAddOne = isSelectAddOne;
            IsSelectMagicWand = isSelectMagicWand;
            IsCanCollectGold = isCanCollectGold;
            IsCanShowRocket = isCanShowRocket;
            WinStreakTimes = winStreakTimes;
            LevelRegulationHard = levelRegulationHard;
            RocketLuckyProbability = rocketLuckyProbability;
            RocketMode = rocketMode;
        }
        
        public void UpdateJungleState(int jungleState)
        {
            JungleState = jungleState;
        }
    }
}
