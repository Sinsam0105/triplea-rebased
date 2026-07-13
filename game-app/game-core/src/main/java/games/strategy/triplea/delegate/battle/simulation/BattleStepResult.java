package games.strategy.triplea.delegate.battle.simulation;

import java.util.Map;
import java.util.Objects;

public record BattleStepResult(
    BattleObservation observation,
    double reward,
    boolean terminated,
    boolean truncated,
    Map<String, String> info) {
  public BattleStepResult {
    Objects.requireNonNull(observation);
    info = Map.copyOf(info);
  }
}
