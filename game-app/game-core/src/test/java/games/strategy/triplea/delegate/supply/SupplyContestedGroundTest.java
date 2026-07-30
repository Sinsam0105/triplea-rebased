package games.strategy.triplea.delegate.supply;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import games.strategy.engine.data.Change;
import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.Unit;
import games.strategy.engine.data.UnitType;
import games.strategy.engine.delegate.IDelegateBridge;
import games.strategy.engine.history.IDelegateHistoryWriter;
import games.strategy.triplea.Constants;
import games.strategy.triplea.attachments.SupplyTerritoryAttachment;
import games.strategy.triplea.attachments.UnitAttachment;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * Units left on contested enemy ground after a drawn battle are only starved when they have truly
 * outrun their own supply network (T4).
 */
class SupplyContestedGroundTest {
  private final GameData data = new GameData();
  private final GamePlayer blue = new GamePlayer("Blue", data);
  private final GamePlayer red = new GamePlayer("Red", data);
  private final Territory depot = new Territory("Depot", data); // Blue supply source
  private final Territory border = new Territory("Border", data); // Blue, on the road home
  private final Territory contested = new Territory("Contested", data); // Red, road to Border
  private final Territory deep = new Territory("Deep", data); // Red, no road home
  private final UnitType infantry = new UnitType("infantry", data);
  private final SupplyTracker tracker = new SupplyTracker();
  private final IDelegateBridge bridge = mock(IDelegateBridge.class);
  private Unit stalledAttacker;
  private Unit recklessDash;

  @BeforeEach
  void setUp() throws Exception {
    data.getPlayerList().addPlayerId(blue);
    data.getPlayerList().addPlayerId(red);
    for (final Territory territory : new Territory[] {depot, border, contested, deep}) {
      data.getMap().addTerritory(territory);
    }
    depot.setOwner(blue);
    border.setOwner(blue);
    contested.setOwner(red);
    deep.setOwner(red);

    infantry.addAttachment(
        Constants.UNIT_ATTACHMENT_NAME,
        new UnitAttachment(Constants.UNIT_ATTACHMENT_NAME, infantry, data));
    data.getUnitTypeList().addUnitType(infantry);

    attach(depot).setSupplySource("true");
    attach(depot).setRoadConnection("Border");
    attach(border).setRoadConnection("Contested");

    stalledAttacker = infantry.create(1, blue).getFirst();
    contested.getUnitCollection().add(stalledAttacker);
    recklessDash = infantry.create(1, blue).getFirst();
    deep.getUnitCollection().add(recklessDash);

    data.getProperties().set(SupplyNetworkResolver.SUPPLY_NETWORK_ENABLED, true);
    when(bridge.getData()).thenReturn(data);
    when(bridge.getHistoryWriter()).thenReturn(mock(IDelegateHistoryWriter.class));
    doAnswer(
            invocation -> {
              data.performChange(invocation.getArgument(0, Change.class));
              return null;
            })
        .when(bridge)
        .addChange(any(Change.class));
  }

  @Test
  void roadToOwnNetworkKeepsContestedGroundSupplied() {
    // The stalled attacker sits on enemy ground, but a road from Contested reaches Blue's network.
    assertThat(SupplyNetworkResolver.wouldBeSupplied(contested, blue, data)).isTrue();
    // The reckless dash has outrun its roads entirely.
    assertThat(SupplyNetworkResolver.wouldBeSupplied(deep, blue, data)).isFalse();
  }

  @Test
  void stalledAttackerSurvivesWhileRecklessDashIsWornDown() {
    SupplyService.apply(bridge, blue, tracker); // round 1
    data.getSequence().setRoundOffset(1);
    SupplyService.apply(bridge, blue, tracker); // round 2: the detached unit hits removal

    assertThat(contested.getUnitCollection()).contains(stalledAttacker);
    assertThat(tracker.getOutOfSupplyTurns(stalledAttacker)).isZero();
    assertThat(deep.getUnitCollection()).doesNotContain(recklessDash);
  }

  private SupplyTerritoryAttachment attach(final Territory territory) {
    return SupplyTerritoryAttachment.get(territory)
        .orElseGet(
            () -> {
              final SupplyTerritoryAttachment attachment =
                  new SupplyTerritoryAttachment("supplyAttachment", territory, data);
              territory.addAttachment("supplyAttachment", attachment);
              return attachment;
            });
  }
}
