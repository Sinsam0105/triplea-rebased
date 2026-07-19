package games.strategy.engine.data;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;

import games.strategy.engine.data.gameparser.GameParser;
import games.strategy.engine.framework.ServerGame;
import games.strategy.engine.framework.startup.ui.PlayerTypes;
import games.strategy.engine.player.Player;
import games.strategy.net.LocalNoOpMessenger;
import games.strategy.net.Messengers;
import games.strategy.net.websocket.ClientNetworkBridge;
import games.strategy.triplea.delegate.scoring.SmallFrontScoringService;
import games.strategy.triplea.delegate.supply.SupplyNetworkResolver;
import java.io.IOException;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.triplea.game.server.HeadlessGameServer;
import org.triplea.game.server.HeadlessLaunchAction;

/** Smoke coverage for the Vistula Withdrawal scenario. */
class SmallFrontPolandGameTest {
  private static final Path MAP_XML =
      Path.of("src", "test", "resources", "map-xmls", "Small_Front_Poland.xml");

  @BeforeAll
  static void setUp() throws IOException {
    GameTestUtils.setUp();
  }

  @Test
  void bothSidesFightAndReachScenarioScoring() {
    final GameData data = loadMap();
    final Map<String, String> ownersAtStart = owners(data);

    final ServerGame game = allSmallFrontAi(data);
    game.setStopGameOnDelegateExecutionStop(true);
    while (!game.isGameOver() && data.getSequence().getRound() <= 11) {
      game.runNextStep();
    }

    assertThat(game.isGameOver()).isTrue();
    final Map<String, String> ownersAtEnd = owners(data);
    final List<String> changedHands =
        ownersAtStart.keySet().stream()
            .filter(name -> !ownersAtStart.get(name).equals(ownersAtEnd.get(name)))
            .sorted()
            .toList();
    assertThat(changedHands).as("no territory changed hands in a whole game").isNotEmpty();
    assertThat(named(SmallFrontScoringService.score(data))).containsOnlyKeys("Germans", "Poland");
  }

  @Test
  void vistulaSupplyUsesTwoGatewaysWithoutOffRoadBypasses() {
    final GameData data = loadMap();
    final Territory warsaw = data.getMap().getTerritoryOrThrow("Warsaw");
    final Territory siedlce = data.getMap().getTerritoryOrThrow("Siedlce");
    final Territory deblin = data.getMap().getTerritoryOrThrow("Deblin");
    final Territory lublin = data.getMap().getTerritoryOrThrow("Lublin");
    final Territory modlin = data.getMap().getTerritoryOrThrow("Modlin");
    final Territory lukow = data.getMap().getTerritoryOrThrow("Lukow");
    final Territory zamosc = data.getMap().getTerritoryOrThrow("Zamosc");

    assertThat(SupplyNetworkResolver.getRoadNeighbors(warsaw, data)).contains(siedlce, deblin);
    assertThat(SupplyNetworkResolver.getRoadNeighbors(deblin, data)).contains(warsaw, lublin);
    assertThat(SupplyNetworkResolver.getRoadNeighbors(modlin, data)).doesNotContain(siedlce);
    assertThat(SupplyNetworkResolver.getRoadNeighbors(deblin, data)).doesNotContain(lukow, zamosc);
  }

  private static GameData loadMap() {
    return GameParser.parse(MAP_XML, false)
        .orElseThrow(() -> new AssertionError("map did not parse"));
  }

  private static Map<String, String> owners(final GameData data) {
    final Map<String, String> owners = new HashMap<>();
    data.getMap().getTerritories().forEach(t -> owners.put(t.getName(), t.getOwner().getName()));
    return owners;
  }

  private static ServerGame allSmallFrontAi(final GameData data) {
    final Map<String, PlayerTypes.Type> playerTypes = new HashMap<>();
    for (final GamePlayer player : data.getPlayerList().getPlayers()) {
      playerTypes.put(player.getName(), PlayerTypes.SMALL_FRONT_AI);
    }
    final Set<Player> gamePlayers = data.getGameLoader().newPlayers(playerTypes);
    final HeadlessLaunchAction launchAction =
        new HeadlessLaunchAction(mock(HeadlessGameServer.class));
    final ServerGame game =
        new ServerGame(
            data,
            gamePlayers,
            new HashMap<>(),
            new Messengers(new LocalNoOpMessenger()),
            ClientNetworkBridge.NO_OP_SENDER,
            launchAction);
    game.setDelegateAutosavesEnabled(false);
    data.getGameLoader().startGame(game, gamePlayers, launchAction, null);
    return game;
  }

  private static Map<String, Integer> named(final Map<GamePlayer, Integer> scores) {
    final Map<String, Integer> byName = new HashMap<>();
    scores.forEach((player, score) -> byName.put(player.getName(), score));
    return byName;
  }
}
