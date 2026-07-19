# Small Front: Vistula Withdrawal

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
