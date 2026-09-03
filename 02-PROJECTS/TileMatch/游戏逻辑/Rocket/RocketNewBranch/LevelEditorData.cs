using BettaSDK;
using Game.TileV2.Scripts.Config.Level;

namespace Game.TileV2.Editor.LevelEditor.Script.Config
{
    public class LevelEditorData : Singleton<LevelEditorData>
    {
        protected override void InitFirst()
        {
            InitData();
        }
        public bool IsFromLevelEditor { get; private set; }
        public int LevelId { get; private set; } = 1;
        public string LevelName{ get; private set; }

        public int RootGroupId { get; private set; } = 1;

        public int LevelGroupId { get; private set; } = 1;
        
        public int LayerIndex { get; private set; } = 1;
        
        public string GroupName{ get; private set; }
        public bool IsAddOne{ get; private set; }
        public bool IsMagicWand{ get; private set; }
        public int WinStreakTimes{ get; private set; }
        public bool IsRocket{ get; private set; }
        public int RocketMode { get; private set; }  // 0=默认, 3=RocketVL闪电球
        public int AILevel{ get; private set; }
        public int RandomStep { get; private set; } = 5;
        public int RandomTimes { get; private set; } = 5;
        
        public int GoldCount { get; private set; } = -1;
        
        public int LogicRandomSeed { get; private set; }
        
        public LevelConfig LevelConfig { get; private set; }

        public int RankIdForDebug { get; private set; }

        public bool UseDdaV2EvalAutoRankByLevelOrdinal { get; private set; } = true;

        public void SetIsFromLevelEditor(bool result)
        {
            IsFromLevelEditor = result;
        }

        public void SetLevelID(int levelId)
        {
            LevelId = levelId;
        }
        
        public void SetLevelName(string levelName)
        {
            LevelName = levelName;
        }
        
        public void SetGroupName(string groupName)
        {
            GroupName = groupName;
        }
        
        public void SetRootGroupId(int groupId)
        {
            RootGroupId = groupId;
        }
        
        public void SetLevelGroupId(int groupIndex)
        {
            LevelGroupId = groupIndex;
        }
        public void SetLayerIndex(int count)
        {
            LayerIndex = count;
        }
        
        public void SetIsAddOne(bool result)
        {
            IsAddOne = result;
        }
        public void SetIsMagicWand(bool result)
        {
            IsMagicWand = result;
        }
        public void SetWinStreakTimes(int count)
        {
            WinStreakTimes = count;
        }
        
        public void SetIsRocket(bool result)
        {
            IsRocket = result;
        }

        public void SetRocketMode(int mode)
        {
            RocketMode = mode;
            if (mode > 0)
            {
                IsRocket = true;
            }
        }
        
        public void SetRandomStep(int count)
        {
            RandomStep = count;
        }
        
        public void SetRandomTimes(int count)
        {
            RandomTimes = count;
        }
        
        public void SetAILevel(int count)
        {
            AILevel = count;
        }
        
        public void SetCurLevelConfig(LevelConfig levelConfig)
        {
            LevelConfig = levelConfig;
        }
        public void SetLogicRandomSeed(int logicRandomSeed)
        {
            LogicRandomSeed = logicRandomSeed;
        }
        
        public void SetGoldCount(int count)
        {
            GoldCount = count;
        }

        
        public void InitData()
        {
            LevelId = 1;
            LevelName = "";
            GroupName = "";
            IsAddOne = false;
            IsMagicWand = false;
            WinStreakTimes = 0;
            IsRocket = false;
            RocketMode = 0;
            AILevel = 1;
            RandomStep = 5;
            RandomTimes = 5;
            LayerIndex = 0;
            GoldCount = -1;
            LogicRandomSeed = 0;
            RankIdForDebug = 9;
            UseDdaV2EvalAutoRankByLevelOrdinal = true;
        }

        public void SetRankIdForDebug(int rankId)
        {
            RankIdForDebug = rankId;
        }

        public void SetUseDdaV2EvalAutoRankByLevelOrdinal(bool value)
        {
            UseDdaV2EvalAutoRankByLevelOrdinal = value;
        }
    }
}
