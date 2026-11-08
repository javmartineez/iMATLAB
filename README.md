# iMATLAB

**A command-line calculator for modular arithmetic and number theory, built on a hand-written, performance-tuned Python library.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-lightgrey)

iMATLAB (IMAT-LAB) is an interactive and batch interpreter for discrete-mathematics commands: primality, factorisation, GCD, modular powers and inverses, Euler's totient, Legendre symbols, modular square roots and systems of linear congruences. All the maths is implemented from scratch in `modular.py`, with no external libraries, and optimised against benchmark suites of tens of thousands of commands.

> Project for the *Discrete Mathematics* course, Universidad Pontificia Comillas (ICAI).

---

## Commands

| Command | Description | Example | Output |
|---|---|---|---|
| `primo(n)` | Is *n* prime? | `primo(7)` | `Sí` |
| `primos(a,b)` | Primes in [a, b) | `primos(5,20)` | `5, 7, 11, 13, 17, 19` |
| `factorizar(n)` | Prime factorisation | `factorizar(120)` | `2: 3, 3: 1, 5: 1` |
| `mcd(a,b,...)` | Greatest common divisor of any number of integers | `mcd(1,20)` | `1` |
| `coprimos(a,b)` | Are *a* and *b* coprime? | `coprimos(6,9)` | `No` |
| `pow(b,e,p)` | Modular power (negative exponents allowed) | `pow(-3,-8,7)` | `4` |
| `inv(n,p)` | Modular inverse | `inv(3,7)` | `5` |
| `euler(n)` | Euler's totient φ(n) | `euler(10)` | `4` |
| `legendre(n,p)` | Legendre symbol | `legendre(10,3)` | `1` |
| `raiz(n,p)` | Modular square root | `raiz(-1,5)` | `2` |
| `resolverSistema([a;b;p],...)` | Solves a·x ≡ b (mod p) systems | `resolverSistema([1;1;3],[4;7;11])` | `10 (mod 33)` |

The output format is fixed by the assignment specification: `Sí`/`No` for yes/no answers, `NE` when no solution exists, and `NOP` for invalid commands or arguments.

## Highlights

- **Fast arithmetic**: binary (Stein's) GCD with bit tricks, square-and-multiply modular exponentiation, extended Euclid kept reduced mod *p*, and 6k ± 1 wheel factorisation.
- **Generalised Chinese Remainder Theorem**: solves congruence systems whose moduli are *not* pairwise coprime by factorising each modulus into prime powers and checking compatibility.
- **Robust command parser** based on regular expressions, with argument-count validation and clear `NE` / `NOP` error semantics.
- **Interactive and batch modes**: type commands at a `>>>` prompt, or stream a file of commands with `-i` / `-o`.
- **Benchmarking and profiling**: `ficheros_benchmarking/` contains large input suites and a `timeit` + `cProfile` harness used to optimise the library.

## Getting started

```bash
git clone https://github.com/javmartineez/iMATLAB.git
cd iMATLAB
```

Interactive mode (press ENTER on an empty line to quit):

```bash
python imatlab.py
```

```
>>> factorizar(120)
2: 3, 3: 1, 5: 1
>>> resolverSistema([1;1;3],[4;7;11])
10 (mod 33)
```

Batch mode:

```bash
python imatlab.py -i ficheros_benchmarking/ejemplosComandos.txt -o output.txt
```

Benchmark and profile the library:

```bash
cd ficheros_benchmarking
python imatlab_benchmark.py
```

## Project structure

```
iMATLAB/
├── imatlab.py                 # Command parser, interactive loop and batch runner
├── modular.py                 # Number theory library (the core of the project)
├── crypto.ipynb               # Applying the library to RSA: decryption and key cracking
├── tests.zip                  # Unit tests for the library (pytest)
└── ficheros_benchmarking/     # Benchmark inputs, expected outputs and timing harness
```

## Tech stack

Python (standard library only) · regular expressions · timeit / cProfile

## Authors

- **Javier Martínez Berenguer** · [GitHub](https://github.com/javmartineez)
- **Javier Mochales López** · [GitHub](https://github.com/jmochales06)
