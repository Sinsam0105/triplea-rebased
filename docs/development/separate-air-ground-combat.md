# Separate air and ground combat

Small Front scenarios can opt into a combat model where aircraft resolve a dedicated air battle before the territory's ground or sea battle.

## Rule switch

```xml
<property name="Separate Air And Ground Combat" value="true" editable="false"/>
```

The property defaults to `false`, preserving existing TripleA behavior.

## Scheduling

When enabled for a normal attack:

1. attacking units with `canAirBattle` are assigned to an `AIR_BATTLE`;
2. the normal battle is created only from non-air attackers;
3. enemy air-battle-capable aircraft are assigned to the air battle;
4. the normal battle depends on the air battle and cannot resolve first;
5. aircraft that survive, withdraw, or are grounded are marked as having completed air combat and are excluded from the normal battle.

Bombing raids retain their existing air-raid behavior.

## Territory control

Aircraft never create an empty ground battle and never trigger territory takeover. A territory can be captured only when a non-air attacking unit survives the normal battle or enters an otherwise empty territory under the existing takeover rules.

## Compatibility

With the property disabled, existing pre-battle interception behavior is unchanged: surviving aircraft may continue into the normal battle according to current TripleA rules.

The implementation reuses `AirBattle`, `BattleTracker` dependencies, `WAS_IN_AIR_BATTLE`, existing retreat/destruction logic, and terrain-specific air round limits.