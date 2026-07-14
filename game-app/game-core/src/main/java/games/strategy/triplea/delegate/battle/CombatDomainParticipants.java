package games.strategy.triplea.delegate.battle;

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

  static List<Unit> groundBattleAttackers(final Collection<Unit> units, final GameState data) {
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
        .anyMatch(unit -> !unit.getUnitAttachment().isInfrastructure());
  }

  static Predicate<Territory> territoryIsEmptyOfGroundCombatUnits(
      final GamePlayer attacker, final GameState data) {
    if (!separatesAirAndGround(data)) {
      return Matches.territoryIsEmptyOfCombatUnits(attacker);
    }
    return territory -> !hasGroundCombatDefenders(territory, attacker, data);
  }
}
