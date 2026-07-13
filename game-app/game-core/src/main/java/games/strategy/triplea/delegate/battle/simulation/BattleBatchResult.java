package games.strategy.triplea.delegate.battle.simulation;

import java.util.List;

/** Ordered replay results for one batch request. */
public record BattleBatchResult(
    List<BattleReplayResult> results, int matchedEpisodes, int mismatchedEpisodes) {
  public BattleBatchResult {
    results = List.copyOf(results);
    if (matchedEpisodes < 0 || mismatchedEpisodes < 0) {
      throw new IllegalArgumentException("batch counts must not be negative");
    }
    if (matchedEpisodes + mismatchedEpisodes != results.size()) {
      throw new IllegalArgumentException("batch counts must equal result count");
    }
  }

  public static BattleBatchResult from(final List<BattleReplayResult> results) {
    final int matched = (int) results.stream().filter(BattleReplayResult::matched).count();
    return new BattleBatchResult(results, matched, results.size() - matched);
  }
}
