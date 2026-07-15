package games.strategy.triplea.delegate.strategic.simulation;

import java.util.List;

/** Mutable adapter over one restored player turn. */
public interface StrategicScenario {
  StrategicObservation observation();

  List<StrategicAction> legalActions();

  default boolean isLegalAction(final StrategicAction action) {
    return legalActions().contains(action);
  }

  StrategicScenarioStep step(StrategicAction action);
}
