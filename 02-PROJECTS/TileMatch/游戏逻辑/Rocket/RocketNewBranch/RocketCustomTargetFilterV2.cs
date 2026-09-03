using System;
using System.Collections.Generic;
using Game.TileV2.Scripts.Config.Tile;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Entity;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Services;
using Game.TileV2.Scripts.GameCore.Logic.Interface;

namespace Game.TileV2.Scripts.GameCore.Logic.GameLogic.Filter
{
    public class RocketCustomTargetFilterV2 : TargetFilter
    {
        public override CustomTargetFilterType FilterType => CustomTargetFilterType.Rocket;

        protected readonly Dictionary<TileType, int> _typeCountMap = new();

        public override List<Tile> FilterTiles(
            RandomService randomService,
            int targetCount,
            IReadOnlyList<Tile> highlightPool,
            IReadOnlyList<Tile> visiblePool,
            IReadOnlyList<Tile> notVisiblePool,
            IReadOnlyList<Tile> barPool,
            IReadOnlyList<Tile> overBarPool,
            Func<Tile, bool> eligible = null)
        {
            var targetTiles = new HashSet<Tile>();
            var processedTiles = new HashSet<Tile>();
            
            int requestedTarget = targetCount > 0 ? targetCount : 3;
            int groupsNeeded = (requestedTarget + 2) / 3;
            int collectedGroupCount = 0;
            
            for (int round = 0; round < 100 && collectedGroupCount < groupsNeeded; round++)
            {
                var roundProcessedTiles = new HashSet<Tile>();
                var roundSelectedTiles = new HashSet<Tile>();
                
                bool hasSelected = SelectTileGroup(
                    randomService,
                    highlightPool,
                    visiblePool,
                    notVisiblePool,
                    barPool,
                    overBarPool,
                    roundProcessedTiles,
                    roundSelectedTiles,
                    targetTiles,
                    processedTiles,
                    eligible);
                
                if (roundProcessedTiles.Count > 0)
                {
                    foreach (var tile in roundProcessedTiles)
                    {
                        processedTiles.Add(tile);
                    }
                    continue;
                }
                
                if (hasSelected)
                {
                    if (roundSelectedTiles.Count == 3)
                    {
                        foreach (var tile in roundSelectedTiles)
                        {
                            targetTiles.Add(tile);
                        }
                        collectedGroupCount++;
                        continue;
                    }
                }
                
                if (roundSelectedTiles.Count > 0)
                {
                    foreach (var tile in roundSelectedTiles)
                    {
                        processedTiles.Add(tile);
                    }
                    continue;
                }
                
                break;
            }
            
            int currentCount = targetTiles.Count;
            if (currentCount < requestedTarget)
            {
                int needCount = requestedTarget - currentCount;
                int rocketGroupsNeeded = (needCount + 2) / 3;
                
                CollectRocketTiles(
                    randomService,
                    rocketGroupsNeeded,
                    highlightPool,
                    visiblePool,
                    notVisiblePool,
                    barPool,
                    overBarPool,
                    targetTiles,
                    processedTiles,
                    eligible);
            }
            
            return new List<Tile>(targetTiles);
        }
        
