from typing import ParamSpec, TypeGuard, TypeVar
import functools
import time
from typing import Any, Callable


P = ParamSpec('P')
RV = TypeVar('RV')


def spell_timer(func: Callable[P, RV]) -> Callable[P, RV]:
    @functools.wraps(func)
    def timefunc(*args: P.args, **kwargs: P.kwargs) -> RV:
        start_time: float = time.time()
        print("Casting function_name...")
        value = func(*args, **kwargs)
        print("Spells completed in "
              f"{round(time.time() - start_time, 3)} seconds")
        return value
    return timefunc


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    result: int = memoized_fibonacci(n - 2) + memoized_fibonacci(n - 1)
    return result


def fibo(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibo(n - 2) + fibo(n - 1)


def power_validator(min_power: int) -> Callable[[Callable[P, RV]],
                                                Callable[P, RV | str]]:

    def is_power(mypower: object) -> TypeGuard[int]:
        return mypower is not None and isinstance(mypower, int)

    def decorator_factory(func: Callable[P, RV]) -> Callable[P, RV | str]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> RV | str:
            pow: object = kwargs.get("power")
            if not is_power(pow):
                raise TypeError(("First argument must be the "
                                "power as integer !"))
            power: int = int(pow)
            if power >= min_power:
                return func(*args, **kwargs)
            else:
                return "Insufficient power for this spell"
        return wrapper
    return decorator_factory


def retry_spell(max_attempts: int) -> Callable[[Callable[P, RV]],
                                               Callable[P, RV | str]]:
    def decorator_retry(func: Callable[P, RV]) -> Callable[P, RV | str]:
        @functools.wraps(func)
        def generate_error(*args: P.args,
                           **kwargs: P.kwargs) -> RV | str:
            for n in range(max_attempts):
                try:
                    if n == 5:
                        return func(*args, **kwargs)
                    raise ValueError("failed")
                except ValueError:
                    print("Spell failed, retrying... (attempt "
                          f"{n + 1}/{max_attempts})")
            return "Spell casting failed after max_attempts attempts"
        return generate_error
    return decorator_retry


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        return all(str.isalpha(x) or str.isspace(x) for x in name)

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":
    n: int = 35
    time_fibo: Callable[..., Any] = spell_timer(fibo)
    x = time_fibo(n)
    time_memoize_fibo: Callable[..., Any] = spell_timer(memoized_fibonacci)
    time_memoize_fibo(n)

    print("Testing power_validator...")

    @power_validator(10)
    def heal_power(power: int) -> str:
        return f"heal power costs {power} points"
    power_min = 10
    print(heal_power(power=12))
    print(heal_power(power=8))

    print("\nTesting retry_spell...")

    @retry_spell(5)
    def heal_power2(power: int) -> str:
        return f"heal power costs {power} points"
    print(heal_power2(power=3))

    print()

    @retry_spell(10)
    def heal_power3(power: int) -> str:
        return f"heal power costs {power} points"
    print(heal_power3(power=3))

    print("\nTesting MageGuild...\n")
    print("is 'Sorcier' a valid name ?",
          MageGuild.validate_mage_name("Sorcier"))
    print("is 'Sorc ier' a valid name ?",
          MageGuild.validate_mage_name("Sorc ier"))
    print("is 'So' a valid name ?",
          MageGuild.validate_mage_name("So"))
    casted: str = MageGuild().cast_spell(power=10, spell_name="fire")
    print(casted)
