from __future__ import annotations

from pathlib import Path
import math
import random
import re
import shutil
import zipfile
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
XML = ROOT / "game-app/smoke-testing/src/test/resources/map-xmls/Small_Front_Meuse.xml"
MAP = ROOT / "maps/small_front_meuse"
W, H = 1600, 1200

CENTERS = {
    "Huy": (270, 115), "Andenne": (430, 130), "Namur": (590, 150), "Havelange": (460, 270),
    "Ciney": (650, 285), "Dinant": (760, 285), "Durbuy": (350, 350), "Marche": (535, 410),
    "Rochefort": (700, 430), "Givet": (900, 390), "Erezee": (300, 500), "La Roche": (430, 525),
    "Hotton": (530, 535), "Nassogne": (650, 560), "Wellin": (790, 520), "Beauraing": (900, 520),
    "St. Vith": (230, 680), "Vielsalm": (340, 650), "Houffalize": (460, 685), "Bastogne": (580, 720),
    "Saint-Hubert": (700, 700), "Neufchateau": (850, 740), "Bertrix": (990, 700), "Losheim Gap": (250, 865),
    "Clervaux": (430, 850), "Wiltz": (560, 850), "Martelange": (700, 870), "Libramont": (840, 870),
    "Blankenheim": (180, 1040), "Prum": (380, 1030), "Bitburg": (590, 1040), "Vianden": (690, 975),
    "Echternach": (820, 1050),
}

UNIT_BLOCK = '''    <attachment name="unitAttachment" attachTo="infantry" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="1"/><option name="combatMovement" value="1"/><option name="redeploymentMovement" value="1"/>
      <option name="attack" value="1"/><option name="defense" value="2"/><option name="isInfantry" value="true"/>
      <option name="artillerySupportable" value="true"/><option name="stackCost" value="1"/><option name="tuv" value="3"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="americanInfantry" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="1"/><option name="combatMovement" value="1"/><option name="redeploymentMovement" value="2"/>
      <option name="attack" value="1"/><option name="defense" value="2"/><option name="isInfantry" value="true"/>
      <option name="artillerySupportable" value="true"/><option name="stackCost" value="1"/><option name="tuv" value="3"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="artillery" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="1"/><option name="combatMovement" value="1"/><option name="redeploymentMovement" value="1"/>
      <option name="attack" value="0"/><option name="defense" value="2"/><option name="artillery" value="true"/>
      <option name="artillerySupportable" value="true"/><option name="stackCost" value="1"/><option name="tuv" value="4"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="selfPropelledArtillery" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="2"/><option name="combatMovement" value="2"/><option name="redeploymentMovement" value="3"/>
      <option name="attack" value="0"/><option name="defense" value="2"/><option name="artillery" value="true"/>
      <option name="artillerySupportable" value="true"/><option name="stackCost" value="1"/><option name="tuv" value="5"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="armour" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="2"/><option name="combatMovement" value="2"/><option name="redeploymentMovement" value="3"/>
      <option name="attack" value="2"/><option name="defense" value="3"/><option name="canBlitz" value="true"/>
      <option name="artillerySupportable" value="true"/><option name="stackCost" value="2"/><option name="tuv" value="6"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="mechanized" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="2"/><option name="combatMovement" value="2"/><option name="redeploymentMovement" value="3"/>
      <option name="attack" value="2"/><option name="defense" value="2"/><option name="isInfantry" value="true"/>
      <option name="artillerySupportable" value="true"/><option name="stackCost" value="1"/><option name="tuv" value="4"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="fighter" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="4"/><option name="combatMovement" value="4"/><option name="redeploymentMovement" value="4"/>
      <option name="attack" value="3"/><option name="defense" value="3"/><option name="isAir" value="true"/>
      <option name="canAirBattle" value="true"/><option name="canIntercept" value="true"/><option name="canEscort" value="true"/>
      <option name="airAttack" value="2"/><option name="airDefense" value="2"/><option name="stackCost" value="0"/><option name="tuv" value="10"/>
    </attachment>'''


