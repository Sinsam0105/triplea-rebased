from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise RuntimeError(f"pattern not found in {path}: {old[:100]!r}")
    path.write_text(text.replace(old, new, 1))


root = Path(__file__).resolve().parents[1]

territory_attachment = root / "game-app/game-core/src/main/java/games/strategy/triplea/attachments/TerritoryEffectAttachment.java"
replace_once(territory_attachment, '  @NonNls public static final String MAX_AIR_BATTLE_ROUNDS = "maxAirBattleRounds";\n', '  @NonNls public static final String MAX_AIR_BATTLE_ROUNDS = "maxAirBattleRounds";\n  @NonNls public static final String STACK_CAPACITY = "stackCapacity";\n')
replace_once(territory_attachment, '  private @Nullable Integer maxAirBattleRounds = null;\n', '  private @Nullable Integer maxAirBattleRounds = null;\n  private @Nullable Integer stackCapacity = null;\n')
replace_once(territory_attachment, '  private static int validateBattleRounds(final Integer value, final String propertyName) {\n', '''  private void setStackCapacity(final String value) {
    setStackCapacity(getInt(value));
  }

  @VisibleForTesting
  public TerritoryEffectAttachment setStackCapacity(final Integer value) {
    final int capacity = value;
    if (capacity < -1) {
      throw new IllegalArgumentException(STACK_CAPACITY + " must be -1 or a non-negative integer");
    }
    stackCapacity = capacity;
    return this;
  }

  public OptionalInt getStackCapacity() {
    return stackCapacity == null ? OptionalInt.empty() : OptionalInt.of(stackCapacity);
  }

  private @Nullable Integer getStackCapacityProperty() {
    return stackCapacity;
  }

  private void resetStackCapacity() {
    stackCapacity = null;
  }

  private static int validateBattleRounds(final Integer value, final String propertyName) {
''')
replace_once(territory_attachment, '      case "movementCostModifier" ->\n', '''      case STACK_CAPACITY ->
          Optional.of(
              MutableProperty.of(
                  this::setStackCapacity,
                  this::setStackCapacity,
                  this::getStackCapacityProperty,
                  this::resetStackCapacity));
      case "movementCostModifier" ->
''')

unit_attachment = root / "game-app/game-core/src/main/java/games/strategy/triplea/attachments/UnitAttachment.java"
replace_once(unit_attachment, '  private @Nullable Tuple<Integer, String> movementLimit = null;\n', '  private @Nullable Tuple<Integer, String> movementLimit = null;\n  @Getter private int stackCost = 1;\n')
replace_once(unit_attachment, '  public int getStackingLimitMax(final Tuple<Integer, String> stackingLimit) {\n', '''  private void setStackCost(final String value) {
    setStackCost(getInt(value));
  }

  @VisibleForTesting
  public UnitAttachment setStackCost(final Integer value) {
    final int cost = value;
    if (cost < 0) {
      throw new IllegalArgumentException("stackCost must be a non-negative integer");
    }
    stackCost = cost;
    return this;
  }

  private void resetStackCost() {
    stackCost = 1;
  }

  public int getStackingLimitMax(final Tuple<Integer, String> stackingLimit) {
''')
replace_once(unit_attachment, '      case ATTACK_STRENGTH ->\n', '''      case "stackCost" ->
          Optional.of(
              MutableProperty.of(
                  this::setStackCost,
                  this::setStackCost,
                  this::getStackCost,
                  this::resetStackCost));
      case ATTACK_STRENGTH ->
''')

stack_filter = root / "game-app/game-core/src/main/java/games/strategy/triplea/delegate/move/validation/UnitStackingLimitFilter.java"
replace_once(stack_filter, 'import games.strategy.triplea.delegate.Matches;\n', 'import games.strategy.triplea.delegate.Matches;\nimport games.strategy.triplea.delegate.StackCapacityResolver;\n')
replace_once(stack_filter, '    final var unitsAllowedSoFar = new ArrayList<>(existingUnitsToBePlaced);\n    final var forbiddenTypes = TerritoryEffectHelper.getUnitTypesForUnitsNotAllowedIntoTerritory(t);\n    for (final Unit unit : units) {\n', '    final var unitsAllowedSoFar = new ArrayList<>(existingUnitsToBePlaced);\n    final var forbiddenTypes = TerritoryEffectHelper.getUnitTypesForUnitsNotAllowedIntoTerritory(t);\n    final var unitsWithinCapacity =\n        StackCapacityResolver.filterUnitsToFit(units, owner, t, existingUnitsToBePlaced);\n    for (final Unit unit : unitsWithinCapacity) {\n')

