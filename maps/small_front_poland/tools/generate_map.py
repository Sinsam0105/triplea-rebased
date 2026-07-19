#!/usr/bin/env python3
# Generate the Small Front: Vistula Withdrawal map package and game XML.

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 768
MARGIN = 20
TILE = 256

SITES = {
    "Danzig": (120, 55),
    "Marienwerder": (80, 145),
    "Schneidemuhl": (65, 245),
    "Frankfurt Oder": (70, 350),
    "Breslau": (80, 470),
    "Oppeln": (110, 590),
    "Teschen": (145, 710),
    "Gdynia": (300, 55),
    "Tczew": (265, 145),
    "Bydgoszcz": (285, 235),
    "Poznan": (250, 345),
    "Kalisz": (300, 450),
    "Katowice": (275, 600),
    "Krakow": (330, 710),
    "Grudziadz": (455, 130),
    "Torun": (500, 220),
    "Wloclawek": (485, 315),
    "Kutno": (525, 400),
    "Lodz": (480, 470),
    "Piotrkow": (520, 550),
    "Czestochowa": (455, 630),
    "Kielce": (545, 700),
    "Plock": (680, 290),
    "Modlin": (720, 370),
    "Warsaw": (750, 450),
    "Radom": (690, 535),
    "Deblin": (770, 585),
    "Sandomierz": (680, 650),
    "Tarnow": (620, 730),
    "Siedlce": (900, 420),
    "Lukow": (880, 500),
    "Lublin": (920, 590),
    "Zamosc": (950, 680),
    "Brest": (980, 480),
    "Lwow": (980, 730),
}

MOVEMENT_EDGES = [
    ("Breslau", "Frankfurt Oder"),
    ("Breslau", "Kalisz"),
    ("Breslau", "Oppeln"),
    ("Breslau", "Poznan"),
    ("Brest", "Lublin"),
    ("Brest", "Lukow"),
    ("Brest", "Siedlce"),
    ("Brest", "Zamosc"),
    ("Bydgoszcz", "Grudziadz"),
    ("Bydgoszcz", "Poznan"),
    ("Bydgoszcz", "Schneidemuhl"),
    ("Bydgoszcz", "Tczew"),
    ("Bydgoszcz", "Torun"),
    ("Bydgoszcz", "Wloclawek"),
    ("Czestochowa", "Katowice"),
    ("Czestochowa", "Kielce"),
    ("Czestochowa", "Krakow"),
    ("Czestochowa", "Lodz"),
    ("Czestochowa", "Piotrkow"),
    ("Danzig", "Gdynia"),
    ("Danzig", "Marienwerder"),
    ("Danzig", "Tczew"),
    ("Deblin", "Lublin"),
    ("Deblin", "Lukow"),
    ("Deblin", "Radom"),
    ("Deblin", "Sandomierz"),
    ("Deblin", "Warsaw"),
    ("Deblin", "Zamosc"),
    ("Frankfurt Oder", "Poznan"),
    ("Frankfurt Oder", "Schneidemuhl"),
    ("Gdynia", "Grudziadz"),
    ("Gdynia", "Tczew"),
    ("Grudziadz", "Tczew"),
    ("Grudziadz", "Torun"),
    ("Kalisz", "Katowice"),
    ("Kalisz", "Lodz"),
    ("Kalisz", "Poznan"),
    ("Katowice", "Krakow"),
    ("Katowice", "Oppeln"),
    ("Katowice", "Teschen"),
    ("Kielce", "Krakow"),
    ("Kielce", "Piotrkow"),
    ("Kielce", "Sandomierz"),
    ("Kielce", "Tarnow"),
    ("Krakow", "Teschen"),
    ("Kutno", "Lodz"),
    ("Kutno", "Modlin"),
    ("Kutno", "Piotrkow"),
    ("Kutno", "Plock"),
    ("Kutno", "Radom"),
    ("Kutno", "Wloclawek"),
    ("Lodz", "Piotrkow"),
    ("Lodz", "Wloclawek"),
    ("Lublin", "Lukow"),
    ("Lublin", "Zamosc"),
    ("Lukow", "Siedlce"),
    ("Lukow", "Warsaw"),
    ("Lwow", "Zamosc"),
    ("Marienwerder", "Schneidemuhl"),
    ("Marienwerder", "Tczew"),
    ("Modlin", "Plock"),
    ("Modlin", "Radom"),
    ("Modlin", "Siedlce"),
    ("Modlin", "Warsaw"),
    ("Oppeln", "Teschen"),
    ("Piotrkow", "Radom"),
    ("Piotrkow", "Sandomierz"),
    ("Plock", "Torun"),
    ("Plock", "Wloclawek"),
    ("Poznan", "Schneidemuhl"),
    ("Radom", "Sandomierz"),
    ("Radom", "Warsaw"),
    ("Sandomierz", "Tarnow"),
    ("Schneidemuhl", "Tczew"),
    ("Siedlce", "Warsaw"),
    ("Torun", "Wloclawek"),
]