def patch_xml() -> str:
    s = XML.read_text(encoding="utf-8")
    s = s.replace('version="0.1"', 'version="0.2"')
    if '<unit name="americanInfantry"/>' not in s:
        s = s.replace('    <unit name="infantry"/>\n', '    <unit name="infantry"/>\n    <unit name="americanInfantry"/>\n')
    if '<unit name="selfPropelledArtillery"/>' not in s:
        s = s.replace('    <unit name="artillery"/>\n', '    <unit name="artillery"/>\n    <unit name="selfPropelledArtillery"/>\n')
    s = re.sub(
        r'(attachTo="Open".*?<option name="stackCapacity" value=")6("/>)',
        r'\g<1>7\2', s, count=1, flags=re.S)
    s = re.sub(
        r'(attachTo="Forest".*?<option name="stackCapacity" value=")3("/>)',
        r'\g<1>5\2', s, count=1, flags=re.S)
    s = re.sub(
        r'(attachTo="Town".*?<option name="stackCapacity" value=")5("/>)',
        r'\g<1>6\2', s, count=1, flags=re.S)
    s = re.sub(
        r'    <attachment name="unitAttachment" attachTo="infantry".*?(?=\n    <attachment name="territoryAttachment")',
        UNIT_BLOCK + "\n",
        s,
        flags=re.S,
    )
    replacements = {
        '2:Prum:artillery:1': '2:Prum:selfPropelledArtillery:1',
        '4:Dinant:artillery:1': '4:Dinant:selfPropelledArtillery:1',
        ':Marche:infantry:2': ':Marche:americanInfantry:2',
        ':Namur:infantry:2': ':Namur:americanInfantry:2',
        ':Huy:infantry:2': ':Huy:americanInfantry:2',
        ':Givet:infantry:2': ':Givet:americanInfantry:2',
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    s = re.sub(r'unitType="infantry"([^>]*owner="Americans")', r'unitType="americanInfantry"\1', s)
    for territory, quantity in {"St. Vith": 2, "Houffalize": 1, "Bastogne": 2, "Marche": 1, "Namur": 1}.items():
        s = re.sub(
            rf'(unitType="americanInfantry" territory="{re.escape(territory)}" quantity=")\d+',
            rf'\g<1>{quantity}',
            s,
        )
    s = re.sub(r' *<unitPlacement unitType="americanInfantry" territory="Ciney"[^>]*/>\n?', '', s)
    XML.write_text(s, encoding="utf-8")
    ET.parse(XML)
    return s


def patch_rulebook() -> None:
    p = ROOT / "docs/small-front-meuse-rulebook.md"
    s = p.read_text(encoding="utf-8")
    s = s.replace("# Small Front: Meuse Corridor 룰북", "# Small Front: Meuse Corridor 룰북\n\n> 기본 편제 단위는 **대대(Battalion, NATO `II`)**이다.", 1)
    start = s.index("## 4. 부대 능력치")
    end = s.index("## 5. 지형")
    section = '''## 4. 부대 능력치

| 부대 | 편제 | 공격 | 방어 | 전투 이동 | 재배치 | 전선 폭 | 특수 규칙 |
|---|---|---:|---:|---:|---:|---:|---|
| infantry | 독일 보병대대 | 1 | 2 | 1 | 1 | 1 | 포병 지원 대상 |
| americanInfantry | 미군 차량화 보병대대 | 1 | 2 | 1 | **2** | 1 | 포병 지원 대상 |
| artillery | 견인포병대대 | **0** | 2 | 1 | 1 | 1 | 공격 시 지상 대대 1개 지원 |
| selfPropelledArtillery | 자주포대대 | **0** | 2 | 2 | 3 | 1 | 기계화 이동, 지상 대대 1개 지원 |
| armour | 기갑대대 | 2 | 3 | 2 | 3 | 2 | 전격, 포병 지원 대상 |
| mechanized | 기계화보병대대 | 2 | 2 | 2 | 3 | **1** | 포병 지원 대상 |
| fighter | 전투항공대 | 3 | 3 | 4 | 4 | 0 | 공중전·요격·호위 |

견인포병과 자주포는 자체 공격 명중 능력이 없다. 공격에 참가한 포병 대대 1개당 같은 전투의 지상 대대 1개에 공격력 +1을 부여한다. 보병, 기갑, 기계화, 포병 계열을 모두 지원할 수 있으며 방어에는 적용하지 않는다.

'''
    s = s[:start] + section + s[end:]
    s = s.replace("Open | 4 | 2 | **7**", "Open | 4 | 2 | **7**")
    s = s.replace("Town | 3 | 1 | **6**", "Town | 3 | 1 | **6**")
    s = s.replace("Forest | 2 | 1 | **5**", "Forest | 2 | 1 | **5**")
    s = s.replace("- infantry, artillery: 1", "- 독일 보병·견인포병: 1\n- 미군 보병: 2")
    s = s.replace("- armour, mechanized: 3", "- armour, mechanized, selfPropelledArtillery: 3")
    s = s.replace("2 | Prum | artillery 1", "2 | Prum | selfPropelledArtillery 1")
    s = s.replace("4 | Dinant | artillery 1", "4 | Dinant | selfPropelledArtillery 1")
    s = s.replace("| 2 | Marche | infantry 2 |", "| 2 | Marche | americanInfantry 2 |")
    s = s.replace("| 4 | Namur | infantry 2 |", "| 4 | Namur | americanInfantry 2 |")
    s = s.replace("| 6 | Huy | infantry 2 |", "| 6 | Huy | americanInfantry 2 |")
    s = s.replace("| 6 | Givet | infantry 2 |", "| 6 | Givet | americanInfantry 2 |")
    s = re.sub(
        r'### 12\.2 미군.*?(?=\n## 13\.)',
        """### 12.2 미군

| 지역 | 초기 부대 |
|---|---|
| St. Vith | americanInfantry 2, artillery 1 |
| Houffalize | americanInfantry 1 |
| Wiltz | americanInfantry 1 |
| Bastogne | americanInfantry 2, artillery 1 |
| Martelange, Vielsalm, La Roche, Erezee, Hotton | americanInfantry 1씩 |
| Nassogne, Libramont, Marche, Neufchateau, Saint-Hubert | americanInfantry 1씩 |
| Ciney | fighter 1 |
| Namur, Dinant | americanInfantry 1씩 |

미군 초기 보병은 24개 대대에서 18개 대대로 25% 감축한다.
""",
        s,
        flags=re.S,
    )
    s += '''\n## 15. 0.2 편제 및 지도 변경\n\n- 미군 초기 보병은 24개 대대에서 18개 대대로 25% 감축한다.\n- 미군 보병만 재배치 이동력이 2이다.\n- 기계화보병 전선 폭은 1이다.\n- 신규 자주포대대는 전투 이동 2, 재배치 3이다.\n- 지도는 녹색 전술도, 도로·하천·초기 전선, NATO 대대 표식을 사용한다.\n'''
    p.write_text(s, encoding="utf-8")


def patch_ai_test() -> None:
    p = ROOT / "game-app/smoke-testing/src/test/java/games/strategy/engine/data/SmallFrontAiGameTest.java"
    s = p.read_text(encoding="utf-8")
    s = s.replace("import java.util.Optional;\n", "")
    s = re.sub(
        r'\n    final Optional<String> overflow =.*?\.contains\("Losheim Gap"\);',
        '',
        s,
        flags=re.S,
    )
    s = s.replace(
        '.filter(unit -> unit.getType().getName().equals("infantry"))',
        '.filter(unit -> unit.getType().getName().equals("infantry")\n'
        '            || unit.getType().getName().equals("americanInfantry"))',
    )
    p.write_text(s, encoding="utf-8")


def write_test() -> None:
    p = ROOT / "game-app/smoke-testing/src/test/java/games/strategy/engine/data/SmallFrontMeuseScenarioTest.java"
    p.write_text('''package games.strategy.engine.data;

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
    assertThat(unit(data, "americanInfantry").getRedeploymentMovement(americans)).isEqualTo(2);
    assertThat(unit(data, "infantry").getRedeploymentMovement(germans)).isEqualTo(1);
    assertThat(unit(data, "mechanized").getStackCost()).isEqualTo(1);
    assertThat(unit(data, "artillery").getAttack(germans)).isZero();
    assertThat(unit(data, "selfPropelledArtillery").getAttack(germans)).isZero();
    assertThat(unit(data, "selfPropelledArtillery").getCombatMovement(germans)).isEqualTo(2);
    assertThat(unit(data, "selfPropelledArtillery").getRedeploymentMovement(germans)).isEqualTo(3);

    final var targets = UnitSupportAttachment.get(data.getUnitTypeList()).stream()
        .filter(rule -> rule.getAttachedTo() == data.getUnitTypeList().getUnitTypeOrThrow("artillery"))
        .map(UnitSupportAttachment::getUnitType)
        .filter(Objects::nonNull)
        .flatMap(java.util.Collection::stream)
        .map(UnitType::getName)
        .collect(Collectors.toSet());
    assertThat(targets).contains("infantry", "americanInfantry", "artillery",
        "selfPropelledArtillery", "armour", "mechanized").doesNotContain("fighter");
  }

  @Test
  void americanInitialInfantryIsReducedToEighteenBattalions() {
    final GameData data = GameParser.parse(MAP_XML, false).orElseThrow();
    final long count = data.getMap().getTerritories().stream()
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
        .getStackCapacity().orElseThrow();
  }
}
''', encoding="utf-8")


def regular_polygon(x: int, y: int, r: int = 50) -> list[tuple[int, int]]:
    return [(round(x + math.cos(i * math.pi / 3) * r), round(y + math.sin(i * math.pi / 3) * r)) for i in range(6)]


def write_map(xml: str) -> None:
    game = MAP / "map/games/Small_Front_Meuse.xml"
    game.parent.mkdir(parents=True, exist_ok=True)
    game.write_text(xml, encoding="utf-8")
    (MAP / "map.yml").write_text("map_name: small_front_meuse\ngames:\n- {game_name: Small Front: Meuse Corridor, file_name: Small_Front_Meuse.xml}\n", encoding="utf-8")
    (MAP / "README.md").write_text("# Small Front: Meuse Corridor\n\nTactical relief map with roads, rivers, a marked initial front, and NATO battalion counters.\n", encoding="utf-8")
    (MAP / "map/map.properties").write_text("color.Germans=7d4038\ncolor.Americans=4d617c\nunits.scale=1\nmap.showTerritoryNames=true\nmap.hasRelief=true\nmap.showCapitolMarkers=true\nmap.scrollWrapX=false\nmap.width=1600\nmap.height=1200\n", encoding="utf-8")
    (MAP / "map/centers.txt").write_text("\n".join(f"{n}  ({x},{y})" for n, (x, y) in CENTERS.items()) + "\n", encoding="utf-8")
    (MAP / "map/place.txt").write_text("\n".join(f"{n}  ({x-23},{y-23})  ({x+23},{y-23})  ({x-23},{y+23})  ({x+23},{y+23})" for n, (x, y) in CENTERS.items()) + "\n", encoding="utf-8")
    polys = {n: regular_polygon(x, y) for n, (x, y) in CENTERS.items()}
    (MAP / "map/polygons.txt").write_text("\n".join(f"{n}  <  " + " ".join(f"({x},{y})" for x, y in pts) + " >" for n, pts in polys.items()) + "\n", encoding="utf-8")

    root = ET.fromstring(re.sub(r'<!DOCTYPE.*?>', '', xml))
    connections = [(e.attrib['t1'], e.attrib['t2']) for e in root.findall('./map/connection')]
    roads = []
    for attachment in root.findall('./attachmentList/attachment'):
        if attachment.attrib.get('name') == 'supplyTerritoryAttachment':
            a = attachment.attrib['attachTo']
            roads += [(a, o.attrib['value']) for o in attachment.findall('option') if o.attrib.get('name') == 'roadConnection']

    random.seed(44)
    image = Image.new("RGB", (W, H), (65, 105, 48))
    draw = ImageDraw.Draw(image)
    for _ in range(24000):
        x, y = random.randrange(W), random.randrange(H)
        v = random.randrange(-12, 13)
        draw.point((x, y), fill=(max(30, 65+v), max(55, 105+v), max(25, 48+v)))
    for a, b in connections:
        draw.line((CENTERS[a], CENTERS[b]), fill=(145, 142, 104), width=4)
    for a, b in roads:
        draw.line((CENTERS[a], CENTERS[b]), fill=(88, 52, 38), width=7)
        draw.line((CENTERS[a], CENTERS[b]), fill=(202, 174, 107), width=3)
    rivers = [[(150,210),(420,210),(650,235),(820,300),(1050,325),(1450,300)], [(720,80),(690,300),(740,500),(790,700),(850,900),(930,1140)]]
    for river in rivers:
        draw.line(river, fill=(25, 70, 150), width=15, joint="curve")
        draw.line(river, fill=(48, 112, 205), width=8, joint="curve")
    front = [(170,600),(300,610),(420,645),(530,690),(620,785),(720,900),(820,1080)]
    draw.line(front, fill=(125, 20, 20), width=7)
    for pts in polys.values():
        draw.line(pts + [pts[0]], fill=(32, 52, 26), width=2)
    font = ImageFont.load_default()
    for n, (x, y) in CENTERS.items():
        box = draw.textbbox((0, 0), n, font=font)
        tw = box[2] - box[0]
        draw.rectangle((x-tw//2-3, y-7, x+tw//2+3, y+7), fill=(220, 209, 155))
        draw.text((x-tw//2, y-5), n, font=font, fill=(22, 25, 18))
    draw.rectangle((1120, 920, 1570, 1160), fill=(226, 215, 165), outline=(60, 55, 35), width=3)
    draw.text((1140, 940), "SMALL FRONT: MEUSE CORRIDOR", font=font, fill=(25,25,20))
    draw.text((1140, 970), "NATO BATTALION SCALE (II)", font=font, fill=(25,25,20))
    draw.line((1140,1005,1220,1005), fill=(202,174,107), width=5); draw.text((1230,999), "Supply road", font=font, fill=(25,25,20))
    draw.line((1140,1035,1220,1035), fill=(48,112,205), width=8); draw.text((1230,1029), "River", font=font, fill=(25,25,20))
    draw.line((1140,1065,1220,1065), fill=(125,20,20), width=6); draw.text((1230,1059), "Initial front", font=font, fill=(25,25,20))
    MAP.mkdir(parents=True, exist_ok=True)
    image.save(MAP / "preview.png")
    for kind, source in (("baseTiles", image), ("reliefTiles", image)):
        out = MAP / "map" / kind; out.mkdir(parents=True, exist_ok=True)
        for row, y in enumerate(range(0, H, 256)):
            for col, x in enumerate(range(0, W, 256)):
                tile = Image.new("RGB", (256,256), (60,90,40)); tile.paste(source.crop((x,y,min(x+256,W),min(y+256,H))), (0,0)); tile.save(out / f"{col}_{row}.png")
    for side, colors in {"Germans": ((238,220,189),(80,28,25)), "Americans": ((178,198,218),(27,48,72))}.items():
        out = MAP / "map/units" / side; out.mkdir(parents=True, exist_ok=True)
        for unit in ["infantry","americanInfantry","artillery","selfPropelledArtillery","armour","mechanized","fighter"]:
            icon = Image.new("RGBA", (64,64), (0,0,0,0)); d = ImageDraw.Draw(icon); fill, ink = colors
            d.text((27,0), "II", font=font, fill=ink); d.rectangle((7,15,57,54), fill=fill, outline=ink, width=3)
            if unit in {"infantry","americanInfantry","mechanized"}: d.line((10,18,54,51), fill=ink, width=3); d.line((54,18,10,51), fill=ink, width=3)
            if unit in {"armour","mechanized","selfPropelledArtillery"}: d.ellipse((18,27,46,43), outline=ink, width=3)
            if unit in {"artillery","selfPropelledArtillery"}: d.ellipse((28,29,36,37), fill=ink)
            if unit == "fighter": d.polygon([(32,19),(38,31),(52,36),(38,39),(34,51),(30,51),(26,39),(12,36),(26,31)], fill=ink)
            icon.save(out / f"{unit}.png")
    zip_path = ROOT / "maps/small_front_meuse.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for p in MAP.rglob("*"):
            if p.is_file() and p.name != "preview.png": archive.write(p, p.relative_to(MAP))


def main() -> None:
    xml = patch_xml()
    patch_rulebook()
    patch_ai_test()
    write_test()
    write_map(xml)


if __name__ == "__main__":
    main()
