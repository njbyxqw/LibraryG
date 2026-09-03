using Newtonsoft.Json;
using UnityEngine.Scripting;

namespace Game.TileV2.Editor.LevelEditor.Script.Config
{
    public class LevelEditorConfig
    {

        [JsonProperty("LevelId")]
        public int LevelId;
        
        [JsonProperty("LevelName")]
        public string LevelName;
        
        [JsonProperty("GroupName")]
        public string GroupName;
        
        [JsonProperty("IsAddOne")]
        public bool IsAddOne;
        
        [JsonProperty("IsMagicWand")]
        public bool IsMagicWand;
        
        [JsonProperty("WinStreakTimes")]
        public int WinStreakTimes;
        
        [JsonProperty("IsRocket")]
        public bool IsRocket;

        [JsonProperty("RocketMode")]
        public int RocketMode;
        
        [JsonProperty("AILevel")]
        public int AILevel;
        
        [JsonProperty("RandomStep")]
        public int RandomStep;
        
        [JsonProperty("RandomTimes")]
        public int RandomTimes;
        
        
        [Preserve]
        public LevelEditorConfig()
        {
            
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
    }
}