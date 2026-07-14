package games.strategy.triplea.delegate.battle;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import games.strategy.engine.data.GameData;
import games.strategy.engine.data.GamePlayer;
import games.strategy.engine.data.GameState;
import games.strategy.engine.data.RelationshipTracker;
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
  private final GameData playerData = mock(GameData.class);
  private final RelationshipTracker relationships = mock(RelationshipTracker.class);
  private final GamePlayer attacker = mock(GamePlayer.class);
  private final GamePlayer defender = mock(GamePlayer.class);

  @BeforeEach
  void setUp() {
    when(data.getProperties()).thenReturn(properties);
    when(attacker.getData()).thenReturn(playerData);
    when(playerData.getRelationshipTracker()).thenReturn(relationships);
    when(relationships.isAtWar(attacker, defender)).thenReturn(true);
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

    assertThat(CombatDomainParticipants.hasGroundCombatDefenders(territory, attacker, data))
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
