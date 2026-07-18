from __future__ import annotations

from pathlib import Path
import math
import random
import re
import zipfile
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_XML = ROOT / "game-app/smoke-testing/src/test/resources/map-xmls/Small_Front_Meuse.xml"
MAP_ROOT = ROOT / "maps/small_front_meuse"
WIDTH, HEIGHT = 1600, 1200

CENTERS = {
    "Huy": (270, 115),
    "Andenne": (430, 130),
    "Namur": (590, 150),
    "Havelange": (460, 270),
    "Ciney": (650, 285),
    "Dinant": (760, 285),
    "Durbuy": (350, 350),
    "Marche": (535, 410),
    "Rochefort": (700, 430),
    "Givet": (900, 390),
    "Erezee": (300, 500),
    "La Roche": (430, 525),
    "Hotton": (530, 535),
    "Nassogne": (650, 560),
    "Wellin": (790, 520),
    "Beauraing": (900, 520),
    "St. Vith": (230, 680),
    "Vielsalm": (340, 650),
    "Houffalize": (460, 685),
    "Bastogne": (580, 720),
    "Saint-Hubert": (700, 700),
    "Neufchateau": (850, 740),
    "Bertrix": (990, 700),
    "Losheim Gap": (250, 865),
    "Clervaux": (430, 850),
    "Wiltz": (560, 850),
    "Martelange": (700, 870),
    "Libramont": (840, 870),
    "Blankenheim": (180, 1040),
    "Prum": (380, 1030),
    "Bitburg": (590, 1040),
    "Vianden": (690, 975),
    "Echternach": (820, 1050),
}

GROUND_UNITS = (
    "infantry",
    "americanInfantry",
    "artillery",
    "selfPropelledArtillery",
    "armour",
    "mechanized",
)
ALL_UNITS = (*GROUND_UNITS, "fighter")


def regular_hexagon(x: int, y: int, radius: int = 50) -> list[tuple[int, int]]:
    return [
        (
            round(x + math.cos(index * math.pi / 3) * radius),
            round(y + math.sin(index * math.pi / 3) * radius),
        )
        for index in range(6)
    ]


