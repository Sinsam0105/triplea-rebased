package games.strategy.triplea.delegate.supply;

import static org.assertj.core.api.Assertions.assertThat;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.Unit;
import games.strategy.engine.data.UnitType;
import games.strategy.triplea.Constants;
import games.strategy.triplea.attachments.UnitAttachment;
import games.strategy.triplea.attachments.UnitSupportAttachment;
import games.strategy.triplea.delegate.battle.BattleState;
import games.strategy.triplea.delegate.power.calculator.SupportCalculator;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/** An isolated supporter provides no support bonus while it is cut off. */
class SupplySupportSuppressionTest {
  private final GameData data = new GameData();
  private final GamePlayer player = new GamePlayer("Blue", data);
  private final Territory front = new Territory("Front", data);
  private final UnitType artillery = new UnitType("artillery", data);
  private final UnitType infantry = new UnitType("infantry", data);
  private final SupplyDelegate supplyDelegate = new SupplyDelegate();
  private Unit gun;
  private UnitSupportAttachment rule;

  @BeforeEach
  void setUp() throws Exception {
    data.getPlayerList().addPlayerId(player);
    front.setOwner(player);
    data.getMap().addTerritory(front);
    artillery.addAttachment(
        Constants.UNIT_ATTACHMENT_NAME,
        new UnitAttachment(Constants.UNIT_ATTACHMENT_NAME, artillery, data));
    data.getUnitTypeList().addUnitType(artillery);
    data.getUnitTypeList().addUnitType(infantry);
    gun = artillery.create(1, player).getFirst();
    front.getUnitCollection().add(gun);

    rule = new UnitSupportAttachment("support", artillery, data);
    rule.setSide("offence")
        .setFaction("allied")
        .setPlayers(List.of(player))
        .setUnitType(Set.of(infantry))
        .setBonusType("artillerySupport")
        .setNumber(1);

    data.getProperties().set(SupplyNetworkResolver.SUPPLY_NETWORK_ENABLED, true);
    supplyDelegate.initialize("supply", "Supply");
    data.addDelegate(supplyDelegate);
  }

  @Test
  void suppliedSupporterGivesItsBonus() {
    final SupportCalculator calculator =
        new SupportCalculator(List.of(gun), List.of(rule), BattleState.Side.OFFENSE, true);

    assertThat(calculator.getSupport(rule)).isEqualTo(1);
  }

  @Test
  void isolatedSupporterGivesNoBonus() {
    supplyDelegate.getTracker().increment(gun);

    final SupportCalculator calculator =
        new SupportCalculator(List.of(gun), List.of(rule), BattleState.Side.OFFENSE, true);

    assertThat(SupplyNetworkResolver.isOutOfSupply(gun, data)).isTrue();
    assertThat(calculator.getSupport(rule)).isZero();
  }

  @Test
  void restoringSupplyReturnsTheBonus() {
    supplyDelegate.getTracker().increment(gun);
    supplyDelegate.getTracker().clear(gun);

    final SupportCalculator calculator =
        new SupportCalculator(List.of(gun), List.of(rule), BattleState.Side.OFFENSE, true);

    assertThat(calculator.getSupport(rule)).isEqualTo(1);
  }
}
