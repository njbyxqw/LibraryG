using System;
using System.Collections.Generic;
using Game.TileV2.Scripts.Config.Behaviours.Action;
using Game.TileV2.Scripts.Config.Prop;
using Game.TileV2.Scripts.Config.Tile;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.AutoMatch;
using Game.TileV2.Scripts.GameCore.View.Interface;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Rocket;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Pickaxe;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Volcano;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Butterfly;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.ExpendBarCell;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.LevelCollect;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Lighting;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.MagicBox;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.MagicWand;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.MultiTilesAdd;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.ShellBox;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Shuffle;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Flip;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.LightBulb;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.JokerFlip;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.SlotMachine;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Mystery;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.SuitCase;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.CardBox;
using Game.TileV2.Scripts.Config.Effect;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.CandyBottleTransformTiles;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Switch;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.Thief;
using Game.TileV2.Scripts.GameCore.View.GameView.Views.ViewActions.RocketVLLighting;

namespace Game.TileV2.Scripts.GameCore.View.GameView
{
    public partial class TileMatchViewController
    {
        private readonly Dictionary<CustomViewActionControllerType, ICustomViewActionController> _viewActions =
            new Dictionary<CustomViewActionControllerType, ICustomViewActionController>()
            {
                { CustomViewActionControllerType.LevelCollect, new LevelCollectViewActionController() },
                { CustomViewActionControllerType.RocketPrepare, new RocketViewCustomActionController() },
                { CustomViewActionControllerType.PickaxePrepare, new PickaxeViewCustomActionController() },
                { CustomViewActionControllerType.VolcanoPrepare, new VolcanoViewCustomActionController() },
                { CustomViewActionControllerType.ButterflyCreate, new ButterflyViewActionController() },
                { CustomViewActionControllerType.MagicBoxEject, new MagicBoxEjectViewActionController() },
                { CustomViewActionControllerType.MagicBoxRefresh, new MagicBoxRefreshViewActionController() },
                { CustomViewActionControllerType.ShellBoxEject, new ShellBoxEjectViewActionController() },
                { CustomViewActionControllerType.ShellBoxRefresh, new ShellBoxRefreshViewActionController() },
                { CustomViewActionControllerType.PropLighting, new LightingViewActionController() },
                { CustomViewActionControllerType.PropMagicWand, new MagicWandViewActionController() },
                { CustomViewActionControllerType.PropShuffle, new ShuffleViewActionController() },
                { CustomViewActionControllerType.PropAddExtraBarCell, new ExpendBarCellViewActionController() },
                { CustomViewActionControllerType.PropAutoMatch , new AutoMatchViewCustomActionController() },
                { CustomViewActionControllerType.MultiTilesAdd , new MultiTilesAddActionController() },
                { CustomViewActionControllerType.TransformSequence, new FlipTransformSequenceViewActionController() },
                { CustomViewActionControllerType.FlipRefresh, new FlipRefreshViewActionController() },
                { CustomViewActionControllerType.JokerFlipTransformSequence, new JokerFlipTransformSequenceViewActionController() },
                { CustomViewActionControllerType.JokerFlipRefresh, new JokerFlipRefreshViewActionController() },
                { CustomViewActionControllerType.SlotMachineRefresh, new SlotMachineRefreshViewActionController() },
                { CustomViewActionControllerType.SlotMachineTransformSequence, new SlotMachineTransformSequenceViewActionController() },
                { CustomViewActionControllerType.CardBoxRefresh, new CardBoxRefreshViewActionController() },
                { CustomViewActionControllerType.LightBulbRefresh, new LightBulbRefreshViewActionController() },
                { CustomViewActionControllerType.Mystery, new MysteryViewActionController() },
                { CustomViewActionControllerType.SuitCaseRefresh, new SuitCaseRefreshViewActionController() },
                { CustomViewActionControllerType.SwitchSetHighlight, new SwitchSetHighlightViewActionController() },
                { CustomViewActionControllerType.ThiefEject, new ThiefEjectViewActionController() },
                { CustomViewActionControllerType.ThiefRefresh, new ThiefRefreshViewActionController() },
                { CustomViewActionControllerType.ThiefEjectAllSequenceTo, new ThiefEjectAllSequenceToViewActionController() },
                { CustomViewActionControllerType.CandyBottleTransformTiles, new CandyBottleTransformTilesViewActionController() },
                { CustomViewActionControllerType.RocketVLLighting, new RocketVLLightningViewActionController() },
            };

