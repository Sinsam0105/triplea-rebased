# Separate air and ground combat

Milestone 9 makes combat domain explicit before changing battle scheduling and rosters.

## Domain model

Each `IBattle.BattleType` has one domain:

- `GROUND`: normal land or sea combat
- `AIR`: fighter and interceptor combat that determines the local air result
- `RAID`: strategic bombing and its escort/interception phase

`AirGroundBattlePolicy` is the common source for unit partitioning and resolution priority.

## Required resolution order

For battles in the same territory:

1. raid-related combat
2. air-domain combat
3. ground-domain combat

The tracker must represent this as dependencies rather than relying on collection iteration order.

## Unit participation

When separated combat is enabled:

- aircraft are assigned to the air-domain battle
- non-air units are assigned to the ground-domain battle
- aircraft are not copied into the ground battle roster
- air-only forces cannot create an ownership-changing empty or ground battle
- only a surviving eligible non-air attacker may capture territory

## Round limits

The existing `BattleRoundResolver` remains authoritative:

- air-domain battles use `maxAirBattleRounds`
- ground-domain battles use `maxGroundBattleRounds`
- global properties remain compatibility fallbacks

## Delivery sequence

This milestone is implemented in reviewable slices:

1. explicit domain model and deterministic policy
2. tracker roster partitioning and dependency integration
3. air-battle survivor handoff and withdrawal rules
4. ownership and regression coverage

Air control is intentionally deferred to milestone 10. The result of an air battle is exposed there without overloading `Territory.owner`.
