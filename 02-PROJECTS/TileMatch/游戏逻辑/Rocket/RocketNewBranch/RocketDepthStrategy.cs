using System;
using System.Collections.Generic;
using Game.TileShared.Scripts.Util;
using Game.TileV2.Scripts.Config.Tile;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Entity;
using Game.TileV2.Scripts.GameCore.Logic.GameLogic.Module.LevelDepth;

namespace Game.TileV2.Scripts.GameCore.Logic.GameLogic.Module.LevelRocket.Strategy
{
    public class RocketDepthStrategy : IRocketStrategy
    {
        private sealed class RocketCandidate
        {
            public Tile Tile;
            public TileType OriginalType;
            public int Depth;
        }

        private TileMatchGameContext _gameContext;
        private Dictionary<long, Tile> _tileDict;

        public void InvokeStrategy(Dictionary<long, Tile> tileDict, TileMatchGameContext gameContext)
        {
            _gameContext = gameContext;
            _tileDict = tileDict;
            ModifyTiles();
        }

        private void ModifyTiles()
        {
            var candidates = GetNormalCandidates();
            int normalGroupCount = candidates.Count / 3;
            int targetRocketGroupCount = GetRocketGroupCount(normalGroupCount);
            int currentRocketCount = CountCurrentRockets();
            if (currentRocketCount % 3 != 0)
            {
                LogUtil.LogError(
                    nameof(RocketDepthStrategy),
                    $"RocketDepthStrategy skipped: currentRocketCount:{currentRocketCount} is not divisible by 3");
                return;
            }

            int currentRocketGroupCount = currentRocketCount / 3;
            int addRocketGroupCount = Math.Max(0, targetRocketGroupCount - currentRocketGroupCount);

            LogUtil.Log(
                nameof(RocketDepthStrategy),
                $"RocketDepthStrategy normalGroupCount:{normalGroupCount} targetRocketGroupCount:{targetRocketGroupCount} currentRocketGroupCount:{currentRocketGroupCount}");

            if (addRocketGroupCount <= 0 || candidates.Count <= 0)
            {
                return;
            }

            FillCandidateDepths(candidates);
            candidates.Sort(CompareCandidateDepth);

            var selectedCandidates = SelectRocketCandidates(candidates, addRocketGroupCount);
            for (int i = 0; i < selectedCandidates.Count; i++)
            {
                _gameContext.TileService.ModifyTile(selectedCandidates[i].Tile, TileType.Rocket);
            }

            EnsureHighlightNotAllRocket(candidates, selectedCandidates);
            LogUtil.Log(nameof(RocketDepthStrategy), $"RocketDepthStrategy converted:{selectedCandidates.Count}");
        }

        private List<RocketCandidate> GetNormalCandidates()
        {
            var candidates = new List<RocketCandidate>();
            foreach (var kvp in _tileDict)
            {
                var tile = kvp.Value;
                if (!IsNormalCandidate(tile))
                {
                    continue;
                }

                candidates.Add(new RocketCandidate
                {
                    Tile = tile,
                    OriginalType = tile.TileType,
                    Depth = 1
                });
            }

            return candidates;
        }

        private static bool IsNormalCandidate(Tile tile)
        {
            if (tile == null)
            {
                return false;
            }

            if (!tile.TileData.FromRandom)
            {
                return false;
            }

            if (tile.TileType == TileType.Rocket || tile.TileType == TileType.Golden ||
                tile.TileType == TileType.CandyBottle)
            {
                return false;
            }

            var tileGroup = tile.TileData.TileType.GetTileGroup();
            if (tileGroup == TileGroup.Blocker || tileGroup == TileGroup.Collectable)
            {
                return false;
            }

            return true;
        }

        private static int GetRocketGroupCount(int normalGroupCount)
        {
            int rocketGroupCount = 4;
            if (normalGroupCount > 25)
            {
                rocketGroupCount += (normalGroupCount - 25) / 5;
            }

            return rocketGroupCount;
        }

        private void FillCandidateDepths(List<RocketCandidate> candidates)
        {
            var tiles = new List<Tile>(candidates.Count);
            for (int i = 0; i < candidates.Count; i++)
            {
                tiles.Add(candidates[i].Tile);
            }

            var depthByTileId = TileDepthComputer.ComputeTileDepths(_gameContext.Board, tiles);
            for (int i = 0; i < candidates.Count; i++)
            {
                if (depthByTileId.TryGetValue(candidates[i].Tile.Id, out int depth))
                {
                    candidates[i].Depth = depth;
                }
            }
        }

        private static int CompareCandidateDepth(RocketCandidate left, RocketCandidate right)
        {
            int depthCompare = left.Depth.CompareTo(right.Depth);
            if (depthCompare != 0)
            {
                return depthCompare;
            }

            int zCompare = left.Tile.Position.z.CompareTo(right.Tile.Position.z);
            if (zCompare != 0)
            {
                return zCompare;
            }

            return left.Tile.Id.CompareTo(right.Tile.Id);
        }

