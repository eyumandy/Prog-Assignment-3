import random
from pathlib import Path

ALPHABET = list("abcdefghijklmnopqrstuvwxyz")

CONFIGS = [
    (25,  101),
    (50,  102),
    (75,  103),
    (100, 104),
    (150, 105),
    (200, 106),
    (275, 107),
    (350, 108),
    (425, 109),
    (500, 110),
]


def make_input(length, seed):
    rng = random.Random(seed)
    val_lines = "\n".join(f"{ch} {rng.randint(1, 10)}" for ch in ALPHABET)
    A = "".join(rng.choices(ALPHABET, k=length))
    B = "".join(rng.choices(ALPHABET, k=length))
    return f"{len(ALPHABET)}\n{val_lines}\n{A}\n{B}\n"


if __name__ == "__main__":
    out = Path(__file__).parent.parent / "data"
    out.mkdir(exist_ok=True)
    for i, (length, seed) in enumerate(CONFIGS, 1):
        path = out / f"test_{i:02d}.in"
        path.write_text(make_input(length, seed))
        print(f"wrote {path.name}  (n={length})")