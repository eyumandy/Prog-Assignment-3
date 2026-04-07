import subprocess
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT    = Path(__file__).parent.parent
SOLVER  = ROOT / "src" / "hvlcs.py"
DATA    = ROOT / "data"
RESULTS = ROOT / "results"

LENGTHS = [25, 50, 75, 100, 150, 200, 275, 350, 425, 500]
REPEATS = 5


def time_file(path):
    times = []
    for _ in range(REPEATS):
        t = time.perf_counter()
        subprocess.run(["python", str(SOLVER), str(path)],
                       check=True, capture_output=True)
        times.append(time.perf_counter() - t)
    return min(times)


def run():
    results = []
    for i, n in enumerate(LENGTHS, 1):
        path = DATA / f"test_{i:02d}.in"
        elapsed = time_file(path)
        results.append((n, elapsed))
        print(f"  test_{i:02d}.in  n={n:<4}  {elapsed * 1000:.2f} ms")
    return results


def plot(results):
    RESULTS.mkdir(exist_ok=True)
    xs = [r[0] for r in results]
    ys = [r[1] * 1000 for r in results]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, marker="o", linewidth=2, color="#2563eb",
            markersize=6, markerfacecolor="white", markeredgewidth=2)

    for x, y in zip(xs, ys):
        ax.annotate(f"{y:.1f}", xy=(x, y), xytext=(4, 6),
                    textcoords="offset points", fontsize=8, color="#6b7280")

    ax.set_xlabel("String length  |A| = |B|")
    ax.set_ylabel("Runtime (ms)")
    ax.set_title("HVLCS — Runtime vs. Input Size")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()

    out = RESULTS / "runtime_plot.png"
    fig.savefig(out, dpi=150)
    print(f"\nsaved {out}")


if __name__ == "__main__":
    print("running benchmark...\n")
    plot(run())