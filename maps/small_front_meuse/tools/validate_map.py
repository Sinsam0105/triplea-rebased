#!/usr/bin/env python3
from pathlib import Path
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
game = root / "map" / "games" / "Small_Front_Meuse.xml"
required = [
    root / "map.yml",
    root / "map" / "map.properties",
    root / "map" / "centers.txt",
    root / "map" / "place.txt",
    root / "map" / "polygons.txt",
    root / "map" / "units" / "Germans" / "airfield.png",
    root / "map" / "units" / "Americans" / "airfield.png",
    root / "tools" / "UnitGen.java",
    game,
]
missing = [str(path.relative_to(root)) for path in required if not path.exists()]
if missing:
    raise SystemExit("Missing files: " + ", ".join(missing))

tree = ET.parse(game)
game_root = tree.getroot()
territories = {node.attrib["name"] for node in game_root.findall("./map/territory")}
connections = game_root.findall("./map/connection")
movement_edges = set()
for connection in connections:
    first = connection.attrib["t1"]
    second = connection.attrib["t2"]
    assert first in territories
    assert second in territories
    movement_edges.add(tuple(sorted((first, second))))

centers = {}
pattern = re.compile(r"^(.*?)\s+\((\d+),(\d+)\)")
for line in (root / "map" / "centers.txt").read_text(encoding="utf-8").splitlines():
    match = pattern.match(line)
    if match:
        centers[match.group(1)] = (int(match.group(2)), int(match.group(3)))
assert set(centers) == territories, set(centers) ^ territories

roads = set()
for attachment in game_root.findall("./attachmentList/attachment"):
    if attachment.attrib.get("javaClass", "").endswith("SupplyTerritoryAttachment"):
        source = attachment.attrib["attachTo"]
        assert source in territories
        for option in attachment.findall("option"):
            if option.attrib["name"] == "roadConnection":
                target = option.attrib["value"]
                assert target in territories
                roads.add(tuple(sorted((source, target))))

assert len(roads) == 46, len(roads)
assert roads <= movement_edges, roads - movement_edges
assert tuple(sorted(("La Roche", "Marche"))) in roads
assert tuple(sorted(("Libramont", "Neufchateau"))) in roads
assert tuple(sorted(("Vielsalm", "Durbuy"))) in roads
for removed in {
    tuple(sorted(("Hotton", "Marche"))),
}:
    assert removed not in roads, removed

road_neighbors = {territory: set() for territory in territories}
for first, second in roads:
    road_neighbors[first].add(second)
    road_neighbors[second].add(first)


def road_components_without(blocked):
    remaining = territories - {blocked}
    components = []
    visited = set()
    for start in sorted(remaining):
        if start in visited:
            continue
        pending = [start]
        component = set()
        while pending:
            current = pending.pop()
            if current in visited:
                continue
            visited.add(current)
            component.add(current)
            pending.extend(road_neighbors[current] - visited - {blocked})
        components.append(component)
    return components


# The added La Roche-Marche road prevents one central plateau hub from splitting the map in half.
for central_hub in ("Hotton", "Nassogne", "Neufchateau"):
    assert len(road_components_without(central_hub)) == 1, central_hub

stack_capacities = {}
for attachment in game_root.findall("./attachmentList/attachment"):
    if attachment.attrib.get("javaClass", "").endswith("TerritoryEffectAttachment"):
        for option in attachment.findall("option"):
            if option.attrib["name"] == "stackCapacity":
                stack_capacities[attachment.attrib["attachTo"]] = int(option.attrib["value"])
assert stack_capacities == {"Open": 7, "Forest": 5, "Town": 6}, stack_capacities

unit_options = {}
for attachment in game_root.findall("./attachmentList/attachment"):
    if attachment.attrib.get("javaClass", "").endswith("UnitAttachment"):
        unit_options[attachment.attrib["attachTo"]] = {
            option.attrib["name"]: option.attrib["value"] for option in attachment.findall("option")
        }

armour = unit_options["armour"]
assert armour["attack"] == "2"
assert armour["attackRolls"] == "2"
assert armour["defense"] == "3"
assert armour["tuv"] == "7"

# Early-game redeployment penalty: mobile ground redeployment starts at the combat-movement value
# and is restored to the pre-existing reach at round 5 by a trigger.
assert unit_options["americanInfantry"]["redeploymentMovement"] == "1"
for mobile in ("armour", "mechanized", "selfPropelledArtillery"):
    assert unit_options[mobile]["redeploymentMovement"] == "2", (
        mobile,
        unit_options[mobile].get("redeploymentMovement"),
    )

attachments_by_name = {
    attachment.attrib["name"]: attachment
    for attachment in game_root.findall("./attachmentList/attachment")
}
round_condition = attachments_by_name["smallFrontRoundFivePlus"]
assert round_condition.attrib["javaClass"].endswith("RulesAttachment")
assert any(
    option.attrib["name"] == "rounds" and option.attrib["value"] == "5-+"
    for option in round_condition.findall("option")
)
for trigger_name, expected_property in (
    ("raiseInfantryRedeployment", "2:redeploymentMovement"),
    ("raiseMobileRedeployment", "3:redeploymentMovement"),
):
    trigger = attachments_by_name[trigger_name]
    assert trigger.attrib["javaClass"].endswith("TriggerAttachment")
    trigger_options = {
        option.attrib["name"]: option.attrib["value"] for option in trigger.findall("option")
    }
    assert trigger_options["conditions"] == "smallFrontRoundFivePlus"
    assert trigger_options["when"] == "before:germanReinforcement"
    assert trigger_options["unitProperty"] == expected_property
    assert trigger_options["uses"] == "1"

fighter = unit_options["fighter"]
assert fighter["canScramble"] == "true"
assert fighter["maxScrambleDistance"] == "2"

airfield = unit_options["airfield"]
assert airfield["isInfrastructure"] == "true"
assert airfield["isAirBase"] == "true"
assert airfield["maxScrambleCount"] == "2"

airfield_placements = {
    (placement.attrib["territory"], placement.attrib["owner"])
    for placement in game_root.findall("./initialize/unitInitialize/unitPlacement")
    if placement.attrib["unitType"] == "airfield"
}
assert airfield_placements == {
    ("Prum", "Germans"),
    ("Bitburg", "Germans"),
    ("Ciney", "Americans"),
    ("Namur", "Americans"),
}, airfield_placements

properties = {
    prop.attrib["name"]: prop.attrib["value"] for prop in game_root.findall("./propertyList/property")
}
for name, expected in {
    "Use Triggers": "true",
    "Air Control Persistent": "false",
    "Scramble Rules In Effect": "true",
    "Scrambled Units Return To Base": "true",
    "Scramble To Sea Only": "false",
    "Scramble From Island Only": "false",
    "Battles May Be Preceeded By Air Battles": "true",
    "Can Scramble Into Air Battles": "true",
}.items():
    assert properties.get(name) == expected, (name, properties.get(name))

redeployment_steps = [
    step
    for step in game_root.findall("./gamePlay/sequence/step")
    if step.attrib.get("display") == "Redeployment"
]
assert len(redeployment_steps) == 2
for step in redeployment_steps:
    properties = {item.attrib["name"]: item.attrib["value"] for item in step.findall("stepProperty")}
    assert properties.get("nonCombatMove") == "true"
    assert properties.get("removeAirThatCanNotLand") == "false"

print(
    f"OK: {len(territories)} territories, {len(connections)} movement edges, "
    f"{len(roads)} roads, native radius-2 scramble, non-persistent air control, armour 2x@2 TUV 7"
)
