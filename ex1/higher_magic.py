from types import FunctionType
from typing import Callable, List, Literal, Protocol, Tuple, cast
from math import sqrt


type Combiner = Callable[[str, int], Tuple[str, str]]
type Conditional = Callable[[str, int], bool]
type SeqSpells = Callable[[str, int], List[str]]
type Spell = Callable[[str, int], str]


class SpellFunc(Protocol):
    power_amplified: int | None = 0

    def __call__(self, target: str, power: int) -> str:
        ...


class heal(SpellFunc):

    def __call__(self, target: str, power: int) -> str:
        return f"Heal restores {target} for {power} HP"


print("sssssssssssssssssssssssssss", heal()("Dragon", 10))

# def heal(target: str, power: int) -> str:
#     return f"Heal restores {target} for {power} HP"


def fireball(target: str, power: int) -> str:
    return f"Fireballs hits {target} for {power} HP"


def spell_combiner(spell1: Spell, spell2: Spell) -> Combiner:
    if not (callable(spell1) and callable(spell2)):
        raise TypeError("arguments spell1 and spell2 must be a function")

    def combiner(target: str, power: int) -> Tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combiner


def power_amplifier_orig(base_spell: SpellFunc, multiplier: int) -> SpellFunc:
    if not callable(base_spell):
        raise TypeError("argument base_spell must be a function")

    class amplified_spell(SpellFunc):
        def  __call__(self, target: str, power: int) -> str:
            amplified_spell.power_amplified = power * multiplier
            return base_spell(target, power * multiplier)
    return amplified_spell()


# def power_amplifier(base_spell: SpellFunc,
#                     multiplier: int) -> SpellFunc:
#     if not callable(base_spell):
#         raise TypeError("argument base_spell must be a function")

#     def amplified_spell(target: str, power: int) -> str:
#         base_spell.power_amplified = multiplier * power
#         return base_spell(target, base_spell.power_amplified)
#     return cast(SpellFunc, amplified_spell)


def test_condition(target: str, power: int) -> bool:
    return (target in ['Dragon', 'Goblin', 'Wizard', 'Knight']
            and power > 10)


# def conditional_caster(condition: Conditional, spell: SpellFunc) -> SpellFunc:
#     if not (callable(spell) and callable(condition)):
#         raise TypeError("arguments must be a functions")

#     def caster(target: str, power: int) -> str:
#         if not condition(target, power):
#             return "Spell fizzled"
#         return spell(target, power)
#     return caster


def spell_sequence(spells: List[SpellFunc]) -> SeqSpells:
    def cast_in_order(target: str, power: int) -> List[str]:
        return [s(target, power) for s in spells]
    return cast_in_order


if __name__ == "__main__":
    try:
        target = "Dragon"
        power = 10
        print("Testing spell combiner...")

        combined: Combiner = spell_combiner(fireball, heal)
        combi: Tuple[str, str] = combined(target, power)
        print("Combined spell result:", sep=" ")
        print(f"{combi[0]}, {combi[1]}")

        print()
        print("Testing power amplifier...")
        original: int = power
        # fireball_spell: SpellFunc = cast(SpellFunc, fireball)
        heal_fn = heal()
        mega_fireball: SpellFunc = power_amplifier_orig(heal_fn, 5)
        print(f"Original power : {power}, Transformed power : {5*power}")
        ampli_spell: str = mega_fireball(target, power)
        print(ampli_spell)
        # ampli: list[int] = [int(s) for s in ampli_spell.split() if s.isdigit()]
        print(f"Original: {original}, Amplified:\
              {mega_fireball.power_amplified}")

    except TypeError as e:
        print(e)