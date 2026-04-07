import sys
from pathlib import Path


def parse_input(path):
    lines = Path(path).read_text().splitlines()
    idx = 0

    k = int(lines[idx]); idx += 1
    val = {}
    for _ in range(k):
        ch, v = lines[idx].split(); idx += 1
        val[ch] = int(v)

    A = lines[idx].strip(); idx += 1
    B = lines[idx].strip()
    return val, A, B


def build_dp(A, B, val):
    m, n = len(A), len(B)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = max(
                    dp[i - 1][j - 1] + val.get(A[i - 1], 0),
                    dp[i - 1][j],
                    dp[i][j - 1],
                )
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp


def traceback(dp, A, B):
    i, j = len(A), len(B)
    result = []

    while i > 0 and j > 0:
        if A[i - 1] == B[j - 1] and dp[i][j] > max(dp[i - 1][j], dp[i][j - 1]):
            result.append(A[i - 1])
            i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(result))


def main():
    if len(sys.argv) != 2:
        print("usage: python hvlcs.py <input_file>", file=sys.stderr)
        sys.exit(1)

    val, A, B = parse_input(sys.argv[1])
    dp = build_dp(A, B, val)

    print(dp[len(A)][len(B)])
    print(traceback(dp, A, B))


if __name__ == "__main__":
    main()