        private List<RocketCandidate> SelectRocketCandidates(List<RocketCandidate> candidates, int rocketGroupCount)
        {
            var buckets = SplitByDepthBuckets(candidates);
            var selectedCandidates = new List<RocketCandidate>(rocketGroupCount * 3);
            var selectedIds = new HashSet<long>();

            int shallowGroupCount = _gameContext.DataBridge.WinStreakTimes <= 2 ? 2 : 1;
            shallowGroupCount = Math.Min(shallowGroupCount, rocketGroupCount);
            int middleGroupCount = rocketGroupCount - shallowGroupCount;

            CollectGroups(selectedCandidates, selectedIds, buckets, shallowGroupCount, 0);
            CollectGroups(selectedCandidates, selectedIds, buckets, middleGroupCount, 1);

            int selectedGroupCount = selectedCandidates.Count / 3;
            if (selectedGroupCount < rocketGroupCount)
            {
                CollectGroups(selectedCandidates, selectedIds, buckets, rocketGroupCount - selectedGroupCount, 0);
            }

            return selectedCandidates;
        }

        private static List<List<RocketCandidate>> SplitByDepthBuckets(List<RocketCandidate> candidates)
        {
            int shallowEnd = (candidates.Count * 30 + 99) / 100;
            int middleEnd = (candidates.Count * 60 + 99) / 100;
            var buckets = new List<List<RocketCandidate>>
            {
                new(),
                new(),
                new()
            };

            for (int i = 0; i < candidates.Count; i++)
            {
                if (i < shallowEnd)
                {
                    buckets[0].Add(candidates[i]);
                }
                else if (i < middleEnd)
                {
                    buckets[1].Add(candidates[i]);
                }
                else
                {
                    buckets[2].Add(candidates[i]);
                }
            }

            return buckets;
        }

        private void CollectGroups(
            List<RocketCandidate> selectedCandidates,
            HashSet<long> selectedIds,
            List<List<RocketCandidate>> buckets,
            int groupCount,
            int startBucketIndex)
        {
            if (groupCount <= 0)
            {
                return;
            }

            int targetGroupCount = selectedCandidates.Count / 3 + groupCount;
            for (int bucketIndex = startBucketIndex; bucketIndex < buckets.Count; bucketIndex++)
            {
                CollectGroupsFromBucket(selectedCandidates, selectedIds, buckets[bucketIndex], targetGroupCount, false);
                if (selectedCandidates.Count / 3 >= targetGroupCount)
                {
                    return;
                }
            }

            for (int bucketIndex = 0; bucketIndex < startBucketIndex; bucketIndex++)
            {
                CollectGroupsFromBucket(selectedCandidates, selectedIds, buckets[bucketIndex], targetGroupCount, false);
                if (selectedCandidates.Count / 3 >= targetGroupCount)
                {
                    return;
                }
            }
        }

        private void CollectGroupsFromBucket(
            List<RocketCandidate> selectedCandidates,
            HashSet<long> selectedIds,
            List<RocketCandidate> bucket,
            int targetGroupCount,
            bool requireNonHighlight)
        {
            while (selectedCandidates.Count / 3 < targetGroupCount)
            {
                var groupTypes = GetSelectableGroupTypes(bucket, selectedIds, requireNonHighlight);
                if (groupTypes.Count <= 0)
                {
                    return;
                }

                var selectedType = groupTypes[_gameContext.RandomService.Range(0, groupTypes.Count)];
                if (!TryCollectRandomGroupByType(selectedCandidates, selectedIds, bucket, selectedType, requireNonHighlight))
                {
                    return;
                }
            }
        }

        private static List<TileType> GetSelectableGroupTypes(
            List<RocketCandidate> bucket,
            HashSet<long> selectedIds,
            bool requireNonHighlight)
        {
            var countsByType = new Dictionary<TileType, int>();
            var groupTypes = new List<TileType>();
            for (int i = 0; i < bucket.Count; i++)
            {
                var candidate = bucket[i];
                if (!IsSelectableCandidate(candidate, selectedIds, requireNonHighlight))
                {
                    continue;
                }

                if (!countsByType.TryGetValue(candidate.OriginalType, out int count))
                {
                    count = 0;
                }

                count++;
                countsByType[candidate.OriginalType] = count;
                if (count == 3)
                {
                    groupTypes.Add(candidate.OriginalType);
                }
            }

            return groupTypes;
        }

