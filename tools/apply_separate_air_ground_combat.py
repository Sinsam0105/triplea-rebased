from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def replace(path: str, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise RuntimeError(f"replacement marker not found in {path}: {old[:160]!r}")
    write(path, text.replace(old, new, 1))


replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/Constants.java",
    '  String AIR_BATTLE_ROUNDS = "Air Battle Rounds";\n',
    '  String SEPARATE_AIR_AND_GROUND_COMBAT = "Separate Air And Ground Combat";\n'
    '  String AIR_BATTLE_ROUNDS = "Air Battle Rounds";\n',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/Properties.java",
    "  public static int getAirBattleRounds(final GameProperties properties) {\n"
    "    return properties.get(AIR_BATTLE_ROUNDS, 1);\n"
    "  }\n",
    "  public static boolean getSeparateAirAndGroundCombat(final GameProperties properties) {\n"
    "    return properties.get(SEPARATE_AIR_AND_GROUND_COMBAT, false);\n"
    "  }\n\n"
    "  public static int getAirBattleRounds(final GameProperties properties) {\n"
    "    return properties.get(AIR_BATTLE_ROUNDS, 1);\n"
    "  }\n",
)

write(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/CombatDomainParticipants.java",
    '''package games.strategy.triplea.delegate.battle;

import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.GameState;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.Unit;
import games.strategy.triplea.Properties;
import games.strategy.triplea.delegate.Matches;
import java.util.Collection;
import java.util.List;
import java.util.function.Predicate;

/** Selects battle participants when air and ground combat use independent domains. */
final class CombatDomainParticipants {
  private CombatDomainParticipants() {}

  static boolean separatesAirAndGround(final GameState data) {
    return Properties.getSeparateAirAndGroundCombat(data.getProperties());
  }

  static List<Unit> airBattleAttackers(final Collection<Unit> units) {
    return units.stream().filter(AirBattle.attackingGroundSeaBattleEscorts()).toList();
  }

  static List<Unit> groundBattleAttackers(
      final Collection<Unit> units, final GameState data) {
    if (!separatesAirAndGround(data)) {
      return List.copyOf(units);
    }
    return units.stream().filter(Matches.unitIsNotAir()).toList();
  }

  static List<Unit> groundBattleDefenders(
      final Territory territory, final GamePlayer attacker, final GameState data) {
    return groundBattleDefenders(territory.getUnits(), attacker, data);
  }

  static List<Unit> groundBattleDefenders(
      final Collection<Unit> units, final GamePlayer attacker, final GameState data) {
    Predicate<Unit> enemy = Matches.enemyUnit(attacker);
    if (separatesAirAndGround(data)) {
      enemy = enemy.and(Matches.unitIsNotAir());
    }
    return units.stream().filter(enemy).toList();
  }

  static boolean hasGroundCombatDefenders(
      final Territory territory, final GamePlayer attacker, final GameState data) {
    return groundBattleDefenders(territory, attacker, data).stream()
        .anyMatch(Matches.unitIsInfrastructure().negate());
  }

  static Predicate<Territory> territoryIsEmptyOfGroundCombatUnits(
      final GamePlayer attacker, final GameState data) {
    if (!separatesAirAndGround(data)) {
      return Matches.territoryIsEmptyOfCombatUnits(attacker);
    }
    return territory -> !hasGroundCombatDefenders(territory, attacker, data);
  }
}
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/BattleTracker.java",
    '''    } else {
      // create both an air battle and a normal battle
      if (!airBattleCompleted
          && Properties.getBattlesMayBePreceededByAirBattles(data.getProperties())
          && AirBattle.territoryCouldPossiblyHaveAirBattleDefenders(
              route.getEnd(), gamePlayer, data, false)) {
        addAirBattle(
            route,
            CollectionUtils.getMatches(units, AirBattle.attackingGroundSeaBattleEscorts()),
            gamePlayer,
            data,
            BattleType.AIR_BATTLE);
      }
      final Change change = addMustFightBattleChange(route, units, gamePlayer, data);
      addChange(bridge, changeTracker, change);
      if (units.stream().anyMatch(Matches.unitIsLand().or(Matches.unitIsSea()))) {
        addEmptyBattle(
            route, units, gamePlayer, bridge, changeTracker, unitsNotUnloadedTilEndOfRoute);
      }
    }