        private readonly Dictionary<Enum, Dictionary<ActionType, CustomViewActionControllerType>> _enumToViewActionControllers =
            new ()
            {
                {
                    PropType.AutoMatch, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.AddTilesToBar, CustomViewActionControllerType.PropAutoMatch },
                    }
                },
                {
                    PropType.Shuffle, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.ShuffleTile, CustomViewActionControllerType.PropShuffle },
                    }
                },
                {
                    PropType.CloneTilesToOverBar, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.CreateTile, CustomViewActionControllerType.PropMagicWand },
                    }
                },
                {
                    PropType.AddExtraBarCell, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.ExpandBarCells, CustomViewActionControllerType.PropAddExtraBarCell },
                    }
                },
                {
                    PropType.Lighting, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.PrepareAttack, CustomViewActionControllerType.PropLighting },
                    }
                },
                {
                    PropType.MultiTilesAdd, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.AddTilesToBar, CustomViewActionControllerType.MultiTilesAdd },
                    }
                },
                {
                    TileType.Rocket, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.PrepareAttack, CustomViewActionControllerType.RocketPrepare },
                        { ActionType.PrepareChainedAttack, CustomViewActionControllerType.RocketPrepare },
                    }
                },
                {
                    TileType.Volcano, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.PrepareAttack, CustomViewActionControllerType.VolcanoPrepare },
                    }
                },
                {
                    TileType.Pickaxe1, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.PrepareAttack, CustomViewActionControllerType.PickaxePrepare },
                    }
                },
                {
                    TileType.Pickaxe2, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.PrepareAttack, CustomViewActionControllerType.PickaxePrepare },
                    }
                },
                {
                    TileType.Pickaxe3, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.PrepareAttack, CustomViewActionControllerType.PickaxePrepare },
                    }
                },
                {
                    TileType.Butterfly, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.CreateTile, CustomViewActionControllerType.ButterflyCreate },
                    }
                },
                {
                    TileType.MagicBox, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.MagicBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.MagicBoxRefresh },
                    }
                },
                {
                    TileType.Thief, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ThiefEject },
                        { ActionType.EjectAllSequenceTo, CustomViewActionControllerType.ThiefEjectAllSequenceTo },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ThiefRefresh },
                    }
                },
                {
                    TileType.ShellBoxUp, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ShellBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ShellBoxRefresh },
                    }
                },
                {
                    TileType.ShellBoxDown, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ShellBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ShellBoxRefresh },
                    }
                },
                {
                    TileType.ShellBoxLeft, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ShellBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ShellBoxRefresh },
                    }
                },
                {
                    TileType.ShellBoxRight, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ShellBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ShellBoxRefresh },
                    }
                },
                {
                    TileType.ShellBoxOpaqueUp, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ShellBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ShellBoxRefresh },
                    }
                },
                {
                    TileType.ShellBoxOpaqueDown, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ShellBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ShellBoxRefresh },
                    }
                },
                {
                    TileType.ShellBoxOpaqueLeft, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ShellBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ShellBoxRefresh },
                    }
                },
                {
                    TileType.ShellBoxOpaqueRight, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.EjectSequenceTo, CustomViewActionControllerType.ShellBoxEject },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.ShellBoxRefresh },
                    }
                },
                {
                    TileType.Flip, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.TransformSequence, CustomViewActionControllerType.TransformSequence },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.FlipRefresh },
                    }
                },
                {
                    TileType.JokerFlip, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.TransformSequence, CustomViewActionControllerType.JokerFlipTransformSequence },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.JokerFlipRefresh },
                    }
                },
                {
                    TileType.SlotMachine, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.TransformSequence, CustomViewActionControllerType.SlotMachineTransformSequence },
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.SlotMachineRefresh },
                    }
                },
                {
                    TileType.CardBox, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.CardBoxRefresh },
                    }
                },
                {
                  TileType.LightBulb, new Dictionary<ActionType, CustomViewActionControllerType>()
                  {
                      {ActionType.UpdateBatchState, CustomViewActionControllerType.LightBulbRefresh},
                  }
                },
                {
                    EffectType.Mystery, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.HandleForwardTileClick, CustomViewActionControllerType.Mystery },
                    }
                },
                {
                    TileType.SuitCaseHorizontal, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.SuitCaseRefresh },
                        { ActionType.RefreshSequenceState, CustomViewActionControllerType.SuitCaseRefresh },
                    }
                },
                {
                    TileType.SuitCaseVertical, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.UpdateSequenceState, CustomViewActionControllerType.SuitCaseRefresh },
                        { ActionType.RefreshSequenceState, CustomViewActionControllerType.SuitCaseRefresh },
                    }
                },
                {
                    TileType.SwitchHorizontal, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.SetSequenceTileHighlightByIndex, CustomViewActionControllerType.SwitchSetHighlight },
                    }
                },
                {
                    TileType.SwitchVertical, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        {
                            ActionType.SetSequenceTileHighlightByIndex, CustomViewActionControllerType.SwitchSetHighlight
                        },
                    }
                },
                {
                    TileType.CandyBottle, new Dictionary<ActionType, CustomViewActionControllerType>()
                    {
                        { ActionType.SelectAndTransformTiles, CustomViewActionControllerType.CandyBottleTransformTiles },
                    }
                }
            };

        #region 获取

        public CustomViewActionControllerType GetViewActionControllerType(Enum type, ActionType actionType)
        {
            if (_enumToViewActionControllers.TryGetValue(type, out var actionControllerTypes))
            {
                if (actionControllerTypes.TryGetValue(actionType, out var controllerType))
                {
                    return controllerType;
                }
            }

            return CustomViewActionControllerType.NotDefined;
        }

        public ICustomViewActionController GetViewActionController(CustomViewActionControllerType type)
        {
            return _viewActions.GetValueOrDefault(type);
        }

        #endregion
    }
}