        private void EnsureHighlightNotAllRocket(
            List<RocketCandidate> candidates,
            List<RocketCandidate> selectedCandidates)
        {
            var highlightTiles = _gameContext.Board.GetAllTileListByVisibility(EntityVisibility.Highlight);
            if (highlightTiles.Count <= 0 || !IsAllHighlightRocket(highlightTiles))
            {
                return;
            }

            var selectedIds = new HashSet<long>();
            for (int i = 0; i < selectedCandidates.Count; i++)
            {
                selectedIds.Add(selectedCandidates[i].Tile.Id);
            }

            int highlightGroupStart = GetSelectedHighlightGroupStart(selectedCandidates);
            if (highlightGroupStart < 0)
            {
                LogUtil.Log(
                    nameof(RocketDepthStrategy),
                    "RocketDepthStrategy skipped highlight replacement: no selected highlight group");
                return;
            }

            var replacementGroup = new List<RocketCandidate>(3);
            var replacementSelectedIds = new HashSet<long>(selectedIds);
            if (!TryCollectReplacementGroup(candidates, replacementSelectedIds, replacementGroup))
            {
                return;
            }

            for (int i = 0; i < replacementGroup.Count; i++)
            {
                _gameContext.TileService.ModifyTile(replacementGroup[i].Tile, TileType.Rocket);
            }

            for (int i = 0; i < 3; i++)
            {
                var candidate = selectedCandidates[highlightGroupStart + i];
                _gameContext.TileService.ModifyTile(candidate.Tile, candidate.OriginalType);
            }
        }

        private bool TryCollectReplacementGroup(
            List<RocketCandidate> candidates,
            HashSet<long> selectedIds,
            List<RocketCandidate> replacementGroup)
        {
            var groupTypes = GetSelectableGroupTypes(candidates, selectedIds, true);
            if (groupTypes.Count <= 0)
            {
                return false;
            }

            var selectedType = groupTypes[_gameContext.RandomService.Range(0, groupTypes.Count)];
            return TryCollectRandomGroupByType(replacementGroup, selectedIds, candidates, selectedType, true);
        }

        private static int GetSelectedHighlightGroupStart(List<RocketCandidate> selectedCandidates)
        {
            for (int groupStart = 0; groupStart + 2 < selectedCandidates.Count; groupStart += 3)
            {
                for (int i = 0; i < 3; i++)
                {
                    if (selectedCandidates[groupStart + i].Tile.TileData.EntityVisibility == EntityVisibility.Highlight)
                    {
                        return groupStart;
                    }
                }
            }

            return -1;
        }

        private bool TryCollectRandomGroupByType(
            List<RocketCandidate> selectedCandidates,
            HashSet<long> selectedIds,
            List<RocketCandidate> bucket,
            TileType originalType,
            bool requireNonHighlight)
        {
            for (int groupIndex = 0; groupIndex < 3; groupIndex++)
            {
                int selectableCount = CountSelectableCandidates(bucket, selectedIds, originalType, requireNonHighlight);
                if (selectableCount <= 0)
                {
                    return false;
                }

                int selectedOffset = _gameContext.RandomService.Range(0, selectableCount);
                for (int i = 0; i < bucket.Count; i++)
                {
                    var candidate = bucket[i];
                    if (!IsSelectableCandidate(candidate, selectedIds, requireNonHighlight) ||
                        candidate.OriginalType != originalType)
                    {
                        continue;
                    }

                    if (selectedOffset > 0)
                    {
                        selectedOffset--;
                        continue;
                    }

                    selectedIds.Add(candidate.Tile.Id);
                    selectedCandidates.Add(candidate);
                    break;
                }
            }

            return true;
        }

        private static int CountSelectableCandidates(
            List<RocketCandidate> bucket,
            HashSet<long> selectedIds,
            TileType originalType,
            bool requireNonHighlight)
        {
            int count = 0;
            for (int i = 0; i < bucket.Count; i++)
            {
                var candidate = bucket[i];
                if (candidate.OriginalType == originalType &&
                    IsSelectableCandidate(candidate, selectedIds, requireNonHighlight))
                {
                    count++;
                }
            }

            return count;
        }

        private static bool IsSelectableCandidate(
            RocketCandidate candidate,
            HashSet<long> selectedIds,
            bool requireNonHighlight)
        {
            if (candidate == null || selectedIds.Contains(candidate.Tile.Id))
            {
                return false;
            }

            if (requireNonHighlight && candidate.Tile.TileData.EntityVisibility == EntityVisibility.Highlight)
            {
                return false;
            }

            return true;
        }

        private static bool IsAllHighlightRocket(IReadOnlyList<Tile> highlightTiles)
        {
            for (int i = 0; i < highlightTiles.Count; i++)
            {
                if (highlightTiles[i].TileType != TileType.Rocket)
                {
                    return false;
                }
            }

            return true;
        }

        private int CountCurrentRockets()
        {
            int rocketCount = 0;
            foreach (var kvp in _tileDict)
            {
                if (kvp.Value.TileData.TileType == TileType.Rocket)
                {
                    rocketCount++;
                }
            }

            return rocketCount;
        }
    }
}