ROADS = [
    ("Danzig", "Marienwerder"),
    ("Marienwerder", "Schneidemuhl"),
    ("Schneidemuhl", "Frankfurt Oder"),
    ("Frankfurt Oder", "Breslau"),
    ("Breslau", "Oppeln"),
    ("Oppeln", "Teschen"),
    ("Danzig", "Gdynia"),
    ("Marienwerder", "Tczew"),
    ("Schneidemuhl", "Bydgoszcz"),
    ("Frankfurt Oder", "Poznan"),
    ("Breslau", "Kalisz"),
    ("Oppeln", "Katowice"),
    ("Teschen", "Krakow"),
    ("Gdynia", "Tczew"),
    ("Tczew", "Bydgoszcz"),
    ("Tczew", "Grudziadz"),
    ("Bydgoszcz", "Torun"),
    ("Torun", "Wloclawek"),
    ("Wloclawek", "Plock"),
    ("Wloclawek", "Kutno"),
    ("Kutno", "Modlin"),
    ("Modlin", "Warsaw"),
    ("Warsaw", "Siedlce"),
    ("Siedlce", "Brest"),
    ("Poznan", "Kalisz"),
    ("Kalisz", "Lodz"),
    ("Lodz", "Kutno"),
    ("Poznan", "Bydgoszcz"),
    ("Lodz", "Piotrkow"),
    ("Piotrkow", "Radom"),
    ("Radom", "Warsaw"),
    ("Katowice", "Czestochowa"),
    ("Czestochowa", "Piotrkow"),
    ("Krakow", "Kielce"),
    ("Kielce", "Tarnow"),
    ("Kielce", "Sandomierz"),
    ("Sandomierz", "Radom"),
    ("Kielce", "Piotrkow"),
    ("Radom", "Deblin"),
    ("Deblin", "Warsaw"),
    ("Deblin", "Lublin"),
    ("Lublin", "Lukow"),
    ("Lukow", "Siedlce"),
    ("Lublin", "Zamosc"),
    ("Zamosc", "Lwow"),
    ("Sandomierz", "Deblin"),
    ("Brest", "Lukow"),
]

GERMAN_START = {
    "Danzig",
    "Marienwerder",
    "Schneidemuhl",
    "Frankfurt Oder",
    "Breslau",
    "Oppeln",
    "Teschen",
}
GERMAN_SOURCES = set(GERMAN_START)
POLISH_SOURCES = {"Siedlce", "Lublin", "Brest", "Lwow"}
OBJECTIVES = {
    "Gdynia",
    "Bydgoszcz",
    "Poznan",
    "Lodz",
    "Warsaw",
    "Radom",
    "Deblin",
    "Lublin",
    "Brest",
    "Lwow",
}

FOREST = {
    "Schneidemuhl",
    "Bydgoszcz",
    "Grudziadz",
    "Czestochowa",
    "Kielce",
    "Sandomierz",
    "Zamosc",
}
TOWNS = {
    "Danzig",
    "Gdynia",
    "Poznan",
    "Lodz",
    "Krakow",
    "Modlin",
    "Warsaw",
    "Radom",
    "Deblin",
    "Lublin",
    "Brest",
    "Lwow",
}

UNITS = [
    ("Danzig", [("infantry", 2, "Germans"), ("mechanized", 1, "Germans")]),
    ("Marienwerder", [("infantry", 2, "Germans"), ("armour", 1, "Germans")]),
    ("Schneidemuhl", [("infantry", 2, "Germans"), ("armour", 1, "Germans")]),
    ("Frankfurt Oder", [("infantry", 2, "Germans"), ("armour", 2, "Germans")]),
    (
        "Breslau",
        [
            ("infantry", 2, "Germans"),
            ("armour", 1, "Germans"),
            ("selfPropelledArtillery", 1, "Germans"),
        ],
    ),
    ("Oppeln", [("infantry", 2, "Germans"), ("mechanized", 1, "Germans")]),
    ("Teschen", [("infantry", 2, "Germans"), ("armour", 1, "Germans")]),
    ("Gdynia", [("polishInfantry", 2, "Poland"), ("polishArtillery", 1, "Poland")]),
    ("Tczew", [("polishInfantry", 1, "Poland")]),
    ("Bydgoszcz", [("polishInfantry", 2, "Poland"), ("polishArtillery", 1, "Poland")]),
    ("Poznan", [("polishInfantry", 2, "Poland"), ("cavalry", 1, "Poland")]),
    ("Kalisz", [("polishInfantry", 1, "Poland")]),
    ("Katowice", [("polishInfantry", 2, "Poland"), ("polishArtillery", 1, "Poland")]),
    ("Krakow", [("polishInfantry", 2, "Poland"), ("cavalry", 1, "Poland")]),
    ("Grudziadz", [("polishInfantry", 1, "Poland")]),
    ("Torun", [("polishInfantry", 1, "Poland")]),
    ("Wloclawek", [("polishInfantry", 1, "Poland")]),
    ("Kutno", [("polishInfantry", 2, "Poland")]),
    ("Lodz", [("polishInfantry", 2, "Poland"), ("polishArtillery", 1, "Poland")]),
    ("Piotrkow", [("polishInfantry", 1, "Poland")]),
    ("Czestochowa", [("polishInfantry", 1, "Poland")]),
    ("Kielce", [("polishInfantry", 1, "Poland")]),
    ("Plock", [("polishInfantry", 1, "Poland")]),
    ("Modlin", [("polishInfantry", 2, "Poland"), ("polishArtillery", 1, "Poland")]),
    ("Warsaw", [("polishInfantry", 3, "Poland"), ("polishArtillery", 1, "Poland")]),
    ("Radom", [("polishInfantry", 1, "Poland")]),
    ("Deblin", [("polishInfantry", 1, "Poland")]),
    ("Sandomierz", [("polishInfantry", 1, "Poland")]),
    ("Tarnow", [("polishInfantry", 1, "Poland")]),
    ("Siedlce", [("polishInfantry", 1, "Poland")]),
    ("Lublin", [("polishInfantry", 1, "Poland")]),
]


