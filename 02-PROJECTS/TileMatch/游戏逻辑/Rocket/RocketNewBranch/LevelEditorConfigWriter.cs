using System.IO;
using BettaSDK;
using Newtonsoft.Json;

namespace Game.TileV2.Editor.LevelEditor.Script.Config
{
    public class LevelEditorConfigWriter
    {
        private string GetResourcePath()
        {
            var jsonPath = "Assets/Game/TileV2/Config/LevelEditorConfig/LevelEditor.json";
            return jsonPath;   
        }
        public void Write(LevelEditorConfig levelEditorConfig)
        {
            
            string path = GetResourcePath();
            UtilsFile.Create(path);

            using var streamWriter = new StreamWriter(path);
            using var jsonWriter = new JsonTextWriter(streamWriter);
            
            jsonWriter.Formatting = Formatting.Indented;
                
            jsonWriter.WriteStartObject();

            jsonWriter.WritePropertyName("LevelId");
            jsonWriter.WriteValue(levelEditorConfig.LevelId);

            jsonWriter.WritePropertyName("LevelName");
            jsonWriter.WriteValue(levelEditorConfig.LevelName);
            
            jsonWriter.WritePropertyName("GroupName");
            jsonWriter.WriteValue(levelEditorConfig.GroupName);
            
            jsonWriter.WritePropertyName("IsAddOne");
            jsonWriter.WriteValue(levelEditorConfig.IsAddOne);
            
            jsonWriter.WritePropertyName("IsMagicWand");
            jsonWriter.WriteValue(levelEditorConfig.IsMagicWand);
            
            jsonWriter.WritePropertyName("WinStreakTimes");
            jsonWriter.WriteValue(levelEditorConfig.WinStreakTimes);
            
            jsonWriter.WritePropertyName("IsRocket");
            jsonWriter.WriteValue(levelEditorConfig.IsRocket);

            jsonWriter.WritePropertyName("RocketMode");
            jsonWriter.WriteValue(levelEditorConfig.RocketMode);
            
            jsonWriter.WritePropertyName("AILevel");
            jsonWriter.WriteValue(levelEditorConfig.AILevel);
            
            jsonWriter.WritePropertyName("RandomStep");
            jsonWriter.WriteValue(levelEditorConfig.RandomStep);
            
            jsonWriter.WritePropertyName("RandomTimes");
            jsonWriter.WriteValue(levelEditorConfig.RandomTimes);
            jsonWriter.WriteEndObject();
        }
    }
}