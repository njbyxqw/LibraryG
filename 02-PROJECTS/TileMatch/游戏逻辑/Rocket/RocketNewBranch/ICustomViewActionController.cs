using System.Collections.Generic;
using System.Threading;
using Cysharp.Threading.Tasks;

namespace Game.TileV2.Scripts.GameCore.View.Interface
{

    public abstract class CustomViewActionData
    {

    }


    public enum CustomViewActionControllerType
    {
        NotDefined = 0,
        LevelCollect,
        RocketPrepare,
        VolcanoPrepare,
        ButterflyCreate,
        MagicBoxEject,
        MagicBoxRefresh,
        ShellBoxEject,
        ShellBoxRefresh,
        PropLighting,
        PropMagicWand,
        PropShuffle,
        PropAddExtraBarCell,
        PropAutoMatch,
        MultiTilesAdd,
        TransformSequence,
        FlipRefresh,
        JokerFlipTransformSequence,
        JokerFlipRefresh,
        SlotMachineRefresh,
        SlotMachineTransformSequence,
        CardBoxRefresh,
        LightBulbRefresh,
        SuitCaseRefresh,
        Mystery,
        SwitchSetHighlight,
        ThiefEject,
        ThiefRefresh,
        ThiefEjectAllSequenceTo,
        PickaxePrepare,
        CandyBottleTransformTiles,
        RocketVLLighting,
    }

    public interface ICustomViewActionController
    {
        public CustomViewActionControllerType Type { get; }

        public CancellationTokenSource CancellationTokenSource { get; }
        public Queue<ICustomViewAction> ActionQueue { get; }

        public bool Running => false;

        public void OnControllerInit();
        public void OnControllerUpdate(float deltaTime, float elapsedTime);
        public void OnControllerDispose();

        public UniTask DoAction(object data);
    }
}
