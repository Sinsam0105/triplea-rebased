from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    source_path = Path(path)
    source = source_path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"expected one match in {path}, found {count}")
    source_path.write_text(source.replace(old, new), encoding="utf-8")


replace_once(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/MustFightBattle.java",
    """    maxRounds =
        battleSite.isWater()
            ? Properties.getSeaBattleRounds(data.getProperties())
            : Properties.getLandBattleRounds(data.getProperties());""",
    """    maxRounds =
        BattleRoundResolver.resolveGroundBattleRounds(battleSite, territoryEffects, data);""",
)

replace_once(
    "game-app/game-core/src/main/java/games/strategy/triplea/delegate/battle/AirBattle.java",
    "    maxRounds = Properties.getAirBattleRounds(data.getProperties());",
    "    maxRounds = BattleRoundResolver.resolveAirBattleRounds(territoryEffects, data);",
)
