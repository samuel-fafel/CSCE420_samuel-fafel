Enter instructions and requirements for running your code here.

Run DPLL.py with the command:
    python3 DPLL.py <cnf_filename> <literal>* [+UCH]

The optional arguments are:
    +UCH: If this argument is included, UCH is enabled. Disabled by default
    <literals> individual literals for DPLL to treat as facts. Appends to CNF file's APPENDIX

Make sure that <cnf_filename> points to a cnf file containing DIMACS-format CNF. 
DPLL can only handle DIMACS-format CNF clauses.


Run convCNF.py with the command:
    python3 convCNF.py <kb_filename> [-DIMACS] > <cnf_filename>

The optional arguments are:
    -DIMACS: If this argument is included, DIMACS-format output is enabled. Disabled by default

In either command, make sure that the <filename> contains the full path from the current working directory to the desired file. For example, if the current working directory is ~/Desktop and the target file is in ~/Desktop/CNFs/
then the filename argument would look something like "CNFs/example.cnf"