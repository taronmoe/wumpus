# Wumpus World Logical Reasoner (FOL Inference)

This project implements a First-Order Logic (FOL) reasoning system for the
Wumpus World environment. Given partial percept information (breeze, stench),
the system classifies a queried cell as **SAFE**, **UNSAFE**, or **RISKY**
using logical inference rather than probabilistic guessing.

## Overview
The system builds and maintains a knowledge base of logical clauses derived
from domain rules and percepts, then performs inference using unification,
resolution, and proof by contradiction.

Rather than hard-coding conclusions, the solver attempts to prove:
- the cell is SAFE, or
- the cell is UNSAFE

If neither can be proven, the result is classified as RISKY.

## Core Components
- `Knowledge.py`  
  Implements the knowledge base, clause generation, unification, resolution,
  and operation counting.

- `CSCI446_Project2_main_Group27.py`  
  Parses input files, initializes the knowledge base, runs inference, and
  outputs deductions and remaining clauses.

- `CSCI446_Project2_Group27.ipynb`  
  Used for experimentation, analysis, and visualization of inference cost
  across grid sizes and difficulty levels.

## Algorithms & Techniques
- First-Order Logic with clause normal forms
- Unification and resolution
- Proof by contradiction
- Decision-level operation counting (rather than runtime)

## Evaluation
The system was evaluated on multiple caves of varying size and difficulty.
Across 12 test environments, it correctly classified query cells in 10 cases
(≈83% accuracy). Results show that inference cost increases sharply with grid
size and percept ambiguity, highlighting the computational tradeoffs of
symbolic reasoning.

## Notes
This project emphasizes correctness, explainability, and explicit reasoning
over heuristic or probabilistic approaches. It was implemented from scratch
in Python as part of an Artificial Intelligence course.