def clip_half_plane(
    polygon: list[tuple[float, float]],
    nx: float,
    ny: float,
    limit: float,
) -> list[tuple[float, float]]:
    # Keep points satisfying nx*x + ny*y <= limit.
    if not polygon:
        return []
    result: list[tuple[float, float]] = []
    previous = polygon[-1]
    previous_value = nx * previous[0] + ny * previous[1] - limit
    previous_inside = previous_value <= 1e-7
    for current in polygon:
        current_value = nx * current[0] + ny * current[1] - limit
        current_inside = current_value <= 1e-7
        if current_inside != previous_inside:
            denominator = previous_value - current_value
            t = 0.0 if abs(denominator) < 1e-12 else previous_value / denominator
            result.append(
                (
                    previous[0] + t * (current[0] - previous[0]),
                    previous[1] + t * (current[1] - previous[1]),
                )
            )
        if current_inside:
            result.append(current)
        previous = current
        previous_value = current_value
        previous_inside = current_inside
    return result


def voronoi_cells() -> dict[str, list[tuple[int, int]]]:
    cells: dict[str, list[tuple[int, int]]] = {}
    bounding = [
        (MARGIN, MARGIN),
        (WIDTH - MARGIN, MARGIN),
        (WIDTH - MARGIN, HEIGHT - MARGIN),
        (MARGIN, HEIGHT - MARGIN),
    ]
    for name, (x, y) in SITES.items():
        polygon = [(float(px), float(py)) for px, py in bounding]
        for other, (ox, oy) in SITES.items():
            if other == name:
                continue
            nx = 2.0 * (ox - x)
            ny = 2.0 * (oy - y)
            limit = float(ox * ox + oy * oy - x * x - y * y)
            polygon = clip_half_plane(polygon, nx, ny, limit)
        cells[name] = [(round(px), round(py)) for px, py in polygon]
    return cells


