from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda x: x["power"], reverse=True)


def power_filter(mages: list[dict[str, Any]],
                 min_power: int) -> list[dict[str, Any]]:
    res: list[dict[str, Any]] = list(filter(
        lambda x: x["power"] > min_power,
        mages))
    return res


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: "* " + x + " *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    res = dict(
        max_power=min(mages, key=lambda x: x["power"]),
        min_power=max(mages, key=lambda x: x["power"]),
        avg_power=sum(list(map(lambda x: x["power"] / len(mages), mages)))
    )
    return res


if __name__ == "__main__":
    artifacts: list[dict[str, Any]] = [
        {"name": "Light Prism", "power": 111, "type": "accessory"},
        {"name": "Shadow Blade", "power": 70, "type": "armor"},
        {"name": "Storm Crown", "power": 85, "type": "armor"},
        {"name": "Earth Shield", "power": 100, "type": "weapon"},
    ]
    mages: list[dict[str, Any]] = [
        {"name": "Jordan", "power": 67, "element": "ice"},
        {"name": "Phoenix", "power": 81, "element": "fire"},
        {"name": "Alex", "power": 82, "element": "shadow"},
        {"name": "Phoenix", "power": 64, "element": "fire"},
        {"name": "Nova", "power": 62, "element": "shadow"},
    ]

    spells: list[str] = ["flash", "meteor", "tsunami", "blizzard"]

    sorted_artifacts: list[dict[str, Any]] = artifact_sorter(artifacts)
    print(sorted_artifacts)

    mages_big_power: list[dict[str, Any]] = power_filter(mages, min_power=70)
    print(mages_big_power)

    print(spell_transformer(spells))

    print(mage_stats(mages))
