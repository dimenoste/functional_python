from functools import partial, reduce, lru_cache, singledispatch
import operator
from typing import Any, Callable, Dict
import time


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells or len(spells) == 0:
        return 0
    ope: Dict[str, Callable[..., int]] = dict()
    ope["add"] = operator.add
    ope["multiply"] = operator.mul
    ope["max"] = max
    ope["min"] = min
    if ope.get(operation, None) is None:
        raise KeyError("Operation not supported!")
    return reduce(ope[operation], spells)


def base_enchantement(power: int, element: str, target: str) -> str:
    return f"{element} causes {target} to lose {power} PV"


def partial_enchanter(base_enchantment:
                      Callable[..., str]) -> dict[str, Callable[..., str]]:
    dico: Dict[str, Callable[..., str]] = dict()
    power_default = 50
    dico["fire"] = partial(base_enchantment, power_default, element="fire")
    dico["ice"] = partial(base_enchantment, power_default, element="ice")
    dico["water"] = partial(base_enchantment, power_default, element="water")
    return dico


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return (memoized_fibonacci(n - 2) + memoized_fibonacci(n - 1))


def fibo(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return (fibo(n - 2) + fibo(n - 1))


@singledispatch
def spell_dispatcher(spell: Any) -> str:
    return "Unknown spell type"


@spell_dispatcher.register
def _(spell: int) -> str:
    return f"Damage spell: {spell} damage"


@spell_dispatcher.register
def _(spell: str) -> str:
    return f"Enchantment: {spell}"


@spell_dispatcher.register(list)
def _(spell: list[str]) -> str:
    return f"Multi-cast: {len(spell)} spells"


if __name__ == "__main__":
    spells: list[int] = [1, 2, 3]

    print("\nTesting spell reducer...\n")
    print("Sum", spell_reducer(spells, "add"))
    print("Multiply", spell_reducer(spells, "multiply"))
    print("Max", spell_reducer(spells, "max"))
    print("Min", spell_reducer(spells, "min"))
    try:
        print("Min", spell_reducer(spells, "kioj"))
    except KeyError as e:
        print(f"ERROR: {e}")

    print()
    print("Testing partial enchanter...")
    fire_spell: Callable[..., str] = partial_enchanter(
        base_enchantement
        )["fire"]
    print(fire_spell(target="Dragon"))

    print("\nTesting memoized fibonacci vs classic fibo runtime...\n")

    start_time: float = time.time()
    print("Memoized fibo(35) =", memoized_fibonacci(35))
    print(f"--- {(round(time.time() - start_time, 5))} seconds ---")

    start_time2: float = time.time()
    print("fibo(35) =", fibo(35))
    print(f"--- {(round(time.time() - start_time, 5))} seconds ---")

    print("\nTesting spell dispatcher...\n")
    print(spell_dispatcher(42))
    print(spell_dispatcher("fireball"))
    print(spell_dispatcher(["fire", "ice", "toto"]))
    print(spell_dispatcher({}))
