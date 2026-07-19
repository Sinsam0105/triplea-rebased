#!/usr/bin/env python3
"""Validate Small Front: Vistula Withdrawal."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from pathlib import Path

EXPECTED_TERRITORIES = 35
EXPECTED_CONNECTIONS = 76
EXPECTED_ROADS = 47
POLISH_SOURCES = {"Siedlce", "Lublin", "Brest", "Lwow"}


def support_names(path: Path) -> set[str]:
    return {
        line.split("  ", 1)[0]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def edge(first: str, second: str) -> tuple[str, str]:
    return tuple(sorted((first, second)))


def reachable(
    nodes: set[str],
    edges: set[tuple[str, str]],
    starts: set[str],
    removed: set[str],
) -> set[str]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for first, second in edges:
        if first in removed or second in removed:
            continue
        adjacency[first].add(second)
        adjacency[second].add(first)
    queue = deque(starts - removed)
    visited = set(queue)
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited & (nodes - removed)


def options_for(root: ET.Element, class_name: str, attach_to: str) -> dict[str, str]:
    for attachment in root.findall("./attachmentList/attachment"):
        if attachment.get("javaClass") == class_name and attachment.get("attachTo") == attach_to:
            return {
                option.get("name", ""): option.get("value", "")
                for option in attachment.findall("option")
            }
    raise AssertionError(f"missing attachment: {class_name} {attach_to}")


def main() -> None:
    map_root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else Path(__file__).resolve().parent.parent
    )
    smoke_xml = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    runtime_xml = map_root / "map/games/Small_Front_Poland.xml"

    required = [
        "README.md",
        "map.yml",
        "manifest.json",
        "map/games/Small_Front_Poland.xml",
        "map/games/Small_Front_Poland.notes.html",
        "map/games/game.dtd",
        "map/map.properties",
        "map/centers.txt",
        "map/polygons.txt",
        "map/place.txt",
        "map/name_place.txt",
        "map/vc.txt",
        "map/smallMap.png",
        "map/misc/vc.png",
        "tools/generate_map.py",
        "tools/validate_map.py",
    ]
    required.extend(f"map/baseTiles/{x}_{y}.png" for x in range(4) for y in range(3))
    required.extend(
        [
            "map/units/Germans/infantry.png",
            "map/units/Germans/armour.png",
            "map/units/Germans/mechanized.png",
            "map/units/Germans/selfPropelledArtillery.png",
            "map/units/Poland/polishInfantry.png",
            "map/units/Poland/polishArtillery.png",
            "map/units/Poland/cavalry.png",
        ]
    )
    missing = [relative for relative in required if not (map_root / relative).is_file()]
    assert not missing, f"missing generated files: {missing}"

    root = ET.parse(runtime_xml).getroot()
    territories = {node.get("name", "") for node in root.findall("./map/territory")}
    assert len(territories) == EXPECTED_TERRITORIES, len(territories)

    connections: set[tuple[str, str]] = set()
    for node in root.findall("./map/connection"):
        first, second = node.get("t1", ""), node.get("t2", "")
        assert first in territories and second in territories and first != second
        canonical = edge(first, second)
        assert canonical not in connections, f"duplicate connection: {canonical}"
        connections.add(canonical)
    assert len(connections) == EXPECTED_CONNECTIONS, len(connections)

    for filename in ["centers.txt", "polygons.txt", "place.txt", "name_place.txt"]:
        actual = support_names(map_root / "map" / filename)
        assert actual == territories, (
            filename,
            sorted(territories - actual),
            sorted(actual - territories),
        )

    roads: set[tuple[str, str]] = set()
    sources: set[str] = set()
    for attachment in root.findall("./attachmentList/attachment"):
        if attachment.get("javaClass") != (
            "games.strategy.triplea.attachments.SupplyTerritoryAttachment"
        ):
            continue
        source = attachment.get("attachTo", "")
        assert source in territories
        for option in attachment.findall("option"):
            name, value = option.get("name"), option.get("value", "")
            if name == "supplySource" and value == "true":
                sources.add(source)
            elif name == "roadConnection":
                assert value in territories and value != source
                canonical = edge(source, value)
                assert canonical not in roads, f"duplicate road: {canonical}"
                roads.add(canonical)

    assert len(roads) == EXPECTED_ROADS, len(roads)
    assert roads <= connections
    assert POLISH_SOURCES <= sources
    assert reachable(territories, roads, {"Brest"}, set()) == territories

    # A single open gateway is enough; losing both isolates the western army.
    for removed in [{"Warsaw"}, {"Deblin"}]:
        assert "Poznan" in reachable(territories, roads, POLISH_SOURCES, removed)
    both_cut = reachable(territories, roads, POLISH_SOURCES, {"Warsaw", "Deblin"})
    assert "Poznan" not in both_cut
    assert POLISH_SOURCES <= both_cut

    # Legal movement temptations that do not carry supply.
    for bypass in [
        edge("Modlin", "Siedlce"),
        edge("Deblin", "Lukow"),
        edge("Deblin", "Zamosc"),
    ]:
        assert bypass in connections and bypass not in roads

    unit_class = "games.strategy.triplea.attachments.UnitAttachment"
    expected_movement = {
        "infantry": ("1", "1"),
        "polishInfantry": ("1", "3"),
        "polishArtillery": ("1", "2"),
        "cavalry": ("2", "4"),
        "armour": ("2", "3"),
        "mechanized": ("2", "3"),
        "selfPropelledArtillery": ("2", "3"),
    }
    for unit_type, (combat, redeployment) in expected_movement.items():
        options = options_for(root, unit_class, unit_type)
        assert options["combatMovement"] == combat
        assert options["redeploymentMovement"] == redeployment

    effect_class = "games.strategy.triplea.attachments.TerritoryEffectAttachment"
    capacities = {
        effect: options_for(root, effect_class, effect)["stackCapacity"]
        for effect in ["Open", "Forest", "Town"]
    }
    assert capacities == {"Open": "7", "Forest": "5", "Town": "6"}

    polish_redeployment = root.find("./gamePlay/sequence/step[@name='polishRedeployment']")
    assert polish_redeployment is not None
    step_options = {
        item.get("name", ""): item.get("value", "")
        for item in polish_redeployment.findall("stepProperty")
    }
    assert step_options["nonCombatMove"] == "true"

    if smoke_xml is not None:
        assert smoke_xml.is_file(), smoke_xml
        assert runtime_xml.read_bytes() == smoke_xml.read_bytes(), "smoke XML is out of sync"

    listed = {
        item["path"]: item["bytes"]
        for item in json.loads((map_root / "manifest.json").read_text(encoding="utf-8"))
    }
    for relative, size in listed.items():
        path = map_root / relative
        assert path.is_file(), relative
        assert path.stat().st_size == size, (relative, size, path.stat().st_size)

    print(
        f"validated territories={len(territories)} connections={len(connections)} "
        f"roads={len(roads)} sources={len(sources)}"
    )


if __name__ == "__main__":
    main()
