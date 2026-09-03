using System.Threading;
using System.Threading.Tasks;
using Cysharp.Threading.Tasks;
using Game.TileShared.Scripts.GameCore.DomainEvent;
using Game.TileV2.Scripts.Config.Behaviours.Action;
using Game.TileV2.Scripts.Config.Behaviours.Event;
using Game.TileV2.Scripts.Config.Tile;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Behaviours.Action;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Behaviours.Action.Implementation;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Data;
using Game.TileV2.Scripts.GameCore.View.GameView;
using Game.TileV2.Scripts.GameCore.View.Interface;
using UnityEngine;
using UnityEngine.Scripting;
using EventType = Game.TileV2.Scripts.Config.Behaviours.Event.EventType;

namespace Game.TileV2.Scripts.GameCore.Application.ActionInvoker.Implementation
{
    [Preserve]
    public class PrepareChainedAttackActionInvoker : BaseActionInvoker
    {
        public PrepareChainedAttackActionInvoker(ITileMatchViewController viewController) : base(viewController)
        {
        }

        public override ActionType ActionType { get; } = ActionType.PrepareChainedAttack;

        public override async UniTask ProcessAsync(ActionResult actionResult, CancellationToken cancellationToken)
        {
            if (actionResult.Data is ChainedAttackActionData data && data.Data is TileData tileData)
            {
                Debug.Log($"[RocketVL] PrepareChainedAttackInvoker hit, TileType={tileData.TileType}");
                
                var controllerType = ResolveControllerType(tileData);
                
                Debug.Log($"[RocketVL] Resolved controllerType={controllerType}");

                if (controllerType != CustomViewActionControllerType.NotDefined)
                {
                    var controller = ViewController.GetViewActionController(controllerType);
                    Debug.Log($"[RocketVL] Got controller: {controller != null}, type={controller?.Type}");
                    
                    if (controller != null)
                    {
                        await controller.DoAction(data).AttachExternalCancellation(cancellationToken);
                    }
                }

                DomainEventBus.PublishForEnumKey(EventType.AfterAttack);
            }

            await Task.CompletedTask;
        }

        private CustomViewActionControllerType ResolveControllerType(TileData tileData)
        {
            bool isRocket = tileData.TileType == TileType.Rocket;
            bool isGameView = ViewController is TileMatchViewController;
            int rocketMode = 0;
            
            if (isGameView)
            {
                var tileMatchVC = (TileMatchViewController)ViewController;
                var db = tileMatchVC.DataBridge;
                rocketMode = db != null ? db.RocketMode : -1;
            }
            
            Debug.Log($"[RocketVL] Resolve: isRocket={isRocket}, isGameView={isGameView}, rocketMode={rocketMode}, ViewControllerType={ViewController.GetType().Name}");
            
            if (isRocket && rocketMode == 3)
            {
                Debug.Log("[RocketVL] ROUTING TO RocketVLLighting!");
                return CustomViewActionControllerType.RocketVLLighting;
            }

            var fallback = ViewController.GetViewActionControllerType(tileData.TileType, ActionType);
            Debug.Log($"[RocketVL] Fallback to: {fallback}");
            return fallback;
        }
    }
}
