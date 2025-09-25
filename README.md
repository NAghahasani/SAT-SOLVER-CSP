🖥️ SAT Solver with CSP & Backtracking (C++)

Solve SAT (Satisfiability) problems using C++, CSP (Constraint Satisfaction Problem) techniques, and backtracking enhanced with smart heuristics! 🚀

🔹 Overview

This solver handles SAT problems in CNF (Conjunctive Normal Form) and uses heuristics to improve search efficiency:

🧩 MRV (Minimum Remaining Values) – pick the variable with the fewest legal options.

⚡ MCV (Most Constrained Variable) – pick the variable involved in the most constraints.

🎯 LCV (Least Constraining Value) – pick the value that interferes least with others.

Classes implemented:

CNF – manages clauses and evaluates hard/soft constraints.

CSP – handles variables, assignments, and applies heuristics for optimized search.

💻 Requirements

C++17 or higher

g++, clang, or MSVC compiler


Run:

./sat_solver      # Linux/Mac
sat_solver.exe    # Windows


Input CNF test cases and get satisfying assignments! ✅

🌟 Features

Backtracking SAT solver

CNF representation of constraints

CSP heuristics: MRV, MCV, LCV

Hard & soft clause evaluation

Analyze runtime & assignments