        private bool SelectTileGroup(
            RandomService randomService,
            IReadOnlyList<Tile> highlightPool,
            IReadOnlyList<Tile> visiblePool,
            IReadOnlyList<Tile> notVisiblePool,
            IReadOnlyList<Tile> barPool,
            IReadOnlyList<Tile> overBarPool,
            HashSet<Tile> roundProcessedTiles,
            HashSet<Tile> roundSelectedTiles,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles,
            Func<Tile, bool> eligible)
        {
            var availableTilesByPriority = GetAvailableTilesByPriority(
                highlightPool, barPool, overBarPool, targetTiles, processedTiles, eligible);
            
            foreach (var availableTiles in availableTilesByPriority)
            {
                if (availableTiles.Count == 0) continue;
                
                var baseTile = SelectTileTypeWithMostCount(availableTiles);
                int requiredMatchCount = GetRequiredMatchCount(baseTile);
                
                CollectSameTypeFromPools(
                    baseTile.TileData.TileType,
                    requiredMatchCount,
                    roundSelectedTiles,
                    targetTiles,
                    processedTiles,
                    eligible,
                    highlightPool,
                    visiblePool,
                    notVisiblePool,
                    barPool,
                    overBarPool);
                
                if (roundSelectedTiles.Count == requiredMatchCount)
                {
                    return true;
                }
                
                if (roundSelectedTiles.Count > 0)
                {
                    foreach (var tile in roundSelectedTiles)
                    {
                        roundProcessedTiles.Add(tile);
                    }
                    roundSelectedTiles.Clear();
                }
            }
            
            var allAvailableTiles = new List<Tile>();
            foreach (var availableTiles in availableTilesByPriority)
            {
                allAvailableTiles.AddRange(availableTiles);
            }
            
            if (allAvailableTiles.Count == 0)
            {
                var allTiles = new List<Tile>();
                if (highlightPool != null) allTiles.AddRange(highlightPool);
                if (barPool != null) allTiles.AddRange(barPool);
                if (overBarPool != null) allTiles.AddRange(overBarPool);
                
                foreach (var tile in allTiles)
                {
                    if (!targetTiles.Contains(tile) && !processedTiles.Contains(tile))
                    {
                        roundProcessedTiles.Add(tile);
                    }
                }
            }
            
            return false;
        }
        
        protected virtual List<List<Tile>> GetAvailableTilesByPriority(
            IReadOnlyList<Tile> highlightPool,
            IReadOnlyList<Tile> barPool,
            IReadOnlyList<Tile> overBarPool,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles,
            Func<Tile, bool> eligible)
        {
            var availableHighlightTiles = GetAvailableTiles(highlightPool, targetTiles, processedTiles, eligible);
            var availableBarTiles = GetAvailableTiles(barPool, targetTiles, processedTiles, eligible);
            var availableOverBarTiles = GetAvailableTiles(overBarPool, targetTiles, processedTiles, eligible);
            
            var resultPools = new List<List<Tile>>
            {
                availableHighlightTiles,
                availableBarTiles,
                availableOverBarTiles,
            };
            
            return resultPools;
        }
        
        protected List<Tile> GetAvailableTiles(
            IReadOnlyList<Tile> pool,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles,
            Func<Tile, bool> eligible)
        {
            var availableList = new List<Tile>();
            
            if (pool == null) return availableList;
            
            foreach (var tile in pool)
            {
                if (targetTiles.Contains(tile) || processedTiles.Contains(tile))
                {
                    continue;
                }
                
                if (IsAvailable(tile, eligible))
                {
                    availableList.Add(tile);
                }
            }
            
            return availableList;
        }
        
        protected virtual bool IsAvailable(Tile tile, Func<Tile, bool> eligible)
        {
            if (tile == null) return false;
            
            if (!IsTileGroupAvailable(tile))
            {
                return false;
            }

            if (IsSpecialTileExcluded(tile))
            {
                return false;
            }

            if (tile.TileData.LockState == LockState.Locked)
            {
                return false;
            }
            
            if (eligible != null && !eligible(tile))
            {
                return false;
            }
            
            return true;
        }

        protected virtual bool IsTileGroupAvailable(Tile tile)
        {
            return tile.TileType.GetTileGroup() != TileGroup.Blocker;
        }

        protected virtual bool IsSpecialTileExcluded(Tile tile)
        {
            return tile.TileType == TileType.CandyBottle;
        }
        
        private int GetRequiredMatchCount(Tile baseTile)
        {
            int required = 3;
            if (baseTile.TileConfig is { MatchCount: > 0 })
            {
                required = baseTile.TileConfig.MatchCount;
            }
            
            return required;
        }

