import subprocess
import sys
from pathlib import Path

ROOT   = Path(__file__).parent.parent
SOLVER = ROOT / "src" / "hvlcs.py"
DATA   = ROOT / "data"


def run_solver(input_path):
    result = subprocess.run(
        ["python", str(SOLVER), str(input_path)],
        capture_output=True, text=True
    )
    return result.stdout.strip(), result.returncode


def validate_format(output, input_path):
    lines = output.splitlines()
    if len(lines) != 2:
        return False, "expected exactly 2 lines of output"
    if not lines[0].isdigit():
        return False, f"first line is not an integer: {lines[0]!r}"
    return True, ""


def check_against_expected(output, expected_path):
    expected = expected_path.read_text().strip()
    if output != expected:
        return False, f"got {output!r}, expected {expected!r}"
    return True, ""


def run_all():
    cases = sorted(DATA.glob("*.in"))
    passed = failed = 0

    for input_path in cases:
        label = input_path.name
        output, code = run_solver(input_path)

        if code != 0:
            print(f"  FAIL  {label}  (nonzero exit)")
            failed += 1
            continue

        ok, msg = validate_format(output, input_path)
        if not ok:
            print(f"  FAIL  {label}  {msg}")
            failed += 1
            continue

        expected_path = input_path.with_suffix(".out")
        if expected_path.exists():
            ok, msg = check_against_expected(output, expected_path)
            if not ok:
                print(f"  FAIL  {label}  {msg}")
                failed += 1
                continue

        print(f"  PASS  {label}")
        passed += 1

    print(f"\n{passed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(run_all())