retreater = root / "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/steps/retreat/RetreaterGeneral.java"
replace_once(retreater, 'import games.strategy.triplea.delegate.Matches;\n', 'import games.strategy.triplea.delegate.Matches;\nimport games.strategy.triplea.delegate.StackCapacityResolver;\n')
replace_once(retreater, '    final Collection<Territory> allRetreatTerritories =\n        CollectionUtils.getMatches(\n            battleState.getAttackerRetreatTerritories(),\n            Matches.territoryEffectsAllowUnits(groundedRetreatUnits));\n', '    final Collection<Territory> allRetreatTerritories =\n        CollectionUtils.getMatches(\n            battleState.getAttackerRetreatTerritories(),\n            Matches.territoryEffectsAllowUnits(groundedRetreatUnits)\n                .and(\n                    territory ->\n                        StackCapacityResolver.canFit(\n                            groundedRetreatUnits,\n                            battleState.getPlayer(OFFENSE),\n                            territory,\n                            List.of())));\n')

(root / "game-app/game-core/src/main/java/games/strategy/triplea/delegate/StackCapacityResolver.java").write_text('''package games.strategy.triplea.delegate;

import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.TerritoryEffect;
import games.strategy.engine.data.Unit;
import games.strategy.triplea.attachments.TerritoryEffectAttachment;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.OptionalInt;

/** Resolves terrain capacity and unit stacking cost for every unit-entry path. */
public final class StackCapacityResolver {
  private StackCapacityResolver() {}

  public static OptionalInt resolveCapacity(final Collection<TerritoryEffect> effects) {
    boolean configured = false;
    int finiteCapacity = Integer.MAX_VALUE;
    for (final TerritoryEffect effect : effects) {
      final OptionalInt capacity = TerritoryEffectAttachment.get(effect).getStackCapacity();
      if (capacity.isEmpty()) {
        continue;
      }
      configured = true;
      if (capacity.getAsInt() >= 0) {
        finiteCapacity = Math.min(finiteCapacity, capacity.getAsInt());
      }
    }
    if (!configured) {
      return OptionalInt.empty();
    }
    return OptionalInt.of(finiteCapacity == Integer.MAX_VALUE ? -1 : finiteCapacity);
  }

  public static int getStackCost(final Unit unit) {
    return unit.getUnitAttachment().getStackCost();
  }

  public static int getOccupiedCapacity(final Collection<Unit> units) {
    return units.stream().mapToInt(StackCapacityResolver::getStackCost).sum();
  }

  public static boolean canFit(final Collection<Unit> enteringUnits, final GamePlayer owner, final Territory territory, final Collection<Unit> pendingUnits) {
    return filterUnitsToFit(enteringUnits, owner, territory, pendingUnits).size() == enteringUnits.size();
  }

  public static List<Unit> filterUnitsToFit(final Collection<Unit> candidates, final GamePlayer owner, final Territory territory, final Collection<Unit> pendingUnits) {
    return filterUnitsToFit(candidates, owner, TerritoryEffectHelper.getEffects(territory), alliedUnits(owner, territory.getUnits()), pendingUnits);
  }

  static List<Unit> filterUnitsToFit(final Collection<Unit> candidates, final GamePlayer owner, final Collection<TerritoryEffect> effects, final Collection<Unit> existingUnits, final Collection<Unit> pendingUnits) {
    final OptionalInt capacity = resolveCapacity(effects);
    if (capacity.isEmpty() || capacity.getAsInt() < 0) {
      return new ArrayList<>(candidates);
    }
    int occupied = getOccupiedCapacity(existingUnits) + getOccupiedCapacity(pendingUnits);
    final List<Unit> accepted = new ArrayList<>();
    for (final Unit candidate : candidates) {
      final int cost = getStackCost(candidate);
      if (cost == 0 || occupied + cost <= capacity.getAsInt()) {
        accepted.add(candidate);
        occupied += cost;
      }
    }
    return accepted;
  }

  private static List<Unit> alliedUnits(final GamePlayer owner, final Collection<Unit> territoryUnits) {
    return territoryUnits.stream().filter(unit -> owner.equals(unit.getOwner()) || owner.getData().getRelationshipTracker().isAllied(owner, unit.getOwner())).toList();
  }
}
''')

