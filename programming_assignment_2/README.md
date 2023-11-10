Instructions and requirements for running my code here.
# ----------- #

Run DPLL.py with the command:
    python3 DPLL.py <cnf_filename> <literal>* [+UCH] [-V]

The optional arguments are:
    <literal> Individual literals for DPLL to treat as facts. Appends to CNF file's APPENDIX.
    +UCH: If this argument is included, UCH is enabled. Disabled by default.
    -V: If this argument is included, Verboseness is enabled, printing tracing information. 
        By default, only resulting model, satisfaction bool, and number of DPLL calls will print.
    

Make sure that <cnf_filename> points to a cnf file containing DIMACS-format CNF. 
DPLL can only handle DIMACS-format CNF clauses.

# ----------- #

Run convCNF.py with the command:
    python3 convCNF.py <kb_filename> [-DIMACS] > <cnf_filename>

The optional arguments are:
    -DIMACS: If this argument is included, DIMACS-format output is enabled. Disabled by default.

# ----------- #

Run queenscript.py with the command:
    python3 queenscript.py <int>

The required arguments are:
    <int>: Number of queens to create a Knowledge Base for.

# ----------- #

In any command, make sure that the <filename> contains the full path from the current working directory 
to the desired file. For example, if the current working directory is ~/Desktop and the target file is 
in ~/Desktop/CNFs/ then the filename argument would look something like "CNFs/example.cnf"