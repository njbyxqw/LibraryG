using BettaSDK;
using BettaSDK.Profile;
using Game.TileV2.Editor.LevelEditor.Script.Config;
using Game.TileV2.Editor.LevelEditor.Script.Core;
using Game.TileV2.Editor.LevelEditor.Script.Core.Command.Interface;
using Game.TileV2.Editor.LevelEditor.Script.Dependency;
using Game.TileV2.Editor.LevelEditor.Script.Views.PopView;
using Game.TileV2.Scripts.Config.Game;
using Game.TileV2.Scripts.Entry;
using Game.TileV2.Scripts.Proxy;
using Game.TileV2.Scripts.UILogic;
using Module.Cameras;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using TransformUtils = Betta.Framework.TransformUtils;

namespace Game.TileV2.Editor.LevelEditor.Script.Views.TestControlView
{
    public class TestControlView : MonoBehaviour, ILevelEditorView
    {
        private ILevelEditorView _levelEditorViewImplementation;
        private Text _levelText;
        private Button _playBtn;
        
        private Button _evaluateBtn;
        
        private InputField _prePropInputField;
        private InputField _winStreakInputField;
        private InputField _rocketInputField;
        private InputField _robotInputField;
        private InputField _seedInputField;
        private InputField _goldInputField;

        private InputField _recordInput;
        private Button _recordPlayBtn;
        private Button _recordCopyBtn;
        private Button _recordClearBtn;
        
        public void OnInitialize()
        {
            _levelText = TransformUtils.Find<Text>(transform, "LevelInfo/Text");
            
            _evaluateBtn = TransformUtils.Find<Button>(transform, "EvelateBtn");
            _evaluateBtn.onClick.AddListener(OnEvaluateBtnClick);
            
            _playBtn = TransformUtils.Find<Button>(transform, "TestBtn");
            _playBtn.onClick.AddListener(OnPlayBtnClick);
            
            _prePropInputField = TransformUtils.Find<InputField>(transform,"PreProp/InputField"); 
            _prePropInputField.onEndEdit.AddListener(OnPropEditorEnd);
            
            _winStreakInputField = TransformUtils.Find<InputField>(transform,"WinStreak/InputField"); 
            _winStreakInputField.onEndEdit.AddListener(OnWinStreakEditorEnd);
            
            _rocketInputField = TransformUtils.Find<InputField>(transform,"Rocket/InputField"); 
            _rocketInputField.onEndEdit.AddListener(OnRocketEditorEnd);
            
            _robotInputField = TransformUtils.Find<InputField>(transform,"Robot/InputField"); 
            _robotInputField.onEndEdit.AddListener(OnRobotEditorEnd);
            
            _goldInputField = TransformUtils.Find<InputField>(transform,"Gold/InputField"); 
            _goldInputField.onEndEdit.AddListener(OnGoldEditorEnd);
            RefreshGoldInputFromData();
            
            _seedInputField = TransformUtils.Find<InputField>(transform,"Seed/InputField"); 
            _seedInputField.onEndEdit.AddListener(OnSeedEditorEnd);
            
            _recordInput = TransformUtils.Find<InputField>(transform,"RecordView/InputField"); 
            _recordInput.onEndEdit.AddListener(OnRecordEditEnd);
            _recordPlayBtn = TransformUtils.Find<Button>(transform, "RecordView/PlayBtn");
            _recordPlayBtn.onClick.AddListener(OnRecordPlayBtnClick);
            _recordCopyBtn = TransformUtils.Find<Button>(transform, "RecordView/CopyBtn");
            _recordCopyBtn.onClick.AddListener(OnRecordCopyBtnClick);
            _recordClearBtn = TransformUtils.Find<Button>(transform, "RecordView/ClearBtn");
            _recordClearBtn.onClick.AddListener(OnRecordClearBtnClick);
        }
        
        public void OnShow()
        {
            RefreshGoldInputFromData();
        }
        public void OnHide()
        {
            
        }
        public void OnLevelListLoaded()
        {
            
        }

        public void OnLevelConfigChanged()
        {
            RefreshInfo();
        }
        
        private void OnPropEditorEnd(string value)
        {
            _prePropInputField.text = value;
            string[] strList = value.Split(",");
            if (strList.Length == 2 )
            {
                var addOne = int.Parse(strList[0]);
                var magicWand = int.Parse(strList[1]);
                if (addOne > 0 )
                {
                    LevelEditorData.Instance.SetIsAddOne(true);
                }
                else {
                    LevelEditorData.Instance.SetIsAddOne(false);
                }
                
                if (magicWand > 0 )
                {
                    LevelEditorData.Instance.SetIsMagicWand(true);
                }else{
                    LevelEditorData.Instance.SetIsMagicWand(false);
                }
                
            }
        }
        
        private void OnWinStreakEditorEnd(string value)
        {
            _winStreakInputField.text = value;  
            var count = int.Parse(value);
            LevelEditorData.Instance.SetWinStreakTimes(count);
        }
        
        private void OnRocketEditorEnd(string value)
        {
            _rocketInputField.text = value;  
            var count = int.Parse(value);
            if (count == 3)
            {
                // RocketVL: 火箭牌 + 闪电球特效
                LevelEditorData.Instance.SetRocketMode(3);
                Debug.Log($"[RocketVL] Editor set RocketMode=3, IsRocket={LevelEditorData.Instance.IsRocket}");
            }
            else if (count > 0 )
            {
                LevelEditorData.Instance.SetRocketMode(0);
                LevelEditorData.Instance.SetIsRocket(true);
            }
            else
            {
                LevelEditorData.Instance.SetRocketMode(0);
                LevelEditorData.Instance.SetIsRocket(false);
            }
        }
        
