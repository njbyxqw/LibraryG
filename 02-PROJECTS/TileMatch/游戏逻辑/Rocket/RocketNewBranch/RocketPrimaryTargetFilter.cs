using System;
using System.Collections.Generic;
using Game.TileV2.Scripts.Config.Tile;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Entity;

namespace Game.TileV2.Scripts.GameCore.Logic.GameLogic.Filter
{
    public class RocketPrimaryTargetFilter : RocketCustomTargetFilterV2
    {
        public override CustomTargetFilterType FilterType => CustomTargetFilterType.RocketPrimary;

        /// <summary>
        /// 重写：将所有可用牌合并为单一优先级列表，使火箭牌与普通牌同优先级
        /// 原逻辑按 highlight > bar > overBar 分优先级，导致火箭牌难以被主流程选中
        /// </summary>
        protected override List<List<Tile>> GetAvailableTilesByPriority(
            IReadOnlyList<Tile> highlightPool,
            IReadOnlyList<Tile> barPool,
            IReadOnlyList<Tile> overBarPool,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles,
            Func<Tile, bool> eligible)
        {
            var allAvailableTiles = new List<Tile>();

            var availableHighlightTiles = GetAvailableTiles(highlightPool, targetTiles, processedTiles, eligible);
            var availableBarTiles = GetAvailableTiles(barPool, targetTiles, processedTiles, eligible);
            var availableOverBarTiles = GetAvailableTiles(overBarPool, targetTiles, processedTiles, eligible);

            allAvailableTiles.AddRange(availableHighlightTiles);
            allAvailableTiles.AddRange(availableBarTiles);
            allAvailableTiles.AddRange(availableOverBarTiles);

            // 返回单一优先级列表，使火箭牌与普通牌在同一次选择中竞争
            return new List<List<Tile>> { allAvailableTiles };
        }

        /// <summary>
        /// 重写：给火箭牌加权，使其在选牌时与普通牌同权重
        /// 原逻辑选"数量最多的类型"，火箭牌因数量少而几乎不会被选中
        /// </summary>
        protected override Tile SelectTileTypeWithMostCount(List<Tile> availableList)
        {
            _typeCountMap.Clear();

            foreach (var tile in availableList)
            {
                _typeCountMap.TryAdd(tile.TileType, 0);
                _typeCountMap[tile.TileType]++;
            }

            // 计算普通牌的最大数量
            int maxNormalCount = 0;
            foreach (var kvp in _typeCountMap)
            {
                if (kvp.Key != TileType.Rocket && kvp.Value > maxNormalCount)
                {
                    maxNormalCount = kvp.Value;
                }
            }

            // 给火箭牌加权：使其数量至少与最多的普通牌类型持平
            // 这样火箭牌在 SelectTileTypeWithMostCount 中有同等竞争力
            if (_typeCountMap.ContainsKey(TileType.Rocket) && maxNormalCount > 0)
            {
                _typeCountMap[TileType.Rocket] = Math.Max(_typeCountMap[TileType.Rocket], maxNormalCount);
            }

            TileType mostCommonType = TileType.Default;
            int maxCount = 0;

            foreach (var kvp in _typeCountMap)
            {
                if (kvp.Value > maxCount)
                {
                    maxCount = kvp.Value;
                    mostCommonType = kvp.Key;
                }
            }

            foreach (var t in availableList)
            {
                if (t.TileType == mostCommonType)
                {
                    return t;
                }
            }

            return availableList[0];
        }

        protected override bool IsTileGroupAvailable(Tile tile)
        {
            var tileGroup = tile.TileType.GetTileGroup();
            if (tileGroup == TileGroup.Blocker && tile.TileType != TileType.Rocket)
            {
                return false;
            }

            if (tileGroup == TileGroup.Collectable)
            {
                return false;
            }

            return true;
        }

        protected override bool IsSpecialTileExcluded(Tile tile)
        {
            return tile.TileType == TileType.Golden || tile.TileType == TileType.CandyBottle;
        }

        protected override bool ShouldSkipFallbackRocket(
            Tile tile,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles)
        {
            return targetTiles.Contains(tile) || processedTiles.Contains(tile);
        }
    }
}
