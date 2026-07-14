from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def replace(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Could not find replacement marker in {path}: {old[:120]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


write(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementRule.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import java.io.Serial;
import java.io.Serializable;
import java.util.Objects;

/** One map-defined fixed reinforcement delivery. */
public record FixedReinforcementRule(
    int round, String territoryName, String unitTypeName, int quantity) implements Serializable {
  @Serial private static final long serialVersionUID = 1L;

  public FixedReinforcementRule {
    if (round < 1) {
      throw new IllegalArgumentException("reinforcement round must be positive");
    }
    territoryName = requireName(territoryName, "territoryName");
    unitTypeName = requireName(unitTypeName, "unitTypeName");
    if (quantity < 1) {
      throw new IllegalArgumentException("reinforcement quantity must be positive");
    }
  }

  FixedReinforcementOrder toOrder() {
    return new FixedReinforcementOrder(round, territoryName, unitTypeName, quantity);
  }

  private static String requireName(final String value, final String field) {
    final String normalized = Objects.requireNonNull(value, field).trim();
    if (normalized.isEmpty()) {
      throw new IllegalArgumentException(field + " must not be blank");
    }
    return normalized;
  }
}
''',
)

write(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementOrder.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import java.io.Serial;
import java.io.Serializable;
import java.util.Objects;

/** A reinforcement delivery that is due now or waiting in the placement queue. */
public record FixedReinforcementOrder(
    int scheduledRound, String territoryName, String unitTypeName, int quantity)
    implements Serializable {
  @Serial private static final long serialVersionUID = 1L;

  public FixedReinforcementOrder {
    if (scheduledRound < 1) {
      throw new IllegalArgumentException("scheduledRound must be positive");
    }
    territoryName = requireName(territoryName, "territoryName");
    unitTypeName = requireName(unitTypeName, "unitTypeName");
    if (quantity < 1) {
      throw new IllegalArgumentException("quantity must be positive");
    }
  }

  FixedReinforcementOrder withQuantity(final int remainingQuantity) {
    return new FixedReinforcementOrder(
        scheduledRound, territoryName, unitTypeName, remainingQuantity);
  }

  private static String requireName(final String value, final String field) {
    final String normalized = Objects.requireNonNull(value, field).trim();
    if (normalized.isEmpty()) {
      throw new IllegalArgumentException(field + " must not be blank");
    }
    return normalized;
  }
}
''',
)

write(
    "game-app/game-core/src/main/java/games/strategy/triplea/attachments/FixedReinforcementAttachment.java",
    r'''package games.strategy.triplea.attachments;

import com.google.common.annotations.VisibleForTesting;
import games.strategy.engine.data.Attachable;
import games.strategy.engine.data.DefaultAttachment;
import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.IAttachment;
import games.strategy.engine.data.MutableProperty;
import games.strategy.engine.data.gameparser.GameParseException;
import games.strategy.triplea.delegate.reinforcement.FixedReinforcementRule;
import java.io.Serial;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.jetbrains.annotations.NonNls;

/** Defines deterministic, economy-independent reinforcement deliveries for one player. */
public final class FixedReinforcementAttachment extends DefaultAttachment {
  @Serial private static final long serialVersionUID = 1L;

  private final List<FixedReinforcementRule> reinforcements = new ArrayList<>();

  public FixedReinforcementAttachment(
      final String name, final Attachable attachable, final GameData gameData) {
    super(name, attachable, gameData);
  }

  public static Optional<FixedReinforcementAttachment> get(final GamePlayer player) {
    final List<FixedReinforcementAttachment> attachments =
        player.getAttachments().values().stream()
            .filter(FixedReinforcementAttachment.class::isInstance)
            .map(FixedReinforcementAttachment.class::cast)
            .toList();
    if (attachments.size() > 1) {
      throw new IllegalStateException(
          "Player " + player.getName() + " has more than one fixed reinforcement attachment");
    }
    return attachments.stream().findFirst();
  }

  @VisibleForTesting
  public void setReinforcement(final String value) throws GameParseException {
    final String[] tokens = value.split(":", -1);
    if (tokens.length != 4) {
      throw new GameParseException(
          "reinforcement must use round:territory:unitType:quantity" + thisErrorMsg());
    }
    final int round = getInt(tokens[0]);
    final String territoryName = tokens[1].trim();
    final String unitTypeName = tokens[2].trim();
    final int quantity = getInt(tokens[3]);
    if (round < 1 || quantity < 1) {
      throw new GameParseException(
          "reinforcement round and quantity must be positive" + thisErrorMsg());
    }
    if (getData().getMap().getTerritoryOrNull(territoryName) == null) {
      throw new GameParseException(
          "reinforcement territory does not exist: " + territoryName + thisErrorMsg());
    }
    if (getData().getUnitTypeList().getUnitType(unitTypeName).isEmpty()) {
      throw new GameParseException(
          "reinforcement unit type does not exist: " + unitTypeName + thisErrorMsg());
    }
    reinforcements.add(
        new FixedReinforcementRule(round, territoryName, unitTypeName, quantity));
  }

  public List<FixedReinforcementRule> getReinforcements() {
    return List.copyOf(reinforcements);
  }

  private void resetReinforcement() {
    reinforcements.clear();
  }

  @Override
  public Optional<MutableProperty<?>> getPropertyOrEmpty(@NonNls final String propertyName) {
    if ("reinforcement".equals(propertyName)) {
      return Optional.of(
          MutableProperty.of(
              this::replaceReinforcements,
              this::setReinforcement,
              this::getReinforcements,
              this::resetReinforcement));
    }
    return Optional.empty();
  }

  private void replaceReinforcements(final List<FixedReinforcementRule> values) {
    reinforcements.clear();
    reinforcements.addAll(values);
  }
}
''',
)

write(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementTracker.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import games.strategy.engine.data.GamePlayer;
import java.io.Serial;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Serializable per-game progress and queue state for fixed reinforcements. */
public final class FixedReinforcementTracker implements Serializable {
  @Serial private static final long serialVersionUID = 1L;

  private final Map<String, Integer> lastProcessedRoundByPlayer = new HashMap<>();
  private final Map<String, List<FixedReinforcementOrder>> pendingByPlayer = new HashMap<>();

  public int getLastProcessedRound(final GamePlayer player) {
    return lastProcessedRoundByPlayer.getOrDefault(player.getName(), 0);
  }

  public List<FixedReinforcementOrder> getPending(final GamePlayer player) {
    return List.copyOf(pendingByPlayer.getOrDefault(player.getName(), List.of()));
  }

  boolean shouldProcess(final GamePlayer player, final int currentRound) {
    return currentRound > getLastProcessedRound(player);
  }

  List<FixedReinforcementOrder> getOrdersForRound(
      final GamePlayer player,
      final int currentRound,
      final List<FixedReinforcementRule> schedule) {
    if (!shouldProcess(player, currentRound)) {
      return List.of();
    }
    final int lastProcessedRound = getLastProcessedRound(player);
    final List<FixedReinforcementOrder> orders = new ArrayList<>(getPending(player));
    schedule.stream()
        .filter(rule -> rule.round() > lastProcessedRound && rule.round() <= currentRound)
        .map(FixedReinforcementRule::toOrder)
        .forEach(orders::add);
    return List.copyOf(orders);
  }

  void completeRound(
      final GamePlayer player,
      final int currentRound,
      final List<FixedReinforcementOrder> remainingOrders) {
    lastProcessedRoundByPlayer.put(player.getName(), currentRound);
    if (remainingOrders.isEmpty()) {
      pendingByPlayer.remove(player.getName());
    } else {
      pendingByPlayer.put(player.getName(), List.copyOf(remainingOrders));
    }
  }
}
''',
)

write(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementService.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.Unit;
import games.strategy.engine.data.UnitType;
import games.strategy.engine.data.changefactory.ChangeFactory;
import games.strategy.engine.delegate.IDelegateBridge;
import games.strategy.engine.history.IDelegateHistoryWriter;
import games.strategy.triplea.attachments.FixedReinforcementAttachment;
import games.strategy.triplea.delegate.StackCapacityResolver;
import java.util.ArrayList;
import java.util.List;

/** Places map-defined reinforcements and carries blocked units into a deterministic queue. */
public final class FixedReinforcementService {
  private FixedReinforcementService() {}

  public static void apply(
      final IDelegateBridge bridge,
      final GamePlayer player,
      final FixedReinforcementTracker tracker) {
    final GameData data = bridge.getData();
    final int currentRound = data.getSequence().getRound();
    if (!tracker.shouldProcess(player, currentRound)) {
      return;
    }
    final List<FixedReinforcementRule> schedule =
        FixedReinforcementAttachment.get(player)
            .map(FixedReinforcementAttachment::getReinforcements)
            .orElse(List.of());
    final List<FixedReinforcementOrder> orders =
        tracker.getOrdersForRound(player, currentRound, schedule);
    final List<FixedReinforcementOrder> remaining = new ArrayList<>();
    final IDelegateHistoryWriter history = bridge.getHistoryWriter();
    if (!orders.isEmpty()) {
      history.startEvent(
          "Fixed reinforcements for " + player.getName() + " in round " + currentRound);
    }
    for (final FixedReinforcementOrder order : orders) {
      final Territory territory = data.getMap().getTerritoryOrNull(order.territoryName());
      final UnitType unitType =
          data.getUnitTypeList().getUnitType(order.unitTypeName()).orElse(null);
      if (territory == null || unitType == null) {
        remaining.add(order);
        history.addChildToEvent(
            "Queued " + describe(order) + " because its map target is unavailable");
        continue;
      }
      if (!isFriendlyDestination(data, player, territory)) {
        remaining.add(order);
        history.addChildToEvent(
            "Queued " + describe(order) + " because " + territory.getName() + " is not allied");
        continue;
      }
      final List<Unit> candidates = unitType.createTemp(order.quantity(), player);
      final int acceptedCount =
          StackCapacityResolver.filterUnitsToFit(candidates, player, territory, List.of()).size();
      if (acceptedCount > 0) {
        final List<Unit> placed = unitType.create(acceptedCount, player);
        bridge.addChange(ChangeFactory.addUnits(territory, placed));
        history.addChildToEvent(
            "Placed "
                + acceptedCount
                + " "
                + unitType.getName()
                + " in "
                + territory.getName(),
            placed);
      }
      final int remainingQuantity = order.quantity() - acceptedCount;
      if (remainingQuantity > 0) {
        final FixedReinforcementOrder queued = order.withQuantity(remainingQuantity);
        remaining.add(queued);
        history.addChildToEvent(
            "Queued " + describe(queued) + " because terrain capacity is full");
      }
    }
    tracker.completeRound(player, currentRound, remaining);
  }

  private static boolean isFriendlyDestination(
      final GameData data, final GamePlayer player, final Territory territory) {
    return player.equals(territory.getOwner())
        || data.getRelationshipTracker().isAllied(player, territory.getOwner());
  }

  private static String describe(final FixedReinforcementOrder order) {
    return order.quantity()
        + " "
        + order.unitTypeName()
        + " for "
        + order.territoryName()
        + " (scheduled round "
        + order.scheduledRound()
        + ")";
  }
}
''',
)

write(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementObservation.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import java.util.List;

/** Strategic-agent view of fixed reinforcement progress and future deliveries. */
public record FixedReinforcementObservation(
    int schemaVersion,
    String player,
    int currentRound,
    int lastProcessedRound,
    List<Entry> pending,
    List<Entry> scheduled) {
  public static final int SCHEMA_VERSION = 1;

  public FixedReinforcementObservation {
    pending = List.copyOf(pending);
    scheduled = List.copyOf(scheduled);
  }

  public record Entry(int round, String territory, String unitType, int quantity) {
    static Entry from(final FixedReinforcementOrder order) {
      return new Entry(
          order.scheduledRound(),
          order.territoryName(),
          order.unitTypeName(),
          order.quantity());
    }

    static Entry from(final FixedReinforcementRule rule) {
      return new Entry(rule.round(), rule.territoryName(), rule.unitTypeName(), rule.quantity());
    }
  }
}
''',
)

write(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementObservationFactory.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.GameState;
import games.strategy.triplea.attachments.FixedReinforcementAttachment;
import games.strategy.triplea.delegate.MoveDelegate;
import java.util.List;

/** Builds a stable reinforcement observation for future strategic environments. */
public final class FixedReinforcementObservationFactory {
  private FixedReinforcementObservationFactory() {}

  public static FixedReinforcementObservation create(
      final GameState data, final GamePlayer player) {
    if (!(data.getMoveDelegate() instanceof MoveDelegate moveDelegate)) {
      throw new IllegalStateException("Fixed reinforcement observations require MoveDelegate");
    }
    return create(data, player, moveDelegate.getFixedReinforcementTracker());
  }

  public static FixedReinforcementObservation create(
      final GameState data,
      final GamePlayer player,
      final FixedReinforcementTracker tracker) {
    final int currentRound = data.getSequence().getRound();
    final List<FixedReinforcementObservation.Entry> pending =
        tracker.getPending(player).stream().map(FixedReinforcementObservation.Entry::from).toList();
    final List<FixedReinforcementObservation.Entry> scheduled =
        FixedReinforcementAttachment.get(player)
            .map(FixedReinforcementAttachment::getReinforcements)
            .orElse(List.of())
            .stream()
            .filter(rule -> rule.round() > tracker.getLastProcessedRound(player))
            .map(FixedReinforcementObservation.Entry::from)
            .toList();
    return new FixedReinforcementObservation(
        FixedReinforcementObservation.SCHEMA_VERSION,
        player.getName(),
        currentRound,
        tracker.getLastProcessedRound(player),
        pending,
        scheduled);
  }
}
''',
)

write(
    "game-app/game-core/src/test/java/games/strategy/triplea/attachments/FixedReinforcementAttachmentTest.java",
    r'''package games.strategy.triplea.attachments;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.UnitType;
import games.strategy.engine.data.gameparser.GameParseException;
import games.strategy.triplea.Constants;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class FixedReinforcementAttachmentTest {
  private final GameData data = new GameData();
  private final GamePlayer player = new GamePlayer("Allies", data);
  private final FixedReinforcementAttachment attachment =
      new FixedReinforcementAttachment("fixedReinforcementAttachment", player, data);

  @BeforeEach
  void setUp() {
    data.getPlayerList().addPlayerId(player);
    data.getMap().addTerritory(new Territory("Front", data));
    final UnitType infantry = new UnitType("infantry", data);
    infantry.addAttachment(
        Constants.UNIT_ATTACHMENT_NAME,
        new UnitAttachment(Constants.UNIT_ATTACHMENT_NAME, infantry, data));
    data.getUnitTypeList().addUnitType(infantry);
    player.addAttachment("fixedReinforcementAttachment", attachment);
  }

  @Test
  void parsesRepeatedRulesInDeclarationOrder() throws Exception {
    attachment.setReinforcement("1:Front:infantry:3");
    attachment.setReinforcement("2:Front:infantry:1");

    assertThat(attachment.getReinforcements())
        .extracting("round", "territoryName", "unitTypeName", "quantity")
        .containsExactly(
            org.assertj.core.groups.Tuple.tuple(1, "Front", "infantry", 3),
            org.assertj.core.groups.Tuple.tuple(2, "Front", "infantry", 1));
    assertThat(FixedReinforcementAttachment.get(player)).containsSame(attachment);
    assertThat(attachment.getPropertyOrEmpty("reinforcement")).isPresent();
  }

  @Test
  void rejectsMalformedOrUnknownTargets() {
    assertThatThrownBy(() -> attachment.setReinforcement("0:Front:infantry:1"))
        .isInstanceOf(GameParseException.class);
    assertThatThrownBy(() -> attachment.setReinforcement("1:Missing:infantry:1"))
        .isInstanceOf(GameParseException.class);
    assertThatThrownBy(() -> attachment.setReinforcement("1:Front:missing:1"))
        .isInstanceOf(GameParseException.class);
    assertThatThrownBy(() -> attachment.setReinforcement("1:Front:infantry"))
        .isInstanceOf(GameParseException.class);
  }
}
''',
)

write(
    "game-app/game-core/src/test/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementTrackerTest.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import games.strategy.engine.data.GamePlayer;
import java.util.List;
import org.junit.jupiter.api.Test;

class FixedReinforcementTrackerTest {
  private final GamePlayer player = player("Allies");

  @Test
  void queuesFirstThenAddsNewlyDueRulesAndProcessesOnlyOncePerRound() {
    final FixedReinforcementTracker tracker = new FixedReinforcementTracker();
    final List<FixedReinforcementRule> schedule =
        List.of(
            new FixedReinforcementRule(1, "Front", "infantry", 2),
            new FixedReinforcementRule(3, "Front", "armor", 1));

    final List<FixedReinforcementOrder> roundOne =
        tracker.getOrdersForRound(player, 1, schedule);
    assertThat(roundOne)
        .containsExactly(new FixedReinforcementOrder(1, "Front", "infantry", 2));
    tracker.completeRound(
        player, 1, List.of(new FixedReinforcementOrder(1, "Front", "infantry", 1)));

    assertThat(tracker.getOrdersForRound(player, 1, schedule)).isEmpty();
    assertThat(tracker.getOrdersForRound(player, 3, schedule))
        .containsExactly(
            new FixedReinforcementOrder(1, "Front", "infantry", 1),
            new FixedReinforcementOrder(3, "Front", "armor", 1));
  }

  private static GamePlayer player(final String name) {
    final GamePlayer player = mock(GamePlayer.class);
    when(player.getName()).thenReturn(name);
    return player;
  }
}
''',
)

write(
    "game-app/game-core/src/test/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementServiceTest.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import games.strategy.engine.data.Change;
import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.UnitType;
import games.strategy.engine.delegate.IDelegateBridge;
import games.strategy.engine.history.IDelegateHistoryWriter;
import games.strategy.triplea.Constants;
import games.strategy.triplea.attachments.FixedReinforcementAttachment;
import games.strategy.triplea.attachments.TerritoryAttachment;
import games.strategy.triplea.attachments.UnitAttachment;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class FixedReinforcementServiceTest {
  private final GameData data = new GameData();
  private final GamePlayer player = new GamePlayer("Allies", data);
  private final Territory front = new Territory("Front", data);
  private final UnitType infantry = new UnitType("infantry", data);
  private final FixedReinforcementAttachment attachment =
      new FixedReinforcementAttachment("fixedReinforcementAttachment", player, data);
  private final FixedReinforcementTracker tracker = new FixedReinforcementTracker();
  private final IDelegateBridge bridge = mock(IDelegateBridge.class);

  @BeforeEach
  void setUp() {
    data.getPlayerList().addPlayerId(player);
    data.getMap().addTerritory(front);
    front.setOwner(player);
    TerritoryAttachment.add(
        front, new TerritoryAttachment(Constants.TERRITORY_ATTACHMENT_NAME, front, data));
    infantry.addAttachment(
        Constants.UNIT_ATTACHMENT_NAME,
        new UnitAttachment(Constants.UNIT_ATTACHMENT_NAME, infantry, data));
    data.getUnitTypeList().addUnitType(infantry);
    player.addAttachment("fixedReinforcementAttachment", attachment);
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
  void placesDueUnitsAndIsIdempotentWithinTheRound() throws Exception {
    attachment.setReinforcement("1:Front:infantry:2");

    FixedReinforcementService.apply(bridge, player, tracker);
    FixedReinforcementService.apply(bridge, player, tracker);

    assertThat(front.getUnitCollection().getUnitCount()).isEqualTo(2);
    assertThat(tracker.getPending(player)).isEmpty();
    assertThat(tracker.getLastProcessedRound(player)).isEqualTo(1);
  }

  @Test
  void carriesBlockedOrdersToTheNextOwnerTurn() throws Exception {
    attachment.setReinforcement("1:Front:infantry:3");
    front.setOwner(data.getPlayerList().getNullPlayer());

    FixedReinforcementService.apply(bridge, player, tracker);
    assertThat(front.getUnitCollection().getUnitCount()).isZero();
    assertThat(tracker.getPending(player))
        .containsExactly(new FixedReinforcementOrder(1, "Front", "infantry", 3));

    front.setOwner(player);
    data.getSequence().setRoundOffset(1);
    FixedReinforcementService.apply(bridge, player, tracker);

    assertThat(front.getUnitCollection().getUnitCount()).isEqualTo(3);
    assertThat(tracker.getPending(player)).isEmpty();
  }
}
''',
)

write(
    "game-app/game-core/src/test/java/games/strategy/triplea/delegate/reinforcement/FixedReinforcementObservationFactoryTest.java",
    r'''package games.strategy.triplea.delegate.reinforcement;

import static org.assertj.core.api.Assertions.assertThat;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.UnitType;
import games.strategy.triplea.Constants;
import games.strategy.triplea.attachments.FixedReinforcementAttachment;
import games.strategy.triplea.attachments.UnitAttachment;
import java.util.List;
import org.junit.jupiter.api.Test;

class FixedReinforcementObservationFactoryTest {
  @Test
  void exposesQueuedAndScheduledDeliveriesInStableOrder() throws Exception {
    final GameData data = new GameData();
    final GamePlayer player = new GamePlayer("Allies", data);
    data.getPlayerList().addPlayerId(player);
    data.getMap().addTerritory(new Territory("Front", data));
    final UnitType infantry = new UnitType("infantry", data);
    infantry.addAttachment(
        Constants.UNIT_ATTACHMENT_NAME,
        new UnitAttachment(Constants.UNIT_ATTACHMENT_NAME, infantry, data));
    data.getUnitTypeList().addUnitType(infantry);
    final FixedReinforcementAttachment attachment =
        new FixedReinforcementAttachment("fixedReinforcementAttachment", player, data);
    attachment.setReinforcement("2:Front:infantry:2");
    player.addAttachment("fixedReinforcementAttachment", attachment);
    final FixedReinforcementTracker tracker = new FixedReinforcementTracker();
    tracker.completeRound(
        player, 1, List.of(new FixedReinforcementOrder(1, "Front", "infantry", 1)));

    final FixedReinforcementObservation observation =
        FixedReinforcementObservationFactory.create(data, player, tracker);

    assertThat(observation.schemaVersion()).isEqualTo(1);
    assertThat(observation.pending())
        .containsExactly(new FixedReinforcementObservation.Entry(1, "Front", "infantry", 1));
    assertThat(observation.scheduled())
        .containsExactly(new FixedReinforcementObservation.Entry(2, "Front", "infantry", 2));
  }
}
''',
)

write(
    "docs/development/fixed-reinforcements.md",
    r'''# Fixed reinforcement scenario system

Small Front scenarios can omit purchase and placement steps and deliver map-authored units at the start of each player's Combat Move.

```xml
<attachment
    name="fixedReinforcementAttachment"
    attachTo="Allies"
    javaClass="games.strategy.triplea.attachments.FixedReinforcementAttachment"
    type="player">
  <option name="reinforcement" value="1:Western Front:infantry:3"/>
  <option name="reinforcement" value="2:Western Front:artillery:1"/>
</attachment>
```

The value format is `round:territory:unitType:quantity`. Round and quantity are positive integers. Territory and unit-type names are validated while the map is parsed. Multiple options are processed in declaration order, which is also the priority order when terrain capacity is limited.

At the first Combat Move initialization for the owning player, the engine combines previously queued orders with all schedule entries that became due since that player's last processed round. Queued orders are attempted first. A destination must be owned by the player or an ally. `StackCapacityResolver` then applies the same `stackCapacity` and `stackCost` rules used by movement, placement, reinforcement batches, and retreat.

Partial placement is allowed. Units that do not fit remain in a serializable queue and are retried at the start of the player's next round. The tracker records the last processed player-round, so saving, loading, or re-entering the same movement phase cannot duplicate deliveries.

`FixedReinforcementObservationFactory` exposes schema version, current and last-processed rounds, queued orders, and future schedule entries for the later strategic-agent environment.

The scenario should remove economic `PurchaseDelegate` and `PlaceDelegate` steps from its sequence. Game-over handling remains on TripleA's existing EndRound, rules attachment, victory-city, or trigger victory paths; the reinforcement system intentionally does not introduce a second game termination mechanism.
''',
)

move_delegate = "game-app/game-core/src/main/java/games/strategy/triplea/delegate/MoveDelegate.java"
replace(
    move_delegate,
    "import games.strategy.triplea.delegate.move.validation.MoveValidator;\n",
    "import games.strategy.triplea.delegate.move.validation.MoveValidator;\n"
    "import games.strategy.triplea.delegate.reinforcement.FixedReinforcementService;\n"
    "import games.strategy.triplea.delegate.reinforcement.FixedReinforcementTracker;\n",
)
replace(
    move_delegate,
    "  private IntegerMap<Territory> pusLost = new IntegerMap<>();\n",
    "  private IntegerMap<Territory> pusLost = new IntegerMap<>();\n"
    "  private FixedReinforcementTracker fixedReinforcementTracker =\n"
    "      new FixedReinforcementTracker();\n",
)
replace(
    move_delegate,
    "      // repair 2-hit units at beginning of turn",
    "      if (GameStepPropertiesHelper.isCombatMove(data)) {\n"
    "        FixedReinforcementService.apply(bridge, player, fixedReinforcementTracker);\n"
    "      }\n\n"
    "      // repair 2-hit units at beginning of turn",
)
replace(
    move_delegate,
    "    state.pusLost = pusLost;\n    return state;",
    "    state.pusLost = pusLost;\n"
    "    state.fixedReinforcementTracker = fixedReinforcementTracker;\n"
    "    return state;",
)
replace(
    move_delegate,
    "    pusLost = s.pusLost;\n  }",
    "    pusLost = s.pusLost;\n"
    "    fixedReinforcementTracker =\n"
    "        s.fixedReinforcementTracker == null\n"
    "            ? new FixedReinforcementTracker()\n"
    "            : s.fixedReinforcementTracker;\n"
    "  }\n\n"
    "  public FixedReinforcementTracker getFixedReinforcementTracker() {\n"
    "    return fixedReinforcementTracker;\n"
    "  }",
)

state_path = "game-app/game-core/src/main/java/games/strategy/triplea/delegate/MoveExtendedDelegateState.java"
replace(
    state_path,
    "import games.strategy.engine.data.Territory;\n",
    "import games.strategy.engine.data.Territory;\n"
    "import games.strategy.triplea.delegate.reinforcement.FixedReinforcementTracker;\n",
)
replace(
    state_path,
    "  IntegerMap<Territory> pusLost;\n",
    "  IntegerMap<Territory> pusLost;\n"
    "  FixedReinforcementTracker fixedReinforcementTracker;\n",
)

roadmap = "docs/development/small-front-roadmap.md"
replace(
    roadmap,
    "## 8. Fixed reinforcement scenario system\n\n- remove economic purchase flow from the scenario\n- reinforcement schedules by player and turn\n- capacity-aware reinforcement placement\n- reinforcement queue observation for strategic agents\n- scenario victory conditions\n\nExit condition: the map plays as a narrow-front reinforcement game without IC income.",
    "## 8. Fixed reinforcement scenario system\n\nStatus: in progress.\n\n- player and round based reinforcement schedule attachment\n- Combat Move start integration without purchase or placement delegates\n- shared terrain-capacity validation and partial placement\n- deterministic serializable queue with save/load idempotence\n- versioned reinforcement observation for strategic agents\n- compatibility with existing EndRound and trigger victory conditions\n\nExit condition: the map plays as a narrow-front reinforcement game without IC income.",
)
