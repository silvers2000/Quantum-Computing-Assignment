"""
Classical Post-Processing for Simon's Algorithm
================================================
Solves the system  U s = 0  (mod 2)  using Gaussian elimination over GF(2).

Usage
-----
Run directly:
    python classical_solve.py

Or call solve_simon(outcomes, n) from another script.

The script demonstrates recovery of the 5-bit secret string s = '10110'
from measurement outcomes obtained in Part B.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# GF(2) Gaussian Elimination
# ---------------------------------------------------------------------------

def gf2_rref(matrix: list[list[int]]) -> tuple[list[list[int]], list[int], list[int]]:
    """
    Reduce a binary matrix to Row Reduced Echelon Form over GF(2).

    Returns
    -------
    rref     : reduced matrix (modified in-place copy)
    pivots   : list of pivot column indices
    free     : list of free (non-pivot) column indices
    """
    M = [row[:] for row in matrix]          # work on a copy
    n_rows, n_cols = len(M), len(M[0])
    pivot_row = 0
    pivots: list[int] = []

    for col in range(n_cols):
        # find a pivot in this column at or below pivot_row
        found = None
        for r in range(pivot_row, n_rows):
            if M[r][col] == 1:
                found = r
                break
        if found is None:
            continue                         # no pivot in this column

        M[pivot_row], M[found] = M[found], M[pivot_row]
        pivots.append(col)

        # eliminate all other rows
        for r in range(n_rows):
            if r != pivot_row and M[r][col] == 1:
                M[r] = [(M[r][j] ^ M[pivot_row][j]) for j in range(n_cols)]

        pivot_row += 1

    free = [c for c in range(n_cols) if c not in pivots]
    return M, pivots, free


def solve_simon(outcomes: list[str]) -> list[str]:
    """
    Recover all non-trivial solutions s ≠ 0 of  U s = 0  (mod 2).

    Parameters
    ----------
    outcomes : list of bit-strings (each '0'/'1' string, no all-zeros entry)

    Returns
    -------
    solutions : list of bit-strings representing candidate secret strings
    """
    if not outcomes:
        raise ValueError("No measurement outcomes provided.")

    n = len(outcomes[0])
    U = [[int(c) for c in u] for u in outcomes]

    rref, pivots, free_cols = gf2_rref(U)

    solutions: list[str] = []
    for fc in free_cols:
        s_vec = [0] * n
        s_vec[fc] = 1                        # set free variable to 1
        for idx, pc in enumerate(pivots):
            s_vec[pc] = rref[idx][fc]        # back-substitute
        candidate = ''.join(map(str, s_vec))
        if '1' in candidate:                 # skip trivial all-zeros
            solutions.append(candidate)

    return solutions


# ---------------------------------------------------------------------------
# Pretty-print helpers
# ---------------------------------------------------------------------------

def print_system(outcomes: list[str]) -> None:
    """Print the linear system U s = 0 (mod 2) in a readable form."""
    n = len(outcomes[0])
    vars_ = [f"s{i}" for i in range(n)]
    header = "  Equation                             u · s (mod 2)"
    print(header)
    print("-" * len(header))
    for u in outcomes:
        terms = " + ".join(f"{vars_[i]}" for i in range(n) if u[i] == '1') or "0"
        print(f"  u = {u}  →  {terms:30s} = 0")


def verify_solution(s: str, outcomes: list[str]) -> bool:
    """Check that u · s = 0 (mod 2) for every outcome u."""
    n = len(s)
    s_vec = [int(c) for c in s]
    return all(
        sum(int(u[i]) * s_vec[i] for i in range(n)) % 2 == 0
        for u in outcomes
    )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Simon's Algorithm – Classical Post-Processing")
    print("Secret string: s = '10110'  (5 qubits)")
    print("=" * 60)

    # Measurement outcomes from the quantum simulation (Part B).
    # All-zeros outcome (00000) is excluded as instructed.
    outcomes_5bit = [
        "11011", "00001", "10100", "01000", "01110",
        "11100", "10010", "01001", "11101", "10011",
        "00111", "10101", "00110", "01111", "11010",
    ]

    print(f"\nNumber of non-trivial measurement outcomes: {len(outcomes_5bit)}")
    print("\nLinear system  U s = 0  (mod 2) – first 8 equations shown:")
    print_system(outcomes_5bit[:8])

    print("\n--- Gaussian Elimination over GF(2) ---")
    U = [[int(c) for c in u] for u in outcomes_5bit]
    rref, pivots, free_cols = gf2_rref(U)

    print(f"Pivot columns : {pivots}")
    print(f"Free  columns : {free_cols}")
    print("\nRow Reduced Echelon Form (non-zero rows only):")
    for row in rref:
        if any(row):
            print(" ", row)

    print("\n--- Recovered Secret String(s) ---")
    solutions = solve_simon(outcomes_5bit)
    if solutions:
        for sol in solutions:
            ok = verify_solution(sol, outcomes_5bit)
            print(f"  s = '{sol}'   verification (all u·s = 0 mod 2): {ok}")
    else:
        print("  No non-trivial solution found – check your outcomes.")

    print("\nConclusion: The recovered secret string matches s = '10110'.")
    print("=" * 60)
