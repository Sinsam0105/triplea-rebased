package games.strategy.triplea.delegate.supply;

import static org.assertj.core.api.Assertions.assertThat;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.Unit;
import games.strategy.engine.data.UnitType;
import games.strategy.triplea.Constants;
import games.strategy.triplea.attachments.UnitAttachment;
import games.strategy.triplea.delegate.MovementAllowanceResolver;
import games.strategy.triplea.delegate.MovementAllowanceResolver.MovementPhase;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class SupplyIsolationMovementTest {
  private final GameData data = new GameData();
  private final GamePlayer player = new GamePlayer("Blue", data);
  private final Territory front = new Territory("Front", data);
  private final UnitType armour = new UnitType("armour", data);
  private final SupplyDelegate supplyDelegate = new SupplyDelegate();
  private Unit unit;

  @BeforeEach
  void setUp() {
    data.getPlayerList().addPlayerId(player);
    front.setOwner(player);
    data.getMap().addTerritory(front);
    final UnitAttachment attachment =
        new UnitAttachment(Constants.UNIT_ATTACHMENT_NAME, armour, data);
    attachment.setMovement(2);
    attachment.setCombatMovement(2);
    attachment.setRedeploymentMovement(3);
    armour.addAttachment(Constants.UNIT_ATTACHMENT_NAME, attachment);
    data.getUnitTypeList().addUnitType(armour);
    unit = armour.create(1, player).getFirst();
    front.getUnitCollection().add(unit);
    data.getProperties().set(SupplyNetworkResolver.SUPPLY_NETWORK_ENABLED, true);
    // The movement resolver reads the isolation tracker off the SupplyDelegate.
    supplyDelegate.initialize("supply", "Supply");
    data.addDelegate(supplyDelegate);
  }

  @Test
  void suppliedUnitKeepsFullMovement() {
    assertThat(MovementAllowanceResolver.resolveMaximumMovement(unit, MovementPhase.COMBAT))
        .isEqualTo(2);
    assertThat(MovementAllowanceResolver.resolveMaximumMovement(unit, MovementPhase.REDEPLOYMENT))
        .isEqualTo(3);
  }

  @Test
  void isolatedUnitMovesOneAndCannotRedeploy() {
    supplyDelegate.getTracker().increment(unit);

    assertThat(SupplyNetworkResolver.isOutOfSupply(unit, data)).isTrue();
    assertThat(MovementAllowanceResolver.resolveMaximumMovement(unit, MovementPhase.COMBAT))
        .isEqualTo(1);
    assertThat(MovementAllowanceResolver.resolveMaximumMovement(unit, MovementPhase.OTHER))
        .isEqualTo(1);
    // Redeployment (afmov) is forbidden while cut off.
    assertThat(MovementAllowanceResolver.resolveMaximumMovement(unit, MovementPhase.REDEPLOYMENT))
        .isZero();
  }

  @Test
  void restoringSupplyReturnsFullMovement() {
    supplyDelegate.getTracker().increment(unit);
    supplyDelegate.getTracker().clear(unit);

    assertThat(SupplyNetworkResolver.isOutOfSupply(unit, data)).isFalse();
    assertThat(MovementAllowanceResolver.resolveMaximumMovement(unit, MovementPhase.COMBAT))
        .isEqualTo(2);
    assertThat(MovementAllowanceResolver.resolveMaximumMovement(unit, MovementPhase.REDEPLOYMENT))
        .isEqualTo(3);
  }
}
