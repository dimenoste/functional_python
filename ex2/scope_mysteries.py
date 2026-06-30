from typing import Callable, TypedDict


def mage_counter() -> Callable[[], int]:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total_int: int = initial_power

    def accumulator(extra_amount: int) -> int:
        nonlocal total_int
        total_int += extra_amount
        print(f"Base {initial_power}, add {extra_amount} : {total_int}")
        return total_int

    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:

    def create_enchantement(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return create_enchantement


class MemVault(TypedDict):
    recall: Callable[[str], int | str]
    store: Callable[[str, int], int]


def memory_vault() -> MemVault:
    dico: dict[str, int] = dict()

    def store(key: str, value: int) -> int:
        dico[key] = value
        return dico[key]

    def recall(key: str) -> int | str:
        if key in dico.keys():
            return dico[key]
        else:
            return "Memory not found"

    vault = MemVault(recall=recall, store=store)
    return vault


if __name__ == '__main__':
    print("Testing mage counter...")
    counter_a: Callable[[], int] = mage_counter()
    print("counter_a call 1: ", counter_a())
    print("counter_a call 2: ", counter_a())
    counter_b: Callable[[], int] = mage_counter()
    print("counter_b call 1: ", counter_b())

    print("Testing spell accumulator...")
    acc: Callable[[int], int] = spell_accumulator(100)
    acc(20)
    acc(30)

    print()
    print("Testing memory vault...")
    vault: MemVault = memory_vault()
    key = 'secret'
    value = 42
    print(f"Store {key} = {vault["store"](key, value)}")
    print(f"Recall {key}: {vault["recall"](key)}")
    print(f"Recall 'unknown': {vault["recall"]("unknown")}")

    print()
    print("Testing enchantment factory...")
    create_flaming: Callable[[str], str] = enchantment_factory("Flaming")
    flam_customed: str = create_flaming("Sword")
    print(flam_customed)
    create_frozen: Callable[[str], str] = enchantment_factory("Frozen")
    frozen_customed: str = create_frozen("Shield")
    print(frozen_customed)
