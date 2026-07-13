# Battle simulation protocol

The first milestone intentionally adds an API boundary without changing battle rules.

## Run

```bash
./gradlew :game-headless:runBattleSimulationServer
```

The process reads one JSON object per stdin line and writes one response object per stdout line.

```json
{"command":"ping","data":{}}
```

A real simulation provider implements `BattleEnvironment` and registers it through Java `ServiceLoader`. Until a provider is installed, `ping` and `schema` work while state-changing commands return a structured error.

`BattleObservationFactory` produces stable unit groups sorted by owner, type, hits, and movement used. The DTO intentionally excludes UI objects and direct engine references so it can be serialized, replayed, and converted into an RL tensor later.
