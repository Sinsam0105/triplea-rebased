package games.strategy.triplea.delegate.supply;

import games.strategy.engine.data.CompositeChange;
import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.MoveDescription;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.Unit;
import games.strategy.engine.data.changefactory.ChangeFactory;
import games.strategy.triplea.delegate.EditDelegate;
import games.strategy.triplea.delegate.GameStepPropertiesHelper;
import games.strategy.triplea.delegate.Matches;
import games.strategy.triplea.delegate.MoveDelegate;
import games.strategy.triplea.delegate.StackCapacityResolver;
import games.strategy.triplea.delegate.battle.BattleTracker;
import games.strategy.triplea.formatter.MyFormatter;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Optional;

/**
 * Move delegate that enforces Small Front supply, terrain stack-capacity and exploitation rules.
 */
public final class SupplyAwareMoveDelegate extends MoveDelegate {
  public static final String STACK_CAPACITY_EXCEEDED = "Terrain stack capacity exceeded";
  public static final String EXPLOITATION_NOT_FROM_CAPTURED_GROUND =
      "Exploitation may only advance from ground captured this turn";
  public static final String EXPLOITATION_INELIGIBLE_UNITS =
      "Only armour, and mechanized alongside armour, may exploit";

  // Small Front unit types allowed to exploit. Named here because exploitation is a scenario rule.
  private static final String ARMOUR = "armour";
  private static final String MECHANIZED = "mechanized";

  @Override
  public void start() {
    super.start();
    // The battle already exhausted the combat movers so they cannot also redeploy. Exploitation is
    // a fresh, separate step, so give only the exploitation-eligible units in this-turn-captured
    // ground a clean movement allowance (capped to one step by MovementAllowanceResolver). Every
    // other unit stays exhausted, preserving the combat-then-redeploy lockout.
    if (GameStepPropertiesHelper.isExploitationMove(getData())) {
      grantExploitationMovement();
    }
  }

  @Override
  public Optional<String> performMove(final MoveDescription move) {
    final GameData data = getData();
    if (!EditDelegate.getEditMode(data.getProperties()) && !move.getRoute().hasNoSteps()) {
      final GamePlayer movingPlayer = getUnitsOwner(move.getUnits());
      if (GameStepPropertiesHelper.isExploitationMove(data)) {
        final Optional<String> exploitationError =
            validateExploitation(move, movingPlayer, getBattleTracker(data));
        if (exploitationError.isPresent()) {
          return exploitationError;
        }
      }
      // Out-of-supply units are not blocked here; their reduced movement is enforced by
      // MovementAllowanceResolver, so ordinary movement validation already stops an over-reach.
      final Optional<String> capacityError = validateStackCapacity(move, movingPlayer);
      if (capacityError.isPresent()) {
        return capacityError;
      }
    }
    return super.performMove(move);
  }

  static Optional<String> validateExploitation(
      final MoveDescription move,
      final GamePlayer movingPlayer,
      final BattleTracker battleTracker) {
    final Territory start = move.getRoute().getStart();
    if (!battleTracker.wasConquered(start)) {
      return Optional.of(EXPLOITATION_NOT_FROM_CAPTURED_GROUND + ": " + start.getName());
    }
    final Collection<Unit> eligible = exploitationEligibleUnits(start, movingPlayer);
    final List<Unit> ineligible = new ArrayList<>(move.getUnits());
    ineligible.removeAll(eligible);
    if (!ineligible.isEmpty()) {
      return Optional.of(
          EXPLOITATION_INELIGIBLE_UNITS + ": " + MyFormatter.unitsToTextNoOwner(ineligible));
    }
    return Optional.empty();
  }

  private void grantExploitationMovement() {
    final GameData data = getData();
    final BattleTracker battleTracker = getBattleTracker(data);
    final CompositeChange change = new CompositeChange();
    for (final Territory territory : data.getMap().getTerritories()) {
      if (!battleTracker.wasConquered(territory)) {
        continue;
      }
      for (final Unit unit : exploitationEligibleUnits(territory, player)) {
        change.add(
            ChangeFactory.unitPropertyChange(
                unit, BigDecimal.ZERO, Unit.PropertyName.ALREADY_MOVED));
      }
    }
    if (!change.isEmpty()) {
      bridge.addChange(change);
    }
  }

  /**
   * Armour in {@code territory}, plus mechanized sharing that ground with an armour. Mechanized may
   * only exploit under the cover of armour, so with no armour present nothing is eligible.
   */
  private static Collection<Unit> exploitationEligibleUnits(
      final Territory territory, final GamePlayer player) {
    final Collection<Unit> owned =
        territory.getUnitCollection().getMatches(Matches.unitIsOwnedBy(player));
    final boolean hasArmour = owned.stream().anyMatch(SupplyAwareMoveDelegate::isArmour);
    return owned.stream()
        .filter(unit -> isArmour(unit) || (hasArmour && isMechanized(unit)))
        .toList();
  }

  private static boolean isArmour(final Unit unit) {
    return unit.getType().getName().equals(ARMOUR);
  }

  private static boolean isMechanized(final Unit unit) {
    return unit.getType().getName().equals(MECHANIZED);
  }

  /** Returns an error when the final destination cannot accept the complete moving force. */
  public static Optional<String> validateStackCapacity(
      final MoveDescription move, final GamePlayer movingPlayer) {
    if (move.getRoute().hasNoSteps()) {
      return Optional.empty();
    }
    final Territory destination = move.getRoute().getEnd();
    final List<Unit> allowed =
        StackCapacityResolver.filterUnitsToFit(
            move.getUnits(), movingPlayer, destination, List.of());
    if (allowed.size() == move.getUnits().size()) {
      return Optional.empty();
    }
    final List<Unit> blocked = new ArrayList<>(move.getUnits());
    blocked.removeAll(allowed);
    return Optional.of(
        STACK_CAPACITY_EXCEEDED
            + " in "
            + destination.getName()
            + ": "
            + MyFormatter.unitsToTextNoOwner(blocked));
  }
}