(root / "game-app/game-core/src/test/java/games/strategy/triplea/delegate/StackCapacityResolverTest.java").write_text('''package games.strategy.triplea.delegate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.TerritoryEffect;
import games.strategy.engine.data.Unit;
import games.strategy.engine.data.UnitType;
import games.strategy.triplea.Constants;
import games.strategy.triplea.attachments.TerritoryEffectAttachment;
import games.strategy.triplea.attachments.UnitAttachment;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class StackCapacityResolverTest {
  private final GameData gameData = new GameData();
  private final AtomicInteger names = new AtomicInteger();

  @Test
  void shortestFiniteCapacityWinsAcrossEffects() {
    assertEquals(2, StackCapacityResolver.resolveCapacity(List.of(effect(4), effect(2))).orElseThrow());
  }

  @Test
  void finiteCapacityWinsOverUnlimitedEffect() {
    assertEquals(3, StackCapacityResolver.resolveCapacity(List.of(effect(-1), effect(3))).orElseThrow());
  }

  @Test
  void allUnlimitedEffectsResolveToUnlimited() {
    assertEquals(-1, StackCapacityResolver.resolveCapacity(List.of(effect(-1), effect(-1))).orElseThrow());
  }

  @Test
  void missingCapacityRemainsUnconfigured() {
    final TerritoryEffect effect = new TerritoryEffect("plain", gameData);
    effect.addAttachment(Constants.TERRITORYEFFECT_ATTACHMENT_NAME, new TerritoryEffectAttachment(Constants.TERRITORYEFFECT_ATTACHMENT_NAME, effect, gameData));
    assertFalse(StackCapacityResolver.resolveCapacity(List.of(effect)).isPresent());
  }

  @Test
  void acceptsCandidatesInStableOrderUntilCapacityIsFull() {
    final GamePlayer owner = mock(GamePlayer.class);
    final Unit first = unit(owner, 2);
    final Unit second = unit(owner, 1);
    final Unit third = unit(owner, 2);
    assertEquals(List.of(first, second), StackCapacityResolver.filterUnitsToFit(List.of(first, second, third), owner, List.of(effect(3)), List.of(), List.of()));
  }

  @Test
  void existingOverCapacityStackAllowsOnlyZeroCostEntries() {
    final GamePlayer owner = mock(GamePlayer.class);
    final Unit existing = unit(owner, 4);
    final Unit free = unit(owner, 0);
    final Unit costly = unit(owner, 1);
    assertEquals(List.of(free), StackCapacityResolver.filterUnitsToFit(List.of(free, costly), owner, List.of(effect(3)), List.of(existing), List.of()));
  }

  @Test
  void pendingUnitsConsumeCapacityForPlacementAndReinforcementBatches() {
    final GamePlayer owner = mock(GamePlayer.class);
    final Unit pending = unit(owner, 2);
    final Unit candidate = unit(owner, 2);
    assertEquals(List.of(), StackCapacityResolver.filterUnitsToFit(List.of(candidate), owner, List.of(effect(3)), List.of(), List.of(pending)));
  }

  @Test
  void invalidAttachmentValuesAreRejected() {
    final TerritoryEffect effect = new TerritoryEffect("invalid", gameData);
    final TerritoryEffectAttachment attachment = new TerritoryEffectAttachment(Constants.TERRITORYEFFECT_ATTACHMENT_NAME, effect, gameData);
    assertThrows(IllegalArgumentException.class, () -> attachment.setStackCapacity(-2));
    final UnitType type = new UnitType("invalid-cost", gameData);
    final UnitAttachment unitAttachment = new UnitAttachment(Constants.UNIT_ATTACHMENT_NAME, type, gameData);
    assertThrows(IllegalArgumentException.class, () -> unitAttachment.setStackCost(-1));
  }

  private TerritoryEffect effect(final int capacity) {
    final TerritoryEffect effect = new TerritoryEffect("effect-" + names.incrementAndGet(), gameData);
    final TerritoryEffectAttachment attachment = new TerritoryEffectAttachment(Constants.TERRITORYEFFECT_ATTACHMENT_NAME, effect, gameData).setStackCapacity(capacity);
    effect.addAttachment(Constants.TERRITORYEFFECT_ATTACHMENT_NAME, attachment);
    return effect;
  }

  private static Unit unit(final GamePlayer owner, final int cost) {
    final Unit unit = mock(Unit.class);
    final UnitAttachment attachment = mock(UnitAttachment.class);
    when(unit.getOwner()).thenReturn(owner);
    when(unit.getUnitAttachment()).thenReturn(attachment);
    when(attachment.getStackCost()).thenReturn(cost);
    return unit;
  }
}
''')

(root / "docs/development/terrain-stack-capacity.md").write_text('''# Terrain stack capacity

Small Front terrain can limit the amount of one allied force that may occupy a territory.

```xml
<attachment name="territoryEffectAttachment" attachTo="mountain">
  <option name="stackCapacity" value="6"/>
</attachment>

<attachment name="unitAttachment" attachTo="armor">
  <option name="stackCost" value="2"/>
</attachment>
```

`stackCapacity` accepts a non-negative integer or `-1` for unlimited capacity. An omitted value keeps legacy unlimited behavior. When several territory effects overlap, the shortest finite capacity wins. `stackCost` defaults to `1`, accepts zero for units that do not consume front capacity, and rejects negative values.

Capacity is counted per allied force. Enemy defenders do not consume an attacker's entry capacity. Existing over-capacity territories are not modified or purged; they may accept zero-cost units, but no additional positive-cost units until their occupied cost is low enough.

The common resolver is applied before legacy movement, attacking, and placement stacking limits. The same API accepts a pending-unit collection, so scheduled reinforcement batches are evaluated consistently. General retreat destinations are removed when the full non-air retreating force cannot fit.
''')

roadmap = root / "docs/development/small-front-roadmap.md"
replace_once(roadmap, '## 6. Territory stack capacity\n\n- `stackCapacity` on territory effects\n', '## 6. Territory stack capacity\n\nStatus: complete in PR #7.\n\n- `stackCapacity` on territory effects\n')
replace_once(roadmap, '## 7. Combat and redeployment movement\n\n- separate combat and after-combat movement values\n', '## 7. Combat and redeployment movement\n\nStatus: next.\n\n- separate combat and after-combat movement values\n')
