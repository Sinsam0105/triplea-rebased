package games.strategy.triplea.delegate.reinforcement;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import games.strategy.engine.data.Change;
import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.gameparser.GameParser;
import games.strategy.engine.data.gameparser.XmlGameElementMapper;
import games.strategy.engine.delegate.IDelegateBridge;
import games.strategy.engine.history.IDelegateHistoryWriter;
import games.strategy.triplea.attachments.AbstractTriggerAttachment;
import games.strategy.triplea.attachments.TriggerAttachment;
import games.strategy.triplea.attachments.UnitAttachment;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import org.junit.jupiter.api.Test;

/**
 * Verifies the generated Meuse Corridor XML parses in the engine and that the round-5
 * redeployment-recovery trigger both loads and actually fires (T6).
 */
class MeuseMapLoadTest {
  private static final String REINFORCEMENT_STEP = "germanReinforcement";

  @Test
  void generatedMapParsesAndDeclaresLoweredRedeployment() throws Exception {
    final GameData data = loadMap();

    // Rounds 1-4: afmov starts at the combat-movement value.
    assertThat(redeployment(data, "americanInfantry")).isEqualTo(1);
    assertThat(redeployment(data, "armour")).isEqualTo(2);
    assertThat(redeployment(data, "mechanized")).isEqualTo(2);
    assertThat(redeployment(data, "selfPropelledArtillery")).isEqualTo(2);
  }

  @Test
  void redeploymentRecoversOnlyFromRoundFive() throws Exception {
    final GameData data = loadMap();
    final IDelegateBridge bridge = bridgeFor(data);
    final int baseRound = data.getSequence().getRound();

    // Round 3: the rounds 5+ condition is not met, so nothing recovers.
    fireReinforcementTriggers(data, bridge, baseRound, 3);
    assertThat(redeployment(data, "americanInfantry")).isEqualTo(1);
    assertThat(redeployment(data, "armour")).isEqualTo(2);

    // Round 5: the trigger fires and restores the pre-existing redeployment reach.
    fireReinforcementTriggers(data, bridge, baseRound, 5);
    assertThat(redeployment(data, "americanInfantry")).isEqualTo(2);
    assertThat(redeployment(data, "armour")).isEqualTo(3);
    assertThat(redeployment(data, "mechanized")).isEqualTo(3);
    assertThat(redeployment(data, "selfPropelledArtillery")).isEqualTo(3);
  }

  private static void fireReinforcementTriggers(
      final GameData data, final IDelegateBridge bridge, final int baseRound, final int round) {
    data.getSequence().setRoundOffset(round - baseRound);
    TriggerAttachment.collectAndFireTriggers(
        new HashSet<>(data.getPlayerList().getPlayers()),
        AbstractTriggerAttachment.availableUses.and(
            AbstractTriggerAttachment.whenOrDefaultMatch(
                AbstractTriggerAttachment.BEFORE, REINFORCEMENT_STEP)),
        bridge,
        AbstractTriggerAttachment.BEFORE,
        REINFORCEMENT_STEP);
  }

  private static IDelegateBridge bridgeFor(final GameData data) {
    final IDelegateBridge bridge = mock(IDelegateBridge.class);
    when(bridge.getData()).thenReturn(data);
    when(bridge.getHistoryWriter()).thenReturn(mock(IDelegateHistoryWriter.class));
    doAnswer(
            invocation -> {
              data.performChange(invocation.getArgument(0, Change.class));
              return null;
            })
        .when(bridge)
        .addChange(any(Change.class));
    return bridge;
  }

  private static int redeployment(final GameData data, final String unit) {
    final UnitAttachment attachment =
        data.getUnitTypeList().getUnitTypeOrThrow(unit).getUnitAttachment();
    final GamePlayer anyPlayer = data.getPlayerList().getPlayers().iterator().next();
    return attachment.getRedeploymentMovement(anyPlayer);
  }

  private static GameData loadMap() throws Exception {
    final Path map = locateMap();
    return GameParser.parse(map, new XmlGameElementMapper(), false)
        .orElseThrow(() -> new IllegalStateException("parse returned empty for " + map));
  }

  private static Path locateMap() {
    Path dir = Path.of(System.getProperty("user.dir")).toAbsolutePath();
    for (int i = 0; i < 6 && dir != null; i++, dir = dir.getParent()) {
      final Path candidate = dir.resolve("maps/small_front_meuse/map/games/Small_Front_Meuse.xml");
      if (Files.exists(candidate)) {
        return candidate;
      }
    }
    throw new IllegalStateException(
        "Could not find Small_Front_Meuse.xml from " + System.getProperty("user.dir"));
  }
}
