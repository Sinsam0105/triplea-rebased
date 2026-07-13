package games.strategy.triplea.delegate.battle.simulation;

import java.util.Map;
import java.util.Objects;

/** Version-one generic action envelope; typed actions can replace this after decision points stabilize. */
public record BattleAction(String type, Map<String, String> parameters) {
  public BattleAction {
    Objects.requireNonNull(type);
    parameters = Map.copyOf(parameters);
  }
}