def terrain(name: str) -> str:
    if name in FOREST:
        return "Forest"
    if name in TOWNS:
        return "Town"
    return "Open"


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def label_position(name: str, draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont) -> tuple[int, int]:
    x, y = SITES[name]
    box = draw.textbbox((0, 0), name, font=font)
    width = box[2] - box[0]
    return max(2, x - width // 2), max(2, y - 7)


def draw_map(cells: dict[str, list[tuple[int, int]]]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#efe9d7")
    draw = ImageDraw.Draw(image)
    terrain_colors = {"Open": "#e3d3ad", "Forest": "#b7c39d", "Town": "#d7c2af"}

    for name, polygon in cells.items():
        draw.polygon(polygon, fill=terrain_colors[terrain(name)])

    for first, second in ROADS:
        draw.line([SITES[first], SITES[second]], fill="#9c7b4e", width=4)
        draw.line([SITES[first], SITES[second]], fill="#d9c89e", width=2)

    vistula = [
        (640, 220),
        SITES["Plock"],
        SITES["Modlin"],
        SITES["Warsaw"],
        SITES["Deblin"],
        SITES["Sandomierz"],
        (720, HEIGHT),
    ]
    draw.line(vistula, fill="#6d9fc3", width=9)
    draw.line(vistula, fill="#b9d6e8", width=4)

    for polygon in cells.values():
        draw.line(polygon + [polygon[0]], fill="#343434", width=2)

    draw.rectangle((MARGIN, MARGIN, 190, HEIGHT - MARGIN), outline="#555555", width=3)

    city_font = load_font(12)
    small_font = load_font(10)
    for name, (x, y) in SITES.items():
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="#202020")
        font = small_font if len(name) > 12 else city_font
        tx, ty = label_position(name, draw, font)
        draw.rectangle(draw.textbbox((tx, ty), name, font=font), fill="#f4efdf")
        draw.text((tx, ty), name, fill="#202020", font=font)

    return image


def save_tiles(image: Image.Image, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for x_index in range(math.ceil(WIDTH / TILE)):
        for y_index in range(math.ceil(HEIGHT / TILE)):
            tile = image.crop(
                (
                    x_index * TILE,
                    y_index * TILE,
                    min((x_index + 1) * TILE, WIDTH),
                    min((y_index + 1) * TILE, HEIGHT),
                )
            )
            if tile.size != (TILE, TILE):
                padded = Image.new("RGB", (TILE, TILE), "#efe9d7")
                padded.paste(tile, (0, 0))
                tile = padded
            tile.save(directory / f"{x_index}_{y_index}.png", optimize=True)


def draw_counter(path: Path, color: str, symbol: str) -> None:
    size = 40
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((3, 8, 36, 32), fill=color, outline="#111111", width=2)
    ink = "#f8f5eb"
    if symbol == "infantry":
        draw.line((8, 12, 31, 29), fill=ink, width=3)
        draw.line((31, 12, 8, 29), fill=ink, width=3)
    elif symbol == "artillery":
        draw.ellipse((17, 18, 22, 23), fill=ink)
    elif symbol == "cavalry":
        draw.line((10, 29, 30, 12), fill=ink, width=3)
    elif symbol == "armour":
        draw.ellipse((9, 13, 30, 28), outline=ink, width=3)
    elif symbol == "mechanized":
        draw.line((8, 12, 31, 29), fill=ink, width=2)
        draw.line((31, 12, 8, 29), fill=ink, width=2)
        draw.ellipse((10, 15, 29, 27), outline=ink, width=2)
    elif symbol == "selfPropelledArtillery":
        draw.ellipse((17, 16, 22, 21), fill=ink)
        draw.ellipse((10, 22, 29, 29), outline=ink, width=2)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def game_xml() -> str:
    names = sorted(SITES)
    movement_edges = sorted(tuple(sorted(edge)) for edge in MOVEMENT_EDGES)
    road_edges = {tuple(sorted(edge)) for edge in ROADS}
    assert len(movement_edges) == 76
    assert len(road_edges) == 47
    assert road_edges <= set(movement_edges)

    roads_by_source: dict[str, list[str]] = {}
    for first, second in ROADS:
        roads_by_source.setdefault(first, []).append(second)

    lines: list[str] = []
    add = lines.append
    add('<?xml version="1.0" encoding="UTF-8"?>')
    add('<!DOCTYPE game SYSTEM "game.dtd">')
    add('<game>')
    add('  <info name="Small Front: Vistula Withdrawal" version="0.1"/>')
    add('  <loader javaClass="games.strategy.triplea.TripleA"/>')
    add('  <triplea minimumVersion="2.7.0"/>')
    add('  <diceSides value="6"/>')
    add('')
    add('  <map>')
    for name in names:
        add(f'    <territory name="{name}"/>')
    for first, second in movement_edges:
        add(f'    <connection t1="{first}" t2="{second}"/>')
    add('  </map>')
    add('')
    add('  <resourceList>')
    add('    <resource name="PUs"/>')
    add('  </resourceList>')
    add('')
    add('  <playerList>')
    add('    <player name="Germans" optional="false" defaultType="Human"/>')
    add('    <player name="Poland" optional="false" defaultType="Human"/>')
    add('    <alliance player="Germans" alliance="Axis"/>')
    add('    <alliance player="Poland" alliance="Allies"/>')
    add('  </playerList>')
    add('')
    add('  <unitList>')
    for unit_type in [
        "infantry",
        "polishInfantry",
        "polishArtillery",
        "cavalry",
        "armour",
        "mechanized",
        "selfPropelledArtillery",
    ]:
        add(f'    <unit name="{unit_type}"/>')
    add('  </unitList>')
    add('')
    add('  <relationshipTypes>')
    add('    <relationshipType name="War"/>')
    add('    <relationshipType name="Allied"/>')
    add('  </relationshipTypes>')
    add('')
    add('  <territoryEffectList>')
    for effect in ["Open", "Forest", "Town"]:
        add(f'    <territoryEffect name="{effect}"/>')
    add('  </territoryEffectList>')
    add('')
    add(GAMEPLAY.rstrip())
    add('  <attachmentList>')
    add(STATIC_ATTACHMENTS.rstrip())

    for name in names:
        add(
            f'    <attachment name="territoryAttachment" attachTo="{name}" '
            'javaClass="games.strategy.triplea.attachments.TerritoryAttachment" type="territory">'
        )
        add('      <option name="production" value="0"/>')
        add(f'      <option name="victoryCity" value="{1 if name in OBJECTIVES else 0}"/>')
        if name == "Frankfurt Oder":
            add('      <option name="capital" value="Germans"/>')
        if name == "Brest":
            add('      <option name="capital" value="Poland"/>')
        add(f'      <option name="territoryEffect" value="{terrain(name)}"/>')
        add('    </attachment>')

        source = name in GERMAN_SOURCES or name in POLISH_SOURCES
        road_targets = roads_by_source.get(name, [])
        if source or road_targets:
            add(
                f'    <attachment name="supplyTerritoryAttachment" attachTo="{name}" '
                'javaClass="games.strategy.triplea.attachments.SupplyTerritoryAttachment" type="territory">'
            )
            if source:
                add('      <option name="supplySource" value="true"/>')
            for target in road_targets:
                add(f'      <option name="roadConnection" value="{target}"/>')
            add('    </attachment>')

    add(REINFORCEMENTS_AND_SCORING.rstrip())
    add('  </attachmentList>')
    add('')
    add('  <initialize>')
    add('    <ownerInitialize>')
    for name in names:
        owner = "Germans" if name in GERMAN_START else "Poland"
        add(f'      <territoryOwner territory="{name}" owner="{owner}"/>')
    add('    </ownerInitialize>')
    add('    <unitInitialize>')
    for territory, groups in UNITS:
        for unit_type, quantity, owner in groups:
            add(
                f'      <unitPlacement unitType="{unit_type}" territory="{territory}" '
                f'quantity="{quantity}" owner="{owner}"/>'
            )
    add('    </unitInitialize>')
    add('    <relationshipInitialize>')
    add('      <relationship player1="Germans" player2="Poland" type="War" roundValue="0"/>')
    add('    </relationshipInitialize>')
    add('  </initialize>')
    add('')
    add(PROPERTIES.rstrip())
    add('</game>')
    return "\n".join(lines) + "\n"


GAMEPLAY = '''  <gamePlay>
    <delegate name="initialization" javaClass="games.strategy.triplea.delegate.InitializationDelegate" display="Initialize"/>
    <delegate name="reinforcement" javaClass="games.strategy.triplea.delegate.FixedReinforcementDelegate" display="Fixed Reinforcements"/>
    <delegate name="supply" javaClass="games.strategy.triplea.delegate.SupplyDelegate" display="Supply"/>
    <delegate name="move" javaClass="games.strategy.triplea.delegate.SupplyAwareMoveDelegate" display="Move"/>
    <delegate name="battle" javaClass="games.strategy.triplea.delegate.BattleDelegate" display="Battle"/>
    <delegate name="endTurn" javaClass="games.strategy.triplea.delegate.NoPUEndTurnDelegate" display="End Turn"/>
    <delegate name="endRound" javaClass="games.strategy.triplea.delegate.SmallFrontEndRoundDelegate" display="End Round"/>

    <sequence>
      <step name="initializationStep" delegate="initialization" maxRunCount="1"/>

      <step name="germanReinforcement" delegate="reinforcement" player="Germans"/>
      <step name="germanSupply" delegate="supply" player="Germans"/>
      <step name="germanCombatMove" delegate="move" player="Germans" display="Combat Move"/>
      <step name="germanBattle" delegate="battle" player="Germans"/>
      <step name="germanRedeployment" delegate="move" player="Germans" display="Redeployment">
        <stepProperty name="nonCombatMove" value="true"/>
        <stepProperty name="removeAirThatCanNotLand" value="false"/>
      </step>
      <step name="germanEndTurn" delegate="endTurn" player="Germans"/>

      <step name="polishReinforcement" delegate="reinforcement" player="Poland"/>
      <step name="polishSupply" delegate="supply" player="Poland"/>
      <step name="polishCombatMove" delegate="move" player="Poland" display="Combat Move"/>
      <step name="polishBattle" delegate="battle" player="Poland"/>
      <step name="polishRedeployment" delegate="move" player="Poland" display="Redeployment">
        <stepProperty name="nonCombatMove" value="true"/>
        <stepProperty name="removeAirThatCanNotLand" value="false"/>
      </step>
      <step name="polishEndTurn" delegate="endTurn" player="Poland"/>

      <step name="endRoundStep" delegate="endRound"/>
    </sequence>
  </gamePlay>
'''

STATIC_ATTACHMENTS = '''    <attachment name="relationshipTypeAttachment" attachTo="War" javaClass="games.strategy.triplea.attachments.RelationshipTypeAttachment" type="relationship">
      <option name="archeType" value="war"/>
    </attachment>
    <attachment name="relationshipTypeAttachment" attachTo="Allied" javaClass="games.strategy.triplea.attachments.RelationshipTypeAttachment" type="relationship">
      <option name="archeType" value="allied"/>
    </attachment>

    <attachment name="territoryEffectAttachment" attachTo="Open" javaClass="games.strategy.triplea.attachments.TerritoryEffectAttachment" type="territoryEffect">
      <option name="maxGroundBattleRounds" value="4"/>
      <option name="maxAirBattleRounds" value="1"/>
      <option name="stackCapacity" value="7"/>
    </attachment>
    <attachment name="territoryEffectAttachment" attachTo="Forest" javaClass="games.strategy.triplea.attachments.TerritoryEffectAttachment" type="territoryEffect">
      <option name="maxGroundBattleRounds" value="2"/>
      <option name="maxAirBattleRounds" value="1"/>
      <option name="stackCapacity" value="5"/>
    </attachment>
    <attachment name="territoryEffectAttachment" attachTo="Town" javaClass="games.strategy.triplea.attachments.TerritoryEffectAttachment" type="territoryEffect">
      <option name="maxGroundBattleRounds" value="3"/>
      <option name="maxAirBattleRounds" value="1"/>
      <option name="stackCapacity" value="6"/>
    </attachment>

    <attachment name="unitAttachment" attachTo="infantry" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="1"/>
      <option name="combatMovement" value="1"/>
      <option name="redeploymentMovement" value="1"/>
      <option name="attack" value="1"/>
      <option name="defense" value="2"/>
      <option name="isInfantry" value="true"/>
      <option name="artillerySupportable" value="true"/>
      <option name="stackCost" value="1"/>
      <option name="tuv" value="3"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="polishInfantry" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="1"/>
      <option name="combatMovement" value="1"/>
      <option name="redeploymentMovement" value="3"/>
      <option name="attack" value="1"/>
      <option name="defense" value="2"/>
      <option name="isInfantry" value="true"/>
      <option name="artillerySupportable" value="true"/>
      <option name="stackCost" value="1"/>
      <option name="tuv" value="3"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="polishArtillery" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="1"/>
      <option name="combatMovement" value="1"/>
      <option name="redeploymentMovement" value="2"/>
      <option name="attack" value="2"/>
      <option name="defense" value="2"/>
      <option name="artillery" value="true"/>
      <option name="stackCost" value="1"/>
      <option name="tuv" value="4"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="cavalry" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="2"/>
      <option name="combatMovement" value="2"/>
      <option name="redeploymentMovement" value="4"/>
      <option name="attack" value="1"/>
      <option name="defense" value="2"/>
      <option name="isInfantry" value="true"/>
      <option name="artillerySupportable" value="true"/>
      <option name="stackCost" value="1"/>
      <option name="tuv" value="4"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="armour" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="2"/>
      <option name="combatMovement" value="2"/>
      <option name="redeploymentMovement" value="3"/>
      <option name="attack" value="3"/>
      <option name="defense" value="3"/>
      <option name="canBlitz" value="true"/>
      <option name="artillerySupportable" value="true"/>
      <option name="stackCost" value="2"/>
      <option name="tuv" value="7"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="mechanized" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="2"/>
      <option name="combatMovement" value="2"/>
      <option name="redeploymentMovement" value="3"/>
      <option name="attack" value="2"/>
      <option name="defense" value="2"/>
      <option name="isInfantry" value="true"/>
      <option name="artillerySupportable" value="true"/>
      <option name="stackCost" value="1"/>
      <option name="tuv" value="5"/>
    </attachment>
    <attachment name="unitAttachment" attachTo="selfPropelledArtillery" javaClass="games.strategy.triplea.attachments.UnitAttachment" type="unitType">
      <option name="movement" value="2"/>
      <option name="combatMovement" value="2"/>
      <option name="redeploymentMovement" value="3"/>
      <option name="attack" value="2"/>
      <option name="defense" value="2"/>
      <option name="artillery" value="true"/>
      <option name="stackCost" value="1"/>
      <option name="tuv" value="5"/>
    </attachment>
'''

REINFORCEMENTS_AND_SCORING = '''
    <attachment name="fixedReinforcementAttachment" attachTo="Germans" javaClass="games.strategy.triplea.attachments.FixedReinforcementAttachment" type="player">
      <option name="reinforcement" value="1:Frankfurt Oder:armour:1"/>
      <option name="reinforcement" value="1:Oppeln:mechanized:1"/>
      <option name="reinforcement" value="2:Danzig:armour:1"/>
      <option name="reinforcement" value="2:Breslau:selfPropelledArtillery:1"/>
      <option name="reinforcement" value="3:Schneidemuhl:infantry:2"/>
      <option name="reinforcement" value="3:Teschen:armour:1"/>
      <option name="reinforcement" value="4:Frankfurt Oder:mechanized:1"/>
      <option name="reinforcement" value="4:Danzig:infantry:2"/>
      <option name="reinforcement" value="5:Breslau:armour:1"/>
    </attachment>
    <attachment name="fixedReinforcementAttachment" attachTo="Poland" javaClass="games.strategy.triplea.attachments.FixedReinforcementAttachment" type="player">
      <option name="reinforcement" value="2:Warsaw:polishInfantry:1"/>
      <option name="reinforcement" value="2:Lublin:cavalry:1"/>
      <option name="reinforcement" value="3:Siedlce:polishInfantry:2"/>
      <option name="reinforcement" value="4:Lublin:polishArtillery:1"/>
      <option name="reinforcement" value="5:Brest:polishInfantry:2"/>
      <option name="reinforcement" value="6:Lwow:cavalry:1"/>
    </attachment>

    <attachment name="scoringAttachment" attachTo="Germans" javaClass="games.strategy.triplea.attachments.SmallFrontScoringAttachment" type="player">
      <option name="pointsPerObjective" value="1"/>
      <option name="suppliedOccupationBonus" value="2:Warsaw:Deblin"/>
      <option name="suppliedOccupationBonus" value="2:Siedlce:Lublin:Brest"/>
      <option name="suppliedOccupationBonus" value="1:Kutno:Lodz:Radom"/>
    </attachment>
    <attachment name="scoringAttachment" attachTo="Poland" javaClass="games.strategy.triplea.attachments.SmallFrontScoringAttachment" type="player">
      <option name="pointsPerObjective" value="1"/>
      <option name="enemyAbsentBonus" value="2:Warsaw:Deblin"/>
      <option name="enemyAbsentBonus" value="1:Siedlce:Lublin:Brest:Lwow"/>
      <option name="winsTies" value="true"/>
    </attachment>
'''

PROPERTIES = '''  <propertyList>
    <property name="Supply Network Enabled" value="true" editable="false"/>
    <property name="Out Of Supply Removal Turns" value="2" editable="false"/>
    <property name="Fog Of War Enabled" value="true" editable="false"/>
    <property name="Fog Of War Vision Radius" value="1" editable="false"/>
    <property name="Auto Termination" value="true" editable="true"/>
    <property name="Scoring Round" value="7" editable="false"/>
    <property name="Land Battle Rounds" value="3" editable="false"/>
    <property name="Air Battle Rounds" value="1" editable="false"/>
    <property name="Sea Battle Rounds" value="3" editable="false"/>
  </propertyList>'''

DTD = '''<!ELEMENT game (info, loader?, triplea?, diceSides?, map, resourceList?, playerList, unitList?, relationshipTypes?, territoryEffectList?, gamePlay, production?, technology?, attachmentList?, initialize?, propertyList?)>
<!ELEMENT info EMPTY>
<!ATTLIST info name CDATA #REQUIRED version CDATA #IMPLIED>
<!ELEMENT loader EMPTY>
<!ATTLIST loader javaClass CDATA #REQUIRED>
<!ELEMENT triplea EMPTY>
<!ATTLIST triplea minimumVersion CDATA #REQUIRED>
<!ELEMENT diceSides EMPTY>
<!ATTLIST diceSides value CDATA #REQUIRED>

<!ELEMENT map (territory+, connection*)>
<!ELEMENT territory EMPTY>
<!ATTLIST territory name CDATA #REQUIRED water (true|false) "false">
<!ELEMENT connection EMPTY>
<!ATTLIST connection t1 CDATA #REQUIRED t2 CDATA #REQUIRED>

<!ELEMENT resourceList (resource+)>
<!ELEMENT resource EMPTY>
<!ATTLIST resource name ID #REQUIRED isDisplayedFor CDATA #IMPLIED>

<!ELEMENT playerList (player+, alliance*)>
<!ELEMENT player EMPTY>
<!ATTLIST player name ID #REQUIRED optional (true|false) "false" canBeDisabled (true|false) "false" defaultType (Human|AI|DoesNothing) "Human" isHidden (true|false) "false">
<!ELEMENT alliance EMPTY>
<!ATTLIST alliance player IDREF #REQUIRED alliance CDATA #REQUIRED>

<!ELEMENT unitList (unit+)>
<!ELEMENT unit EMPTY>
<!ATTLIST unit name ID #REQUIRED>

<!ELEMENT relationshipTypes (relationshipType+)>
<!ELEMENT relationshipType EMPTY>
<!ATTLIST relationshipType name ID #REQUIRED>

<!ELEMENT territoryEffectList (territoryEffect+)>
<!ELEMENT territoryEffect EMPTY>
<!ATTLIST territoryEffect name ID #REQUIRED>

<!ELEMENT gamePlay (delegate+, sequence, offset?)>
<!ELEMENT delegate EMPTY>
<!ATTLIST delegate name ID #REQUIRED javaClass CDATA #REQUIRED display CDATA #IMPLIED>
<!ELEMENT sequence (step+)>
<!ELEMENT step (stepProperty*)>
<!ATTLIST step name ID #REQUIRED delegate IDREF #REQUIRED player IDREF #IMPLIED maxRunCount CDATA #IMPLIED display CDATA #IMPLIED>
<!ELEMENT stepProperty EMPTY>
<!ATTLIST stepProperty name CDATA #REQUIRED value CDATA #REQUIRED>
<!ELEMENT offset EMPTY>
<!ATTLIST offset round CDATA #REQUIRED>

<!ELEMENT production ANY>
<!ELEMENT technology ANY>

<!ELEMENT attachmentList (attachment+)>
<!ELEMENT attachment (option+)>
<!ATTLIST attachment foreach CDATA #IMPLIED name CDATA #REQUIRED attachTo CDATA #REQUIRED javaClass CDATA #REQUIRED type (unitType|territory|resource|player|relationship|territoryEffect|technology) "unitType">
<!ELEMENT option EMPTY>
<!ATTLIST option name CDATA #REQUIRED value CDATA #REQUIRED count CDATA "">

<!ELEMENT initialize (ownerInitialize?, unitInitialize?, resourceInitialize?, relationshipInitialize?)>
<!ELEMENT ownerInitialize (territoryOwner+)>
<!ELEMENT territoryOwner EMPTY>
<!ATTLIST territoryOwner territory CDATA #REQUIRED owner IDREF #REQUIRED>
<!ELEMENT unitInitialize (unitPlacement*, heldUnits*)>
<!ELEMENT unitPlacement EMPTY>
<!ATTLIST unitPlacement unitType IDREF #REQUIRED territory CDATA #REQUIRED quantity CDATA #REQUIRED owner IDREF #IMPLIED hitsTaken CDATA #IMPLIED unitDamage CDATA #IMPLIED>
<!ELEMENT heldUnits EMPTY>
<!ATTLIST heldUnits unitType IDREF #REQUIRED player IDREF #REQUIRED quantity CDATA #REQUIRED>
<!ELEMENT resourceInitialize (resourceGiven+)>
<!ELEMENT resourceGiven EMPTY>
<!ATTLIST resourceGiven player IDREF #REQUIRED resource IDREF #REQUIRED quantity CDATA #REQUIRED>
<!ELEMENT relationshipInitialize (relationship+)>
<!ELEMENT relationship EMPTY>
<!ATTLIST relationship player1 IDREF #REQUIRED player2 IDREF #REQUIRED type IDREF #REQUIRED roundValue CDATA #REQUIRED>

<!ELEMENT propertyList (property*)>
<!ELEMENT property (boolean?, string?, number?, value?)>
<!ATTLIST property value CDATA "" name CDATA #REQUIRED editable (true|false) "false" player CDATA "">
<!ELEMENT value (#PCDATA)>
<!ELEMENT boolean EMPTY>
<!ELEMENT string EMPTY>
<!ELEMENT number EMPTY>
<!ATTLIST number max CDATA #REQUIRED min CDATA #REQUIRED>
'''

NOTES = '''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Small Front: Vistula Withdrawal</title></head>
<body>
<h1>Small Front: Vistula Withdrawal</h1>
<p>
An operational abstraction of the 1939 Polish campaign. The German player has the stronger
concentrated mobile formations. Poland begins with more units, but they are dispersed across a broad
front and become vulnerable when Warsaw and Deblin, the two eastern supply gateways, are cut.
</p>
<h2>Polish problem</h2>
<ul>
  <li>Polish infantry has combat movement 1 but redeployment movement 3.</li>
  <li>Cavalry has combat movement 2 and redeployment movement 4.</li>
  <li>Do not defend every border territory. Fight delaying actions, then use Redeployment to leave
      the next pocket before the German armour closes it.</li>
  <li>Units isolated from a Polish source for two turns are removed.</li>
</ul>
<h2>German problem</h2>
<p>
Drive on Kutno, Lodz and Radom to compress the Polish front, then seize both Warsaw and Deblin.
Taking only one gateway leaves a second route east. Taking both cuts the western road network from
Siedlce, Lublin, Brest and Lwow.
</p>
<h2>Victory</h2>
<p>
The game scores after round 7. Objectives reward delay and depth; supplied German occupation of the
two gateways and eastern depots is worth additional points. Ties favour Poland.
</p>
<p>This is a gameplay prototype, not a geographically or chronologically exact simulation.</p>
</body>
</html>
'''

README = '''# Small Front: Vistula Withdrawal

A 35-territory operational scenario for the custom Small Front TripleA engine. Germany has the
stronger, concentrated mobile force. Poland has a broad, brittle front and unusually strong
**Redeployment** values.

## Core decision

Polish infantry moves only 1 territory during Combat Move, but 3 during Redeployment. Cavalry moves
2 in combat and 4 in Redeployment. The Polish player must decide which positions can be screened for
one more turn and which formations must leave immediately.

The map has two load-bearing eastern supply gateways:

- **Warsaw–Siedlce** on the northern route
- **Deblin–Lublin** on the southern route

Losing either is survivable. Losing both cuts the western road network from the Polish supply
sources at Siedlce, Lublin, Brest and Lwow. Because isolation attrition removes units after two
turns, a late withdrawal is usually a destroyed withdrawal.

## Scope

- 35 land territories
- 76 movement edges
- 47 supply roads
- 7-round fixed-reinforcement scenario
- radius-1 fog of war
- terrain stack limits: Open 7, Town 6, Forest 5
- two-turn isolation attrition
- no purchase or placement phase

## Intended Polish play

Use frontier formations as screens, not anchors. Preserve a connected road route to one of the two
Vistula gateways, rotate damaged or exposed groups east, and counterattack only when it opens a
retreat route or delays a German mobile stack.

## Intended German play

Avoid grinding every Polish position. Use armour and mechanized units to threaten the rear, force
premature redeployments, and converge on Warsaw and Deblin. The scoring bonuses favour supplied
penetration, not unsupported raids.

## Balance status

The order of battle and reinforcement schedule are first-pass values. The smoke test verifies that
the map parses and both AIs fight; it does not establish competitive balance.

## Installation

Copy the top-level `small_front_poland` folder into the TripleA downloaded-maps directory. The map
requires the custom Small Front engine build in this repository.
'''

TOOLS_README = '''# Map tools

Run from this directory:

```bash
python generate_map.py ../
python validate_map.py ../
```

`generate_map.py` uses Pillow and writes the complete map package: Voronoi territory polygons,
base tiles, NATO-style counters, game XML and metadata. Territory cells are generated by clipping a
bounding rectangle against every pairwise Voronoi half-plane, so SciPy and Shapely are not required.

`validate_map.py` checks:

- exact territory, movement-edge and road counts
- road/movement-edge consistency
- generated map support files
- the two-gateway supply topology
- Polish combat versus Redeployment movement values
- synchronized runtime and smoke-test XML
'''

MAP_YML = '''map_name: small_front_poland
games:
- {game_name: "Small Front: Vistula Withdrawal", file_name: "Small_Front_Poland.xml"}
'''

MAP_PROPERTIES = '''color.Germans=626262
color.Poland=BC1E2C
color.Neutral=E8DFC7
color.Impassable=333333

map.width=1024
map.height=768
map.hasRelief=false
map.showTerritoryNames=false
map.mapBlends=false
map.scrollWrapX=false
map.scrollWrapY=false
units.scale=0.9000
units.width=40
units.height=40

screenshot.title.x=30
screenshot.title.y=30
screenshot.title.color=202020
screenshot.title.font.size=22
screenshot.stats.enabled=true
screenshot.stats.x=30
screenshot.stats.y=710
screenshot.stats.text.color=202020
screenshot.stats.border.color=F0E8D0
'''


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    map_dir = destination / "map"
    cells = voronoi_cells()
    image = draw_map(cells)
    save_tiles(image, map_dir / "baseTiles")
    image.resize((256, 192), Image.Resampling.LANCZOS).save(map_dir / "smallMap.png", optimize=True)
    preview_dir = destination / "preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    image.resize((768, 576), Image.Resampling.LANCZOS).save(
        preview_dir / "vistula_withdrawal_preview.png", optimize=True
    )

    write_text(destination / ".gitignore", "__pycache__/\n*.pyc\n")
    write_text(destination / "README.md", README)
    write_text(destination / "map.yml", MAP_YML)
    write_text(destination / "tools" / "README.md", TOOLS_README)
    write_text(map_dir / "map.properties", MAP_PROPERTIES)
    write_text(map_dir / "games" / "Small_Front_Poland.xml", game_xml())
    write_text(map_dir / "games" / "Small_Front_Poland.notes.html", NOTES)
    write_text(map_dir / "games" / "game.dtd", DTD)

    names = sorted(SITES)
    write_text(
        map_dir / "centers.txt",
        "".join(f"{name}  ({SITES[name][0]},{SITES[name][1]})\n" for name in names),
    )
    write_text(
        map_dir / "polygons.txt",
        "".join(
            f"{name}  <  {' '.join(f'({x},{y})' for x, y in cells[name])} >\n"
            for name in names
        ),
    )
    write_text(
        map_dir / "place.txt",
        "".join(
            f"{name}  ({x-20},{y-19})  ({x+20},{y-19})  ({x-20},{y+19})  ({x+20},{y+19})\n"
            for name, (x, y) in sorted(SITES.items())
        ),
    )
    label_draw = ImageDraw.Draw(image)
    label_font = load_font(12)
    write_text(
        map_dir / "name_place.txt",
        "".join(
            f"{name}  ({label_position(name, label_draw, label_font)[0]},"
            f"{label_position(name, label_draw, label_font)[1]})\n"
            for name in names
        ),
    )
    write_text(
        map_dir / "vc.txt",
        "".join(f"{name}  ({SITES[name][0]},{SITES[name][1]})\n" for name in sorted(OBJECTIVES)),
    )

    vc = Image.new("RGBA", (18, 18), (0, 0, 0, 0))
    vc_draw = ImageDraw.Draw(vc)
    vc_draw.ellipse((2, 2, 15, 15), fill="#f2d35d", outline="#202020", width=2)
    vc_draw.line((9, 4, 9, 13), fill="#202020", width=2)
    vc_draw.line((5, 9, 13, 9), fill="#202020", width=2)
    (map_dir / "misc").mkdir(parents=True, exist_ok=True)
    vc.save(map_dir / "misc" / "vc.png", optimize=True)

    draw_counter(map_dir / "units" / "Germans" / "infantry.png", "#626262", "infantry")
    draw_counter(map_dir / "units" / "Germans" / "armour.png", "#626262", "armour")
    draw_counter(map_dir / "units" / "Germans" / "mechanized.png", "#626262", "mechanized")
    draw_counter(
        map_dir / "units" / "Germans" / "selfPropelledArtillery.png",
        "#626262",
        "selfPropelledArtillery",
    )
    draw_counter(
        map_dir / "units" / "Poland" / "polishInfantry.png", "#bc1e2c", "infantry"
    )
    draw_counter(
        map_dir / "units" / "Poland" / "polishArtillery.png", "#bc1e2c", "artillery"
    )
    draw_counter(map_dir / "units" / "Poland" / "cavalry.png", "#bc1e2c", "cavalry")

    manifest = []
    for path in sorted(destination.rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            manifest.append(
                {"path": path.relative_to(destination).as_posix(), "bytes": path.stat().st_size}
            )
    write_text(destination / "manifest.json", json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    import sys

    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    generate(destination.resolve())
    print(
        f"territories={len(SITES)} connections={len(MOVEMENT_EDGES)} "
        f"roads={len({tuple(sorted(edge)) for edge in ROADS})} objectives={len(OBJECTIVES)}"
    )


if __name__ == "__main__":
    main()
