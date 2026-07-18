package games.strategy.engine.data;

import static org.assertj.core.api.Assertions.assertThat;

import games.strategy.engine.data.gameparser.GameParser;
import games.strategy.triplea.attachments.TerritoryEffectAttachment;
import games.strategy.triplea.attachments.UnitAttachment;
import games.strategy.triplea.attachments.UnitSupportAttachment;
import java.nio.file.Path;
import java.util.Objects;
import java.util.stream.Collectors;
import org.junit.jupiter.api.Test;

class SmallFrontMeuseScenarioTest {
  private static final Path MAP_XML =
      Path.of("src", "test", "resources", "map-xmls", "Small_Front_Meuse.xml");

  @Test
  void rulebookValuesAreEncodedInTheScenario() {
    final GameData data = GameParser.parse(MAP_XML, false).orElseThrow();
    final GamePlayer americans = data.getPlayerList().getPlayerId("Americans");
    final GamePlayer germans = data.getPlayerList().getPlayerId("Germans");
    assertThat(capacity(data, "Open")).isEqualTo(7);
    assertThat(capacity(data, "Town")).isEqualTo(6);
    assertThat(capacity(data, "Forest")).isEqualTo(5);
    assertThat(unit(data, "americanInfantry").getCombatMovement(americans)).isEqualTo(1);
    assertThat(unit(data, "americanInfantry").getRedeploymentMovement(americans)).isEqualTo(2);
    assertThat(unit(data, "infantry").getRedeploymentMovement(germans)).isEqualTo(1);
    assertThat(unit(data, "mechanized").getStackCost()).isEqualTo(1);
    assertThat(unit(data, "artillery").getAttack(germans)).isZero();
    assertThat(unit(data, "selfPropelledArtillery").getAttack(germans)).isZero();
    assertThat(unit(data, "selfPropelledArtillery").getCombatMovement(germans)).isEqualTo(2);
    assertThat(unit(data, "selfPropelledArtillery").getRedeploymentMovement(germans)).isEqualTo(3);

    final var targets =
        UnitSupportAttachment.get(data.getUnitTypeList()).stream()
            .filter(
                rule ->
                    rule.getAttachedTo() == data.getUnitTypeList().getUnitTypeOrThrow("artillery"))
            .map(UnitSupportAttachment::getUnitType)
            .filter(Objects::nonNull)
            .flatMap(java.util.Collection::stream)
            .map(UnitType::getName)
            .collect(Collectors.toSet());
    assertThat(targets)
        .contains(
            "infantry",
            "americanInfantry",
            "artillery",
            "selfPropelledArtillery",
            "armour",
            "mechanized")
        .doesNotContain("fighter");
  }

  @Test
  void americanInitialInfantryIsReducedToEighteenBattalions() {
    final GameData data = GameParser.parse(MAP_XML, false).orElseThrow();
    final long count =
        data.getMap().getTerritories().stream()
            .flatMap(t -> t.getUnitCollection().getUnits().stream())
            .filter(u -> u.getOwner().getName().equals("Americans"))
            .filter(u -> u.getType().getName().equals("americanInfantry"))
            .count();
    assertThat(count).isEqualTo(18);
  }

  private static UnitAttachment unit(final GameData data, final String name) {
    return UnitAttachment.get(data.getUnitTypeList().getUnitTypeOrThrow(name), "unitAttachment");
  }

  private static int capacity(final GameData data, final String name) {
    return TerritoryEffectAttachment.get(data.getTerritoryEffectList().get(name))
        .getStackCapacity()
        .orElseThrow();
  }
}
