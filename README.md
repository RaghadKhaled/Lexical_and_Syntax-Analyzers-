# Lexical and Syntax Analyzers 

---

In this project we implement the first two phases of compilation process in two parts. 
This is a college project required for a compiler course during my BSc studies.<br>
It is done as teamwork with my colleagues.

---

## Part1: Lexical Analyzer using DFA and NFA

We Implement a program that do the following tasks: 
1. Builds an NFA from a given regular expression. 
2. Converts a giving NFA into a DFA. 
3. Builds a DFA from a given regular expression directly.


--- 

## Part2: Syntax Analyzer using Top-Down Parser

In part two, we create LL (1) parser using the following grammar:
```
PROGRAM → STMTS
STMTS → STMT| STMT ; STMTS
STMT → id = EXPR
EXPR → EXPR + TERM | EXPR - TERM | TERM
TERM → TERM * FACTOR | TERM / FACTOR | FACTOR
FACTOR → ( EXPR ) | id | integer
```

---

### Tools

Libraries: 
- PIL
- Tkinter
- Matplotlib
- Networkx
- Ply.lex

Softwares: 

- PyCharm

---

### How to run
- Download all files of code and open it in the programming enviremoner.
- For part 1, run the ```gui``` file to work with the program using GUI. All details about the GUI are illustrated in the Report. 
- For part 2, run the ```main``` file to work with the program using GUI. All details about the GUI are illustrated in the Report. 