        private void OnRobotEditorEnd(string value)
        {
            _robotInputField.text = value;  
            var count = int.Parse(value);
            LevelEditorData.Instance.SetAILevel(count);
        }
        
        private void RefreshGoldInputFromData()
        {
            if (_goldInputField == null) return;
            _goldInputField.text = LevelEditorData.Instance.GoldCount.ToString();
        }
        
        private void OnGoldEditorEnd(string value)
        {
            _goldInputField.text = value;
            const int useLevelExcelGold = -1;
            var count = useLevelExcelGold;
            if (!string.IsNullOrEmpty(value) && int.TryParse(value, out var parsedCount))
            {
                count = parsedCount;
            }
            LevelEditorData.Instance.SetGoldCount(count);
        }
        
        private void OnSeedEditorEnd(string value)
        {
            _robotInputField.text = value;  
            var count = int.Parse(value);
            LevelEditorData.Instance.SetLogicRandomSeed(count);
        }

        private void RefreshInfo()
        {
            var groupName = LevelListDataManager.Instance.GroupDirList[LevelDataManager.Instance.RootGroupId - 1].RootGroupName;
            var groupIndexName = LevelListDataManager.Instance.GroupDirList[LevelDataManager.Instance.RootGroupId - 1]
                .LevelGroupNames[LevelDataManager.Instance.LevelGroupId -1];
            _levelText.text = groupName + "_" + groupIndexName + ":"  + LevelDataManager.Instance.LevelFileName;
        }

        public void OnDisposed()
        {
            
        }

        public void OnEventHandle(CommandType type, object data)
        {
            if (type == CommandType.AddTile 
                ||type == CommandType.RemoveTile
                ||type == CommandType.ModifyTile
                ||type == CommandType.AddPile 
                ||type == CommandType.RemovePile
                ||type == CommandType.ModifyPile)
            {
                RefreshInfo();
            }
        }

        private void OnPlayBtnClick()
        {
            if (LevelDataManager.Instance.CurrentLevelConfig != null && LevelDataManager.Instance.CurrentLevelConfig.TileTypes.Count == 0 )
            {
                Debug.LogError("花色配置为空");
                return;
            }
            ProfileHub.Instance.GetProfile<ProfilePlayerInfo>().Level = LevelDataManager.Instance.LevelId;
            //SceneManager.LoadSceneAsync("TileMatchGameV2", LoadSceneMode.Additive);
            LevelEditorData.Instance.SetCurLevelConfig(LevelDataManager.Instance.CurrentLevelConfig);
            LevelEditorData.Instance.SetIsFromLevelEditor(true);
            ViewUtil.SetGameViewResolution(1080, 1920);
            GameUILogic.Instance.SetProxy(new TileMatchV2Proxy(),null);
            
            var customData = new CustomData();
            customData.SetGameMode(GameMode.Trial);
            customData.SetLevelName(LevelDataManager.Instance.LevelFileName);
            customData.SetWinStreakTimes(LevelEditorData.Instance.WinStreakTimes);
            customData.SetIsAddOne(LevelEditorData.Instance.IsAddOne);
            customData.SetIsMagicWand(LevelEditorData.Instance.IsMagicWand);
            customData.SetIsRocket(LevelEditorData.Instance.IsRocket);
            if (LevelEditorData.Instance.RocketMode > 0)
            {
                customData.SetRocketMode(LevelEditorData.Instance.RocketMode);
            }
            Debug.Log($"[RocketVL] PlayBtn: IsRocket={LevelEditorData.Instance.IsRocket}, RocketMode={LevelEditorData.Instance.RocketMode}, CustomData.IsCanShowRocket={customData.IsCanShowRocket}, CustomData.RocketMode={customData.RocketMode}");
            customData.SetIsCanCollectGold(false);
            customData.SetGoldCountOverride(LevelEditorData.Instance.GoldCount);
            customData.SetLevelIdOverride(LevelDataManager.Instance.LevelId);
            customData.SetRandomStep(LevelEditorData.Instance.RandomStep);
            customData.SetRandomTimes(LevelEditorData.Instance.RandomTimes);
            customData.SetLevelConfig(LevelEditorData.Instance.LevelConfig);
            customData.SetLogicRandomSeed(LevelEditorData.Instance.LogicRandomSeed);
            
            var rankId = LevelEditorData.Instance.RankIdForDebug;
            if (rankId > 0)
            {
                TileMatchGame.SetPendingLevelDiffString(rankId.ToString());
            }
            else
            {
                TileMatchGame.SetPendingLevelDiffString(null);
            }
            GameUILogic.Instance.SetCustomData(customData);
            
            GameUILogic.Instance.SetEditorOperation(new GameUILogicEditorOperation());
            
            ResourceHub.LoadSceneASync("Assets/Res/Scenes/EditorInitScene.unity", (result) =>
            {
                CameraModule.ClearInstance();
            },null,false);
        }
        
        private void OnEvaluateBtnClick() 
        {
            AssetDatabase.Refresh();
            LevelEditorViewManager.Instance.Open<LevelBotEntryView>();
        }
        
        private void OnRecordEditEnd(string value)
        {
            _recordInput.text = value;
            TileMatchGame.SetRecordString(value);
        }

        private void OnRecordPlayBtnClick()
        {
            OnPlayBtnClick();
        }
        
        private void OnRecordCopyBtnClick()
        {
            var recordString = TileMatchGame.GetLevelRecordStringFromDisk();
            GameExtend.CopyToClipboard(recordString);
        }
        
        private void OnRecordClearBtnClick()
        {
            _recordInput.text = "";
            TileMatchGame.SetRecordString("");
        }
    }
}