def parse_scenario(xml_text: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    root = ET.fromstring(re.sub(r"<!DOCTYPE.*?>", "", xml_text))
    connections = [
        (element.attrib["t1"], element.attrib["t2"])
        for element in root.findall("./map/connection")
    ]
    roads: list[tuple[str, str]] = []
    for attachment in root.findall("./attachmentList/attachment"):
        if attachment.attrib.get("name") != "supplyTerritoryAttachment":
            continue
        source = attachment.attrib["attachTo"]
        roads.extend(
            (source, option.attrib["value"])
            for option in attachment.findall("option")
            if option.attrib.get("name") == "roadConnection"
        )
    return connections, roads


def draw_board(
    connections: list[tuple[str, str]], roads: list[tuple[str, str]]
) -> Image.Image:
    random.seed(44)
    image = Image.new("RGB", (WIDTH, HEIGHT), (65, 105, 48))
    draw = ImageDraw.Draw(image)

    for _ in range(24_000):
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        variation = random.randrange(-12, 13)
        draw.point(
            (x, y),
            fill=(
                max(30, 65 + variation),
                max(55, 105 + variation),
                max(25, 48 + variation),
            ),
        )

    for first, second in connections:
        draw.line((CENTERS[first], CENTERS[second]), fill=(145, 142, 104), width=4)
    for first, second in roads:
        draw.line((CENTERS[first], CENTERS[second]), fill=(88, 52, 38), width=7)
        draw.line((CENTERS[first], CENTERS[second]), fill=(202, 174, 107), width=3)

    rivers = (
        ((150, 210), (420, 210), (650, 235), (820, 300), (1050, 325), (1450, 300)),
        ((720, 80), (690, 300), (740, 500), (790, 700), (850, 900), (930, 1140)),
    )
    for river in rivers:
        draw.line(river, fill=(25, 70, 150), width=15, joint="curve")
        draw.line(river, fill=(48, 112, 205), width=8, joint="curve")

    initial_front = (
        (170, 600),
        (300, 610),
        (420, 645),
        (530, 690),
        (620, 785),
        (720, 900),
        (820, 1080),
    )
    draw.line(initial_front, fill=(125, 20, 20), width=7)

    for x, y in CENTERS.values():
        polygon = regular_hexagon(x, y)
        draw.line([*polygon, polygon[0]], fill=(32, 52, 26), width=2)

    font = ImageFont.load_default()
    for name, (x, y) in CENTERS.items():
        bounds = draw.textbbox((0, 0), name, font=font)
        text_width = bounds[2] - bounds[0]
        draw.rectangle(
            (x - text_width // 2 - 3, y - 7, x + text_width // 2 + 3, y + 7),
            fill=(220, 209, 155),
        )
        draw.text((x - text_width // 2, y - 5), name, font=font, fill=(22, 25, 18))

    draw.rectangle((1120, 920, 1570, 1160), fill=(226, 215, 165), outline=(60, 55, 35), width=3)
    draw.text((1140, 940), "SMALL FRONT: MEUSE CORRIDOR", font=font, fill=(25, 25, 20))
    draw.text((1140, 970), "NATO BATTALION SCALE (II)", font=font, fill=(25, 25, 20))
    draw.line((1140, 1005, 1220, 1005), fill=(202, 174, 107), width=5)
    draw.text((1230, 999), "Supply road", font=font, fill=(25, 25, 20))
    draw.line((1140, 1035, 1220, 1035), fill=(48, 112, 205), width=8)
    draw.text((1230, 1029), "River", font=font, fill=(25, 25, 20))
    draw.line((1140, 1065, 1220, 1065), fill=(125, 20, 20), width=6)
    draw.text((1230, 1059), "Initial front", font=font, fill=(25, 25, 20))
    return image


def write_tiles(image: Image.Image, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for row, y in enumerate(range(0, HEIGHT, 256)):
        for column, x in enumerate(range(0, WIDTH, 256)):
            tile = Image.new("RGB", (256, 256), (60, 90, 40))
            tile.paste(image.crop((x, y, min(x + 256, WIDTH), min(y + 256, HEIGHT))), (0, 0))
            tile.save(directory / f"{column}_{row}.png")


def draw_nato_counter(unit_name: str, fill: tuple[int, int, int], ink: tuple[int, int, int]) -> Image.Image:
    icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    font = ImageFont.load_default()
    draw.text((27, 0), "II", font=font, fill=ink)
    draw.rectangle((7, 15, 57, 54), fill=fill, outline=ink, width=3)

    if unit_name in {"infantry", "americanInfantry", "mechanized"}:
        draw.line((10, 18, 54, 51), fill=ink, width=3)
        draw.line((54, 18, 10, 51), fill=ink, width=3)
    if unit_name in {"armour", "mechanized", "selfPropelledArtillery"}:
        draw.ellipse((18, 27, 46, 43), outline=ink, width=3)
    if unit_name in {"artillery", "selfPropelledArtillery"}:
        draw.ellipse((28, 29, 36, 37), fill=ink)
    if unit_name == "fighter":
        draw.polygon(
            ((32, 19), (38, 31), (52, 36), (38, 39), (34, 51), (30, 51), (26, 39), (12, 36), (26, 31)),
            fill=ink,
        )
    return icon


def write_map_files(xml_text: str, image: Image.Image) -> None:
    game_path = MAP_ROOT / "map/games/Small_Front_Meuse.xml"
    game_path.parent.mkdir(parents=True, exist_ok=True)
    game_path.write_text(xml_text, encoding="utf-8")

    (MAP_ROOT / "map.yml").write_text(
        "map_name: small_front_meuse\n"
        "games:\n"
        "- {game_name: Small Front: Meuse Corridor, file_name: Small_Front_Meuse.xml}\n",
        encoding="utf-8",
    )
    (MAP_ROOT / "map/map.properties").write_text(
        "color.Germans=7d4038\n"
        "color.Americans=4d617c\n"
        "units.scale=1\n"
        "map.showTerritoryNames=true\n"
        "map.hasRelief=true\n"
        "map.showCapitolMarkers=true\n"
        "map.scrollWrapX=false\n"
        f"map.width={WIDTH}\n"
        f"map.height={HEIGHT}\n",
        encoding="utf-8",
    )
    (MAP_ROOT / "map/centers.txt").write_text(
        "\n".join(f"{name}  ({x},{y})" for name, (x, y) in CENTERS.items()) + "\n",
        encoding="utf-8",
    )
    (MAP_ROOT / "map/place.txt").write_text(
        "\n".join(
            f"{name}  ({x - 23},{y - 23})  ({x + 23},{y - 23})  "
            f"({x - 23},{y + 23})  ({x + 23},{y + 23})"
            for name, (x, y) in CENTERS.items()
        )
        + "\n",
        encoding="utf-8",
    )
    (MAP_ROOT / "map/polygons.txt").write_text(
        "\n".join(
            f"{name}  <  " + " ".join(f"({x},{y})" for x, y in regular_hexagon(*center)) + " >"
            for name, center in CENTERS.items()
        )
        + "\n",
        encoding="utf-8",
    )

    image.save(MAP_ROOT / "preview.png")
    write_tiles(image, MAP_ROOT / "map/baseTiles")
    write_tiles(image, MAP_ROOT / "map/reliefTiles")

    side_colors = {
        "Germans": ((238, 220, 189), (80, 28, 25)),
        "Americans": ((178, 198, 218), (27, 48, 72)),
    }
    for side, (fill, ink) in side_colors.items():
        unit_directory = MAP_ROOT / "map/units" / side
        unit_directory.mkdir(parents=True, exist_ok=True)
        for unit_name in ALL_UNITS:
            draw_nato_counter(unit_name, fill, ink).save(unit_directory / f"{unit_name}.png")


def write_archive() -> None:
    archive_path = ROOT / "maps/small_front_meuse.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in MAP_ROOT.rglob("*"):
            if path.is_file() and path.name != "preview.png":
                archive.write(path, path.relative_to(MAP_ROOT))


def main() -> None:
    xml_text = SCENARIO_XML.read_text(encoding="utf-8")
    connections, roads = parse_scenario(xml_text)
    image = draw_board(connections, roads)
    write_map_files(xml_text, image)
    write_archive()


if __name__ == "__main__":
    main()
