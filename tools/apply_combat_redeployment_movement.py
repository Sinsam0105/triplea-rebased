from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise RuntimeError(f"pattern not found in {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1))


unit_attachment = ROOT / "game-app/game-core/src/main/java/games/strategy/triplea/attachments/UnitAttachment.java"
replace_once(
    unit_attachment,
    "import java.util.Optional;\nimport java.util.Set;",
    "import java.util.Objects;\nimport java.util.Optional;\nimport java.util.OptionalInt;\nimport java.util.Set;",
)
replace_once(
    unit_attachment,
    "  private int movement = 0;\n  private boolean canBlitz = false;",
    "  private int movement = 0;\n  private @Nullable Integer combatMovement = null;\n  private @Nullable Integer redeploymentMovement = null;\n  private boolean canBlitz = false;",
)
replace_once(
    unit_attachment,
    '''  private void setMovement(final String s) {
    movement = getInt(s);
  }

  @VisibleForTesting
  public void setMovement(final Integer s) {
    movement = s;
  }

  private int getMovement() {
    return movement;
  }

  public int getMovement(final GamePlayer player) {
    final int bonus = getTechTracker().getMovementBonus(player, getUnitType());
    return Math.max(0, movement + bonus);
  }

  private void resetMovement() {
    movement = 0;
  }
''',
    '''  private void setMovement(final String s) {
    movement = getInt(s);
  }

  @VisibleForTesting
  public void setMovement(final Integer s) {
    movement = s;
  }

  private int getMovement() {
    return movement;
  }

  public int getMovement(final GamePlayer player) {
    return getMovementWithBonus(movement, player);
  }

  private void resetMovement() {
    movement = 0;
  }

  private void setCombatMovement(final String value) {
    setCombatMovement(getInt(value));
  }

  @VisibleForTesting
  public UnitAttachment setCombatMovement(final Integer value) {
    combatMovement = validateMovementOverride(value, "combatMovement");
    return this;
  }

  public OptionalInt getCombatMovement() {
    return combatMovement == null ? OptionalInt.empty() : OptionalInt.of(combatMovement);
  }

  public int getCombatMovement(final GamePlayer player) {
    return getMovementWithBonus(combatMovement == null ? movement : combatMovement, player);
  }

  private @Nullable Integer getCombatMovementProperty() {
    return combatMovement;
  }

  private void resetCombatMovement() {
    combatMovement = null;
  }

  private void setRedeploymentMovement(final String value) {
    setRedeploymentMovement(getInt(value));
  }

  @VisibleForTesting
  public UnitAttachment setRedeploymentMovement(final Integer value) {
    redeploymentMovement = validateMovementOverride(value, "redeploymentMovement");
    return this;
  }

  public OptionalInt getRedeploymentMovement() {
    return redeploymentMovement == null
        ? OptionalInt.empty()
        : OptionalInt.of(redeploymentMovement);
  }

  public int getRedeploymentMovement(final GamePlayer player) {
    return getMovementWithBonus(
        redeploymentMovement == null ? movement : redeploymentMovement, player);
  }

  private @Nullable Integer getRedeploymentMovementProperty() {
    return redeploymentMovement;
  }

  private void resetRedeploymentMovement() {
    redeploymentMovement = null;
  }

  private int getMovementWithBonus(final int baseMovement, final GamePlayer player) {
    final int bonus = getTechTracker().getMovementBonus(player, getUnitType());
    return Math.max(0, baseMovement + bonus);
  }

  private static int validateMovementOverride(final Integer value, final String propertyName) {
    final int movementValue = Objects.requireNonNull(value);
    if (movementValue < 0) {
      throw new IllegalArgumentException(propertyName + " must be a non-negative integer");
    }
    return movementValue;
  }
''',
)
replace_once(
    unit_attachment,
    '''      case "movement" ->
          Optional.of(
              MutableProperty.of(
                  this::setMovement, this::setMovement, this::getMovement, this::resetMovement));
      case "canBlitz" ->
''',
    '''      case "movement" ->
          Optional.of(
              MutableProperty.of(
                  this::setMovement, this::setMovement, this::getMovement, this::resetMovement));
      case "combatMovement" ->
          Optional.of(
              MutableProperty.of(
                  this::setCombatMovement,
                  this::setCombatMovement,
                  this::getCombatMovementProperty,
                  this::resetCombatMovement));
      case "redeploymentMovement" ->
          Optional.of(
              MutableProperty.of(
                  this::setRedeploymentMovement,
                  this::setRedeploymentMovement,
                  this::getRedeploymentMovementProperty,
                  this::resetRedeploymentMovement));
      case "canBlitz" ->
''',
)

unit_file = ROOT / "game-app/game-core/src/main/java/games/strategy/engine/data/Unit.java"
replace_once(
    unit_file,
    "import games.strategy.triplea.delegate.Matches;",
    "import games.strategy.triplea.delegate.Matches;\nimport games.strategy.triplea.delegate.MovementAllowanceResolver;",
)
replace_once(
    unit_file,
    '''  /** Does not account for any movement already made. Generally equal to UnitType movement */
  public int getMaxMovementAllowed() {
    return Math.max(0, bonusMovement + getType().getUnitAttachment().getMovement(getOwner()));
  }

  public BigDecimal getMovementLeft() {
    return new BigDecimal(getType().getUnitAttachment().getMovement(getOwner()))
        .add(new BigDecimal(bonusMovement))
        .subtract(alreadyMoved);
  }
''',
    '''  /** Does not account for any movement already made. */
  public int getMaxMovementAllowed() {
    return MovementAllowanceResolver.resolveMaximumMovement(this);
  }

  public BigDecimal getMovementLeft() {
    return BigDecimal.valueOf(getMaxMovementAllowed()).subtract(alreadyMoved);
  }
''',
)

move_delegate = ROOT / "game-app/game-core/src/main/java/games/strategy/triplea/delegate/MoveDelegate.java"
replace_once(
    move_delegate,
    '''      // Only air units can move during both CM and NCM in the same turn so moved units are set to
      // no moves left
      final List<Unit> alreadyMovedNonAirUnits =
          CollectionUtils.getMatches(
              data.getUnits().getUnits(), Matches.unitHasMoved().and(Matches.unitIsNotAir()));
      bridge.addChange(ChangeFactory.markNoMovementChange(alreadyMovedNonAirUnits));
''',
    '''      // Only air units can move during both combat and redeployment in the same turn. Mark
      // moved non-air units against the redeployment allowance, which may be larger than combat
      // movement.
      final List<Unit> alreadyMovedNonAirUnits =
          CollectionUtils.getMatches(
              data.getUnits().getUnits(), Matches.unitHasMoved().and(Matches.unitIsNotAir()));
      final CompositeChange noRedeploymentMovement = new CompositeChange();
      for (final Unit unit : alreadyMovedNonAirUnits) {
        final BigDecimal exhaustedMovement =
            BigDecimal.valueOf(
                MovementAllowanceResolver.resolveMaximumMovement(
                        unit, MovementAllowanceResolver.MovementPhase.REDEPLOYMENT)
                    + 1L);
        noRedeploymentMovement.add(
            ChangeFactory.unitPropertyChange(
                unit,
                unit.getAlreadyMoved().max(exhaustedMovement),
                Unit.PropertyName.ALREADY_MOVED));
      }
      bridge.addChange(noRedeploymentMovement);
''',
)

resolver = ROOT / "game-app/game-core/src/main/java/games/strategy/triplea/delegate/MovementAllowanceResolver.java"
resolver.write_text(
    '''package games.strategy.triplea.delegate;

import com.google.common.annotations.VisibleForTesting;
import games.strategy.engine.data.GameData;
import games.strategy.engine.data.Unit;
import games.strategy.triplea.attachments.UnitAttachment;
import lombok.experimental.UtilityClass;

/** Resolves a unit's maximum movement for the current movement phase. */
@UtilityClass
public final class MovementAllowanceResolver {
  public enum MovementPhase {
    COMBAT,
    REDEPLOYMENT,
    OTHER
  }

  public static int resolveMaximumMovement(final Unit unit) {
    return resolveMaximumMovement(unit, resolveCurrentPhase(unit.getData()));
  }

  @VisibleForTesting
  public static int resolveMaximumMovement(final Unit unit, final MovementPhase phase) {
    final UnitAttachment attachment = unit.getUnitAttachment();
    final int attachmentMovement =
        switch (phase) {
          case COMBAT -> attachment.getCombatMovement(unit.getOwner());
          case REDEPLOYMENT -> attachment.getRedeploymentMovement(unit.getOwner());
          case OTHER -> attachment.getMovement(unit.getOwner());
        };
    return Math.max(0, attachmentMovement + unit.getBonusMovement());
  }

  private static MovementPhase resolveCurrentPhase(final GameData data) {
    if (data.getSequence().getStep() == null) {
      return MovementPhase.OTHER;
    }
    if (GameStepPropertiesHelper.isCombatMove(data, true)) {
      return MovementPhase.COMBAT;
    }
    if (GameStepPropertiesHelper.isNonCombatMove(data, true)) {
      return MovementPhase.REDEPLOYMENT;
    }
    return MovementPhase.OTHER;
  }
}
'''
)

test_file = ROOT / "game-app/game-core/src/test/java/games/strategy/triplea/delegate/MovementAllowanceResolverTest.java"
test_file.write_text(
    '''package games.strategy.triplea.delegate;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Unit;
import games.strategy.engine.data.UnitType;
import games.strategy.triplea.Constants;
import games.strategy.triplea.attachments.UnitAttachment;
import org.junit.jupiter.api.Test;

class MovementAllowanceResolverTest {
  @Test
  void resolvesCombatAndRedeploymentMovementWithUnitBonus() {
    final Unit unit = mock(Unit.class);
    final UnitAttachment attachment = mock(UnitAttachment.class);
    final GamePlayer player = mock(GamePlayer.class);
    when(unit.getUnitAttachment()).thenReturn(attachment);
    when(unit.getOwner()).thenReturn(player);
    when(unit.getBonusMovement()).thenReturn(1);
    when(attachment.getCombatMovement(player)).thenReturn(2);
    when(attachment.getRedeploymentMovement(player)).thenReturn(5);

    assertThat(
            MovementAllowanceResolver.resolveMaximumMovement(
                unit, MovementAllowanceResolver.MovementPhase.COMBAT))
        .isEqualTo(3);
    assertThat(
            MovementAllowanceResolver.resolveMaximumMovement(
                unit, MovementAllowanceResolver.MovementPhase.REDEPLOYMENT))
        .isEqualTo(6);
  }

  @Test
  void usesLegacyMovementOutsideMovementPhases() {
    final Unit unit = mock(Unit.class);
    final UnitAttachment attachment = mock(UnitAttachment.class);
    final GamePlayer player = mock(GamePlayer.class);
    when(unit.getUnitAttachment()).thenReturn(attachment);
    when(unit.getOwner()).thenReturn(player);
    when(attachment.getMovement(player)).thenReturn(4);

    assertThat(
            MovementAllowanceResolver.resolveMaximumMovement(
                unit, MovementAllowanceResolver.MovementPhase.OTHER))
        .isEqualTo(4);
  }

  @Test
  void phaseOverridesFallBackToLegacyMovementAndApplyTechBonus() {
    final GameData data = mock(GameData.class);
    final UnitType unitType = mock(UnitType.class);
    final GamePlayer player = mock(GamePlayer.class);
    final TechTracker techTracker = mock(TechTracker.class);
    when(data.getTechTracker()).thenReturn(techTracker);
    when(techTracker.getMovementBonus(player, unitType)).thenReturn(1);
    final UnitAttachment attachment =
        new UnitAttachment(Constants.UNIT_ATTACHMENT_NAME, unitType, data);
    attachment.setMovement(3);

    assertThat(attachment.getCombatMovement(player)).isEqualTo(4);
    assertThat(attachment.getRedeploymentMovement(player)).isEqualTo(4);

    attachment.setCombatMovement(1);
    attachment.setRedeploymentMovement(5);
    assertThat(attachment.getCombatMovement(player)).isEqualTo(2);
    assertThat(attachment.getRedeploymentMovement(player)).isEqualTo(6);
  }

  @Test
  void exposesOptionalOverridesAndRejectsNegativeValues() {
    final UnitAttachment attachment =
        new UnitAttachment(
            Constants.UNIT_ATTACHMENT_NAME, mock(UnitType.class), mock(GameData.class));

    assertThat(attachment.getCombatMovement()).isEmpty();
    assertThat(attachment.getRedeploymentMovement()).isEmpty();
    assertThat(attachment.getPropertyOrEmpty("combatMovement")).isPresent();
    assertThat(attachment.getPropertyOrEmpty("redeploymentMovement")).isPresent();

    attachment.setCombatMovement(2);
    attachment.setRedeploymentMovement(4);
    assertThat(attachment.getCombatMovement()).hasValue(2);
    assertThat(attachment.getRedeploymentMovement()).hasValue(4);
    assertThatThrownBy(() -> attachment.setCombatMovement(-1))
        .isInstanceOf(IllegalArgumentException.class);
    assertThatThrownBy(() -> attachment.setRedeploymentMovement(-1))
        .isInstanceOf(IllegalArgumentException.class);
  }
}
'''
)

doc = ROOT / "docs/development/combat-redeployment-movement.md"
doc.write_text(
    '''# Combat and redeployment movement

Small Front unit types can define different movement allowances for the combat and after-combat movement phases.

```xml
<attachment name="unitAttachment" attachTo="infantry">
  <option name="movement" value="1"/>
  <option name="combatMovement" value="1"/>
  <option name="redeploymentMovement" value="3"/>
</attachment>
```

Both phase-specific values are optional non-negative integers. If omitted, the legacy `movement` value is used. Existing technology and local bonus-movement modifiers apply after the phase value is selected.

`Unit.getMaxMovementAllowed()` and `Unit.getMovementLeft()` use the current game step, so movement validators, route searches, UI selection, aircraft landing checks, transports, and AI utilities that consume unit movement share the same allowance.

Air units retain movement spent during combat and may use any remaining redeployment allowance. At the end of Combat Move, every non-air unit that moved is marked beyond its redeployment allowance. This preserves the rule that non-air units used during Combat Move cannot move again during After Combat Move, even when their redeployment allowance is larger.
'''
)

roadmap = ROOT / "docs/development/small-front-roadmap.md"
replace_once(
    roadmap,
    '''## 7. Combat and redeployment movement

Status: next.
''',
    '''## 7. Combat and redeployment movement

Status: in progress.
''',
)
