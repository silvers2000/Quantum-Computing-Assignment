# Simon's Algorithm – Qiskit Implementation

## Chosen 5-bit Secret String

```
s = '10110'
```

---

## Repository Structure

```
.
├── simon_3bit.ipynb      # Part A – Reference implementation for s = '011'
├── simon_5bit.ipynb      # Part B & C – Simon's algorithm for s = '10110'
├── classical_solve.py    # Part C – GF(2) linear-system solver
└── README.md
```

---

## Requirements

Install dependencies:

```bash
pip install qiskit qiskit-aer
```

Tested with:
- Python 3.10+
- qiskit 1.x
- qiskit-aer 0.14+

---

## How to Run

### Jupyter Notebooks

```bash
jupyter notebook simon_3bit.ipynb   # Reference 3-bit example  (s = '011')
jupyter notebook simon_5bit.ipynb   # 5-bit implementation      (s = '10110')
```

Run all cells top-to-bottom. The notebooks use `AerSimulator` (local) – no IBM
Quantum account is required.

### Classical Solver (standalone)

```bash
python classical_solve.py
```

This script reads the measurement outcomes hard-coded from the simulation
results, constructs the matrix equation **U s = 0 (mod 2)**, performs Gaussian
elimination over GF(2), and prints the recovered secret string.

---

## Recovered Secret String

After running Simon's circuit with **2000 shots** and discarding the trivial
all-zeros outcome, the classical GF(2) solver uniquely recovers:

```
s = '10110'
```

which matches the string used to construct the oracle, confirming correctness
of both the quantum and classical stages.

---

## Quick Algorithm Summary

| Stage | What happens |
|---|---|
| 1st Hadamard layer | Creates uniform superposition over all *n*-bit inputs |
| Oracle | Encodes the 2-to-1 function *f(x) = f(x ⊕ s)* |
| 2nd Hadamard layer | Quantum interference keeps only *u* satisfying *u · s = 0 (mod 2)* |
| Measurement | Samples a random valid *u*; repeat O(*n*) times |
| Classical post-processing | Gaussian elimination over GF(2) recovers *s* |