        protected virtual Tile SelectTileTypeWithMostCount(List<Tile> availableList)
        {
            _typeCountMap.Clear();
            
            foreach (var tile in availableList)
            {
                _typeCountMap.TryAdd(tile.TileType, 0);
                _typeCountMap[tile.TileType]++;
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
        
        private void CollectSameTypeFromPools(
            TileType tileType,
            int requiredCount,
            HashSet<Tile> selectedTiles,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles,
            Func<Tile, bool> eligible,
            IReadOnlyList<Tile> highlightPool,
            IReadOnlyList<Tile> visiblePool,
            IReadOnlyList<Tile> notVisiblePool,
            IReadOnlyList<Tile> barPool,
            IReadOnlyList<Tile> overBarPool)
        {
            var allPools = new List<IReadOnlyList<Tile>>
            {
                highlightPool,
                visiblePool,
                notVisiblePool,
                overBarPool,
                barPool,
            };
            
            foreach (var pool in allPools)
            {
                if (selectedTiles.Count >= requiredCount) break;
                
                CollectSameTypeFromList(tileType, pool, requiredCount, selectedTiles, targetTiles, processedTiles, eligible);
            }
        }
        
        private void CollectSameTypeFromList(
            TileType tileType,
            IReadOnlyList<Tile> sourceList,
            int requiredCount,
            HashSet<Tile> selectedTiles,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles,
            Func<Tile, bool> eligible)
        {
            if (sourceList == null) return;
            
            foreach (var tile in sourceList)
            {
                if (selectedTiles.Count >= requiredCount) break;
                
                if (tile.TileType == tileType)
                {
                    if (targetTiles.Contains(tile) || processedTiles.Contains(tile))
                    {
                        continue;
                    }
                    
                    if (IsAvailable(tile, eligible))
                    {
                        selectedTiles.Add(tile);
                    }
                }
            }
        }
        
        private void CollectRocketTiles(
            RandomService randomService,
            int rocketGroupsNeeded,
            IReadOnlyList<Tile> highlightPool,
            IReadOnlyList<Tile> visiblePool,
            IReadOnlyList<Tile> notVisiblePool,
            IReadOnlyList<Tile> barPool,
            IReadOnlyList<Tile> overBarPool,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles,
            Func<Tile, bool> eligible)
        {
            var allPools = new List<IReadOnlyList<Tile>>
            {
                highlightPool,
                visiblePool,
                notVisiblePool,
                overBarPool,
                barPool,
            };
            
            var availableRockets = new List<Tile>();
            
            foreach (var pool in allPools)
            {
                if (pool == null) continue;
                
                foreach (var tile in pool)
                {
                    if (tile == null) continue;
                    
                    if (tile.TileType == TileType.Rocket)
                    {
                        if (ShouldSkipFallbackRocket(tile, targetTiles, processedTiles))
                        {
                            continue;
                        }
                        
                        if (tile.TileData.LockState == LockState.Locked)
                        {
                            continue;
                        }
                        
                        if (eligible != null && !eligible(tile))
                        {
                            continue;
                        }
                        
                        availableRockets.Add(tile);
                    }
                }
            }
            
            int collectedGroups = 0;
            int index = 0;
            
            while (collectedGroups < rocketGroupsNeeded && index < availableRockets.Count)
            {
                int groupSize = 0;
                var groupTiles = new List<Tile>();
                
                while (groupSize < 3 && index < availableRockets.Count)
                {
                    groupTiles.Add(availableRockets[index]);
                    groupSize++;
                    index++;
                }
                
                if (groupSize == 3)
                {
                    foreach (var tile in groupTiles)
                    {
                        targetTiles.Add(tile);
                    }
                    collectedGroups++;
                }
                else
                {
                    break;
                }
            }
        }

        protected virtual bool ShouldSkipFallbackRocket(
            Tile tile,
            HashSet<Tile> targetTiles,
            HashSet<Tile> processedTiles)
        {
            return targetTiles.Contains(tile);
        }
    }
}