''',
    '''    } else {
      final boolean separateAirAndGround =
          CombatDomainParticipants.separatesAirAndGround(data);
      final Collection<Unit> airBattleUnits =
          CombatDomainParticipants.airBattleAttackers(units);
      if (!airBattleCompleted
          && (separateAirAndGround
              || Properties.getBattlesMayBePreceededByAirBattles(data.getProperties()))
          && AirBattle.territoryCouldPossiblyHaveAirBattleDefenders(
              route.getEnd(), gamePlayer, data, false)) {
        addAirBattle(route, airBattleUnits, gamePlayer, data, BattleType.AIR_BATTLE);
      }
      final Collection<Unit> groundBattleUnits =
          CombatDomainParticipants.groundBattleAttackers(units, data);
      if (!groundBattleUnits.isEmpty()) {
        final Change change =
            addMustFightBattleChange(route, groundBattleUnits, gamePlayer, data);
        addChange(bridge, changeTracker, change);
        if (groundBattleUnits.stream().anyMatch(Matches.unitIsLand().or(Matches.unitIsSea()))) {
          addEmptyBattle(
              route,
              groundBattleUnits,
              gamePlayer,
              bridge,
              changeTracker,
              unitsNotUnloadedTilEndOfRoute);
        }
      }
    }
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/BattleTracker.java",
    '''    final Predicate<Territory> conquerable =
        Matches.territoryIsEmptyOfCombatUnits(gamePlayer).and(passableLandAndNotRestricted);
''',
    '''    final Predicate<Territory> conquerable =
        CombatDomainParticipants.territoryIsEmptyOfGroundCombatUnits(gamePlayer, data)
            .and(passableLandAndNotRestricted);
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/BattleTracker.java",
    '''    if (conquerable.test(route.getEnd())) {
      IBattle precede = getDependentAmphibiousAssault(route);
      if (precede == null) {
        precede = getPendingBombingBattle(route.getEnd());
      }
      // if we have a preceding battle, then we must use a non-fighting-battle
      // if we have scrambling on, and this is an amphibious attack,
      // we may wish to scramble to kill the transports, so must use non-fighting-battle also
      if (precede != null
          || (scramblingEnabled && route.isSeaUnload() && route.hasExactlyOneStep())) {
        IBattle nonFight = getPendingBattle(route.getEnd(), BattleType.NORMAL);
        if (nonFight == null) {
          nonFight = new NonFightingBattle(route.getEnd(), gamePlayer, this, data);
          pendingBattles.add(nonFight);
          getBattleRecords()
              .addBattle(
                  gamePlayer, nonFight.getBattleId(), route.getEnd(), nonFight.getBattleType());
        }
        final Change change = nonFight.addAttackChange(route, units, null);
        addChange(bridge, changeTracker, change);
        if (precede != null) {
          addDependency(nonFight, precede);
        }
      } else {
''',
    '''    if (conquerable.test(route.getEnd())) {
      IBattle precede = getDependentAmphibiousAssault(route);
      if (precede == null) {
        precede = getPendingBombingBattle(route.getEnd());
      }
      final IBattle airBattle =
          CombatDomainParticipants.separatesAirAndGround(data)
              ? getPendingBattle(route.getEnd(), BattleType.AIR_BATTLE)
              : null;
      // if we have a preceding battle, then we must use a non-fighting-battle
      // if we have scrambling on, and this is an amphibious attack,
      // we may wish to scramble to kill the transports, so must use non-fighting-battle also
      if (precede != null
          || airBattle != null
          || (scramblingEnabled && route.isSeaUnload() && route.hasExactlyOneStep())) {
        IBattle nonFight = getPendingBattle(route.getEnd(), BattleType.NORMAL);
        if (nonFight == null) {
          nonFight = new NonFightingBattle(route.getEnd(), gamePlayer, this, data);
          pendingBattles.add(nonFight);
          getBattleRecords()
              .addBattle(
                  gamePlayer, nonFight.getBattleId(), route.getEnd(), nonFight.getBattleType());
        }
        final Change change = nonFight.addAttackChange(route, units, null);
        addChange(bridge, changeTracker, change);
        if (precede != null) {
          addDependency(nonFight, precede);
        }
        if (airBattle != null && airBattle != precede) {
          addDependency(nonFight, airBattle);
        }
      } else {
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/BattleTracker.java",
    '''    // this will be taken care of by the non fighting battle
    if (!Matches.territoryHasEnemyUnits(gamePlayer).test(site)) {
      return ChangeFactory.EMPTY_CHANGE;
    }
''',
    '''    // this will be taken care of by the non fighting battle
    if (CombatDomainParticipants.separatesAirAndGround(data)
        && !CombatDomainParticipants.hasGroundCombatDefenders(site, gamePlayer, data)) {
      return ChangeFactory.EMPTY_CHANGE;
    }
    if (!Matches.territoryHasEnemyUnits(gamePlayer).test(site)) {
      return ChangeFactory.EMPTY_CHANGE;
    }
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/MustFightBattle.java",
    '''    super(battleSite, attacker, battleTracker, data);
    defendingUnits.addAll(this.battleSite.getMatches(Matches.enemyUnit(attacker)));
    maxRounds = BattleRoundResolver.resolveGroundBattleRounds(battleSite, territoryEffects, data);
''',
    '''    super(battleSite, attacker, battleTracker, data);
    defendingUnits.addAll(
        CombatDomainParticipants.groundBattleDefenders(this.battleSite, attacker, data));
    maxRounds = BattleRoundResolver.resolveGroundBattleRounds(battleSite, territoryEffects, data);
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/MustFightBattle.java",
    '''  void resetDefendingUnits(final GamePlayer attacker) {
    defendingUnits.clear();
    defendingUnits.addAll(battleSite.getMatches(Matches.enemyUnit(attacker)));
  }
''',
    '''  void resetDefendingUnits(final GamePlayer attacker) {
    defendingUnits.clear();
    defendingUnits.addAll(
        CombatDomainParticipants.groundBattleDefenders(battleSite, attacker, gameData));
  }
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/MustFightBattle.java",
    '''    defendingUnits = new ArrayList<>(defending);
    attackingUnits = new ArrayList<>(attacking);
''',
    '''    defendingUnits =
        new ArrayList<>(
            CombatDomainParticipants.separatesAirAndGround(gameData)
                ? defending.stream().filter(Matches.unitIsNotAir()).toList()
                : defending);
    attackingUnits =
        new ArrayList<>(
            CombatDomainParticipants.separatesAirAndGround(gameData)
                ? attacking.stream().filter(Matches.unitIsNotAir()).toList()
                : attacking);
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/MustFightBattle.java",
    '''    // Filter out allied units if WW2V2
    final Predicate<Unit> ownedBy = Matches.unitIsOwnedBy(attacker);
    final Collection<Unit> attackingUnits =
        Properties.getWW2V2(gameData.getProperties())
            ? CollectionUtils.getMatches(units, ownedBy)
            : units;
''',
    '''    final Collection<Unit> domainUnits =
        CombatDomainParticipants.groundBattleAttackers(units, gameData);
    // Filter out allied units if WW2V2
    final Predicate<Unit> ownedBy = Matches.unitIsOwnedBy(attacker);
    final Collection<Unit> attackingUnits =
        Properties.getWW2V2(gameData.getProperties())
            ? CollectionUtils.getMatches(domainUnits, ownedBy)
            : domainUnits;
''',
)

replace(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/AirBattle.java",
    '''    // record who was in this battle first, so that they do not take part in any ground battles
    if (isBombingRun) {
      recordUnitsWereInAirBattle(attackingUnits, bridge);
      recordUnitsWereInAirBattle(defendingUnits, bridge);
    }
''',
    '''    // record who was in this battle first, so that they do not take part in any ground battles
    if (isBombingRun
        || Properties.getSeparateAirAndGroundCombat(gameData.getProperties())) {
      recordUnitsWereInAirBattle(attackingUnits, bridge);
      recordUnitsWereInAirBattle(defendingUnits, bridge);
    }
''',
)

write(
    "game-app/game-core/src/test/java/games/strategy/triplea/delegate/battle/CombatDomainParticipantsTest.java",
    '''package games.strategy.triplea.delegate.battle;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.GameState;
import games.strategy.engine.data.Territory;
import games.strategy.engine.data.Unit;
import games.strategy.engine.data.properties.GameProperties;
import games.strategy.triplea.Constants;
import games.strategy.triplea.attachments.UnitAttachment;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class CombatDomainParticipantsTest {
  private final GameState data = mock(GameState.class);
  private final GameProperties properties = mock(GameProperties.class);
  private final GamePlayer attacker = mock(GamePlayer.class);
  private final GamePlayer defender = mock(GamePlayer.class);

  @BeforeEach
  void setUp() {
    when(data.getProperties()).thenReturn(properties);
    when(attacker.isAtWar(defender)).thenReturn(true);
  }

  @Test
  void legacyRuleKeepsAircraftInTheNormalBattle() {
    setSeparated(false);
    final Unit fighter = unit(defender, true, true, false);
    final Unit infantry = unit(defender, false, false, false);

    assertThat(CombatDomainParticipants.groundBattleAttackers(List.of(fighter, infantry), data))
        .containsExactly(fighter, infantry);
    assertThat(
            CombatDomainParticipants.groundBattleDefenders(
                List.of(fighter, infantry), attacker, data))
        .containsExactly(fighter, infantry);
  }

  @Test
  void separatedRuleSplitsAirAndGroundAttackers() {
    setSeparated(true);
    final Unit fighter = unit(attacker, true, true, false);
    final Unit transportAircraft = unit(attacker, true, false, false);
    final Unit infantry = unit(attacker, false, false, false);

    assertThat(
            CombatDomainParticipants.airBattleAttackers(
                List.of(fighter, transportAircraft, infantry)))
        .containsExactly(fighter);
    assertThat(
            CombatDomainParticipants.groundBattleAttackers(
                List.of(fighter, transportAircraft, infantry), data))
        .containsExactly(infantry);
  }

  @Test
  void separatedRuleRemovesEnemyAircraftFromGroundDefense() {
    setSeparated(true);
    final Unit fighter = unit(defender, true, true, false);
    final Unit infantry = unit(defender, false, false, false);

    assertThat(
            CombatDomainParticipants.groundBattleDefenders(
                List.of(fighter, infantry), attacker, data))
        .containsExactly(infantry);
  }

  @Test
  void infrastructureAloneDoesNotCreateGroundCombat() {
    setSeparated(true);
    final Territory territory = mock(Territory.class);
    final Unit fighter = unit(defender, true, true, false);
    final Unit factory = unit(defender, false, false, true);
    when(territory.getUnits()).thenReturn(List.of(fighter, factory));

    assertThat(
            CombatDomainParticipants.hasGroundCombatDefenders(territory, attacker, data))
        .isFalse();
    assertThat(
            CombatDomainParticipants.territoryIsEmptyOfGroundCombatUnits(attacker, data)
                .test(territory))
        .isTrue();
  }

  @Test
  void nonAirCombatUnitPreventsNonFightingGroundCapture() {
    setSeparated(true);
    final Territory territory = mock(Territory.class);
    final Unit infantry = unit(defender, false, false, false);
    when(territory.getUnits()).thenReturn(List.of(infantry));

    assertThat(
            CombatDomainParticipants.territoryIsEmptyOfGroundCombatUnits(attacker, data)
                .test(territory))
        .isFalse();
  }

  private void setSeparated(final boolean value) {
    when(properties.get(Constants.SEPARATE_AIR_AND_GROUND_COMBAT, false)).thenReturn(value);
  }

  private static Unit unit(
      final GamePlayer owner,
      final boolean air,
      final boolean canAirBattle,
      final boolean infrastructure) {
    final Unit unit = mock(Unit.class);
    final UnitAttachment attachment = mock(UnitAttachment.class);
    when(unit.getOwner()).thenReturn(owner);
    when(unit.getUnitAttachment()).thenReturn(attachment);
    when(attachment.isAir()).thenReturn(air);
    when(attachment.canAirBattle()).thenReturn(canAirBattle);
    when(attachment.isInfrastructure()).thenReturn(infrastructure);
    return unit;
  }
}
''',
)

replace(
    "docs/development/small-front-roadmap.md",
    '''## 9. Separate air and ground combat

- distinct air-battle and ground-battle scheduling
- dependency ordering: air battle before ground battle
- aircraft cannot capture ground territory
- aircraft withdrawal and destruction rules
- separate air and ground round limits

Exit condition: air units resolve combat independently and never change ground ownership directly.
''',
    '''## 9. Separate air and ground combat

Status: in progress in PR #11.

- optional `Separate Air And Ground Combat` game property with legacy fallback
- air-capable attackers assigned to `AIR_BATTLE`
- all aircraft excluded from the dependent normal battle
- enemy aircraft ignored when determining whether ground combat is required
- non-fighting ground capture waits for the air battle dependency
- surviving, grounded, and withdrawn aircraft marked as having completed air combat
- aircraft-only forces cannot create or capture a ground battle
- existing scramble, retreat, casualty, destruction, and terrain round-limit rules retained

Exit condition: air units resolve combat independently and never change ground ownership directly.
''',
)
