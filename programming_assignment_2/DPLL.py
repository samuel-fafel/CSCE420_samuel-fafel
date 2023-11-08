import argparse
import os
import sys
import time

def convert_KB_to_CNF(kb_filename, literals, verbose=False):
    """Converts a Given KB File to a CNF File. If the CNF file already exists, 
    remove it and recreate it.

    Args:
        kb_filename (string): Path of the .kb file to be converted
        verbose (bool, optional): Enables print() feedback. Defaults to False.
        
    Returns:
        clauses: list of clauses included in the CNF
    """
    
    # Append the literals to the KB, if they are not already present
    with open(kb_filename, 'r+') as kb_file:
        for line in kb_file:
            for literal in literals.copy():
                if line == literal:
                    literals.remove(literal)
    
        for literal in literals:
            addition = f"\n{literal}"
            kb_file.write(addition)
    
    # Convert to CNF
    if verbose: print("\nConverting to CNF... ", end='')
    name = kb_filename[kb_filename.find("/") + 1:kb_filename.find('.')]
    command = f"python convCNF.py KBs/{name}.kb -DIMACS >> CNFs/{name}.cnf"
    os.system(f"touch CNFs/{name}.cnf; rm CNFs/{name}.cnf")
    os.system(command)
    if verbose: print("Done")
    
    clauses = []
    with open(f"CNFs/{name}.cnf", 'r') as cnf_file:
        for line in cnf_file:
            if '#' not in line: # not comment line
                symbols = line.split(" ")
                if '\n' in symbols: symbols.remove('\n')
                if symbols:
                    clause = [symbol.strip('\n') for symbol in symbols]
                    clauses.append(clause)
   
    model = {}
    for clause in clauses:
        for symbol in clause:
            model[symbol.strip('-')] = None
    return clauses, model

def parse_args(verbose=False):
    """Parses the Arguments provided in the command line

    Args:
        verbose (bool, optional): Enables print() feedback. Defaults to False.
    
    Returns:
        filename: the filename includded in the command line
        literals: a list of literals added in the command line
             uch: a bool representing the enable or disable of UCH 
    """
    # Create the argument parser
    parser = argparse.ArgumentParser(description="DPLL Algorithm Implementation")
    
    # Add arguments
    parser.add_argument("filename", type=str, help="Filename of the knowledge base")
    parser.add_argument("literals", nargs='*', type=str, help="Additional literals (optional)")
    parser.add_argument("--UCH", action="store_true", help="Enable Unit Clause Heuristic")

    # Parse arguments
    args = parser.parse_args()

    # Echo arguments
    if verbose:
        print(f"Filename: {args.filename}")
        print(f"Literals: {args.literals}")
        print(f"Unit Clause Heuristic Enabled: {args.UCH}")

    return args.filename, args.literals, args.UCH

def find_unit_clause(clauses, model):
    clauses_copy = clauses.copy()
    for clause in clauses_copy:
        # A list to keep track of unassigned literals in the current clause
        unassigned_literals = []
        
        # Check if the clause is a unit clause
        for literal in clause:
            negated = False
            if '-' in literal:
                literal = literal.strip("-")
                negated = True
            # If literal is not in the model, it means it's unassigned
            if literal not in model or model[literal] is None:
                unassigned_literals.append(literal)
            # If the literal is assigned False, it does not affect the unit clause status
            elif model[literal] is False:
                continue
            # If there is a True literal, the clause is not a unit clause, skip to the next clause
            else:
                break
        else:  # This else corresponds to the for loop, not the inner if-else
            # If there is exactly one unassigned literal, we have a unit clause
            if len(unassigned_literals) == 1:
                    return unassigned_literals[0], not negated  # Return the literal and the value it must take
    
    return None, None  # If no unit clause is found, return None

def DPLL_Satisfiable(s):
    """ Initializes clauses and symbols and calls DPLL().

    Args:
        s (string): a sentence in propositional logic
    """
    clauses = set()
    
    return DPLL(clauses, {})

def DPLL(clauses, symbols, model, UCH, verbose=False):
    """Returns

    Args:
        clauses (set): the set of clauses in the CNF representation of a sentence
        model (dict): the current truth assignment of the propositional symbols in a sentence

    Returns:
        bool: True or False for Satisfiability
    """
    if verbose:
        print('---------------')
        print(f"CLAUSES: {clauses}")
        print(f"SYMBOLS: {symbols}")
        print(f"  MODEL: {model}")
        print("---")
    
    # Evaluate Clauses vs current Model
    clauses_bools = []
    clauses_dict = {}
    for i, clause in enumerate(clauses):
        clauses_bools.append(clause.copy())
        for j, symbol in enumerate(clause):
            if model[symbol.strip('-')] == None: # Symbol is Undetermined
                clauses_bools[i][j] = None # Put None in place of Symbol
                clauses_dict[i] = None # Clause is Undetermined
                continue
            if '-' in symbol: # Symbol is Negated
                clauses_bools[i][j] = not model[symbol.strip('-')] # Put Negated Bool in place of Symbol
            else:
                clauses_bools[i][j] = model[symbol.strip('-')] # Put Bool in place of Symbol
            clauses_dict[i] = any(clauses_bools[i])
    if verbose: print(clauses)
    if verbose: print(clauses_bools)
    if verbose: print(clauses_dict)
    
    # BASE CASE 1: ALL CLAUSES EVALUATE TO TRUE:
    if all(clauses_dict.values()):
        if verbose: print("\tBASE CASE 1: ALL TRUE")
        return True, model

    # BASE CASE 2: SOME CLAUSES EVALUATE TO FALSE:
    for clause in clauses_dict.values():
        if clause == False:
            if verbose: print("\tBASE CASE 2: SOME FALSE")
            return False, model
        
    # UCH ENABLED:
    if UCH:
        unit_symbol, value = find_unit_clause(clauses, model)
        if unit_symbol:
            model[unit_symbol] = value
            if verbose: print(f"\tUCH CASE: Unit Symbol = {unit_symbol}")
            unit_test, model = DPLL(clauses, symbols, model, UCH, verbose=verbose)
            return unit_test, model

    # UCH DISABLED OR RETURNS NONE
    for symbol in symbols:
        if model[symbol] == None:
            next_symbol = symbol
    
    if verbose: print(f"\tTOP CASE 1: {next_symbol} = True")
    model_test1 = model.copy()
    model_test1[next_symbol] = True
    test1, model = DPLL(clauses, symbols, model_test1, UCH, verbose)
    if test1:
        return test1, model
    
    if verbose: print(f"\tTOP CASE 2: {next_symbol} = False")
    model_test2 = model.copy()
    model_test2[next_symbol] = False
    test2, model = DPLL(clauses, symbols, model_test2, UCH, verbose)
    return test2, model

if __name__ == "__main__":
    filename, literals, UCH = parse_args()
   
    clauses, model = convert_KB_to_CNF(filename, literals)
    symbols = list(model.keys())
    satisfied, model = DPLL(clauses, symbols, model, UCH, verbose=False)
    print('---------------')
    print(f"SATISFIED: {satisfied}")
    print(f"    MODEL: {model}")


