package games.strategy.triplea.attachments;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.gameparser.GameParseException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class SupplyTerritoryAttachmentTest {
  private final GameData data = new GameData();
  private final GamePlayer blue = new GamePlayer("Blue", data);
  private final GamePlayer red = new GamePlayer("Red", data);
  private final Territory depot = new Territory("Depot", data);
  private final Territory front = new Territory("Front", data);
  private final SupplyTerritoryAttachment attachment =
      new SupplyTerritoryAttachment("supplyAttachment", depot, data);

  @BeforeEach
  void setUp() {
    data.getPlayerList().addPlayerId(blue);
    data.getPlayerList().addPlayerId(red);
    data.getMap().addTerritory(depot);
    data.getMap().addTerritory(front);
    depot.addAttachment("supplyAttachment", attachment);
  }

  @Test
  void parsesSupplySourceAndRepeatedRoadConnections() throws Exception {
    attachment.setSupplySource("true");
    attachment.setRoadConnection("Front");
    attachment.setRoadConnection("Front");

    assertThat(attachment.getSupplySource()).isTrue();
    assertThat(attachment.getRoadConnections()).containsExactly(front);
    assertThat(SupplyTerritoryAttachment.get(depot)).containsSame(attachment);
    assertThat(attachment.getPropertyOrEmpty("supplySource")).isPresent();
    assertThat(attachment.getPropertyOrEmpty("roadConnection")).isPresent();
  }

  @Test
  void supplySourceOwnerRestrictsWhichPlayersMayDrawFromTheSource() throws Exception {
    attachment.setSupplySource("true");

    // No owner declared: the source is usable by any player.
    assertThat(attachment.isSupplySourceFor(blue)).isTrue();
    assertThat(attachment.isSupplySourceFor(red)).isTrue();

    attachment.setSupplySourceOwner("Blue");

    assertThat(attachment.getSupplySourceOwners()).containsExactly(blue);
    assertThat(attachment.isSupplySourceFor(blue)).isTrue();
    assertThat(attachment.isSupplySourceFor(red)).isFalse();
    assertThat(attachment.getPropertyOrEmpty("supplySourceOwner")).isPresent();
  }

  @Test
  void supplySourceOwnerIsMeaninglessWithoutTheSupplySourceFlag() throws Exception {
    attachment.setSupplySourceOwner("Blue");

    // Not a source at all, so ownership never grants supply.
    assertThat(attachment.isSupplySourceFor(blue)).isFalse();
  }

  @Test
  void rejectsUnknownSupplySourceOwner() {
    assertThatThrownBy(() -> attachment.setSupplySourceOwner("Green"))
        .isInstanceOf(GameParseException.class);
  }

  @Test
  void rejectsUnknownRoadTargetsAndSelfConnections() {
    assertThatThrownBy(() -> attachment.setRoadConnection("Missing"))
        .isInstanceOf(GameParseException.class);

    assertThatThrownBy(
            () -> {
              attachment.setRoadConnection("Depot");
              attachment.validate(data);
            })
        .isInstanceOf(GameParseException.class);
  }
}
