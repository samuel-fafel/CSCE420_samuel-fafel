import sys

def extract_CNF(cnf_filename, literals):
    """Extracts the clauses and model from the file.
        Appends given literals to file and adds them to model.

        Args:
            cnf_filename (string): Path of the .cnf file to be read
            literals (list): List of literals to be appended to the file
            
        Returns:
            clauses: list of clauses included in the CNF
            model: dictionary with {symbol:None} for each symbol present
        """
    
    clauses = []
    model = {}
    literals.append("# APPENDIX:\n")
    with open(cnf_filename, 'r+') as cnf_file: # Open file
        lines = cnf_file.readlines() # Read file
        cnf_file.seek(0) # Go back to beginning of file
        cnf_file.truncate() # Truncate File
        for line in lines: 
            if line == literals[-1]: # Stop copying at APPENDIX
                break 
            
            cnf_file.write(line) # Rewrite line to file
            
            if '#' not in line: # Not a comment line
                symbols = line.split(" ") # Get literals
                if '\n' in symbols: symbols.remove('\n')
                clause = [symbol.strip('\n') for symbol in symbols] # Gather literals into clause
                if clause: clauses.append(clause) # Append clause to list
                
            for literal in literals[:-1]: # Prevent duplicates in Appendix
                if line.strip('\n') == literal:
                    literals.remove(literal) 
        
        cnf_file.write(literals[-1]) # Write APPENDIX header
        for literal in literals[:-1]: # Write Appendix values and add to the Model
            cnf_file.write(f"{literal}\n")
            if not '-' in literal:
                model[literal] = True
            else:
                model[literal.strip('-')] = False

    for clause in clauses: # Create Model
        for literal in clause:
            symbol = literal.strip('-')
            if symbol in model.keys(): # If already set in appendix, skip
                continue
            else:
                model[symbol] = None # Else set None
    
    return clauses, model

def parse_args(argv):
    """Parses the Arguments provided in the command line

        Args:
            argv: List of command line arguments passed to the script
        
        Returns:
            filename: the filename included in the command line
            literals: a list of literals added in the command line
                uch: a bool representing the enable or disable of UCH 
        """
    # Initialize variables
    filename = ""
    literals = []
    uch = False

    # Start from 1 to skip the script name
    it = iter(argv[1:])
    for arg in it:
        if arg == "+UCH":
            uch = True
        elif not filename:
            filename = arg
        else:
            literals.append(arg)

    # Check if filename is provided
    if not filename:
        raise ValueError("No filename provided.")

    return filename, literals, uch

def evaluate_clause(clause, model, verbose=False):
    """Checks if a clause is satisfied, unsatisfied, or undetermined.

        Args:
            clause (list): the list of clauses in the CNF
            model (dict): the current truth assignment of each propositional symbol
            verbose (bool, optional): Enable or Disable feedback. Defaults to False.

        Returns:
            bool or None: The satisfaction (True/False) or undetermined (None) state of the clause
        """
    satisfied = False
    for j, literal in enumerate(clause):
        symbol = literal.strip('-')
        if model[symbol] == True and '-' not in literal: # Clause contains True
            satisfied = True
            return satisfied
        elif model[symbol] == False and '-' in literal: # Clause contains (not False)
            satisfied = True
            return satisfied
        elif model[symbol] == None:
            satisfied = None
            
    return satisfied

def find_unit_clause(clauses, model):
    """Finds a unit clause: a clause in which all literals are False except one,
        and sets the one literal unassigned to True, making the clause True.

        Args:
            clauses (list): the list of clauses in the CNF
            model (dict): the current truth assignment of each propositional symbol in the clauses

        Returns:
            string: symbol of the literal to be changed
            bool or None: the correct value of that symbol in the model
        """
    clauses_copy = clauses.copy()
    for clause in clauses_copy:
        if evaluate_clause(clause, model): # Clause is already True, not Unit
            continue
        # A list to keep track of unassigned literals in the current clause
        unassigned_symbols = []
        value = None
        # Check if the clause is a unit clause
        for literal in clause:
            symbol = literal
            negated = False
            if '-' in literal:
                symbol = symbol.strip('-')
                negated = True
                
            if symbol in model.keys():
                if model[symbol] == True and negated: # Literal = False
                    continue # Already assgined False, move on
                elif model[symbol] == False and negated: # Literal = True
                    break # Not a Unit Clause if Literal = True
                elif model[symbol] == True and not negated: # Literal = True
                    break # Not a Unit Clause if Literal = True
                elif model[symbol] == False and not negated: # Literal = False
                    continue # Already assgined False, move on
            
            if symbol not in model.keys() or model[symbol] == None:
                unassigned_symbols.append(literal)
            
        # If there is exactly one unassigned literal, we have a unit clause
        if len(unassigned_symbols) == 1:
            negated = False
            symbol = unassigned_symbols[0]
            if '-' in symbol:
                symbol = symbol.strip('-')
                negated = True
            
            if negated:
                value = False # not False = True
            else:
                value = True # True = True
            attempt = model.copy()
            attempt[symbol] = value
            
            if evaluate_clause(clause, attempt, verbose=True):
                return symbol, value  # Return the literal and the value it must take
    
    return None, None  # If no unit clause is found, return None

def DPLL(clauses, symbols, model, UCH, depth=0, verbose=False):
    """Evaluates a set of clauses against a given model and attempts to satisfy all clauses

        Args:
            clauses (list): the list of clauses in the CNF
            symbols (set): set of symbols used in the model, limited to those not yet assigned a value.
            model (dict): the current truth assignment of each propositional symbol in the clauses
            UCH (bool): Enable or Disable UCH
            depth (int): Depth of Recursion
            verbose (bool): Enable or Disable feedback. Defaults to False.

        Returns:
            bool: True or False for Satisfiability
        """
    
    # Check if every clause in clauses is true in model
    all_satisfied = all(evaluate_clause(clause, model) for clause in clauses)
    if verbose: print(f"Are all satisfied? {all_satisfied}")
    if all_satisfied:
        if verbose: print(f"\tBASE CASE 1: ALL TRUE -- Depth {depth}\n\n")
        return True
    
    # Check if any clause in clauses is false in model
    some_false = any(evaluate_clause(clause, model) == False for clause in clauses)
    if verbose: print(f"Are some false? {some_false}")
    if some_false:
        if verbose:
            print("\t-----------------------")
            print(f"\tBASE CASE 2: SOME FALSE -- Depth {depth}")
            for i, clause in enumerate(clauses):
                if evaluate_clause(clause, model) == False:
                    print(f"\t {clause}")
                    print("\t", end='  ')
                    for symbol in clause:
                        print(f"{symbol.strip('-')} = {model[symbol.strip('-')]}", end=', ')
                    print()
            print("\t-----------------------")
        return False
    
    # Find a unit clause
    if UCH:
        P, value = find_unit_clause(clauses, model)
        if P:
            model[P] = value
            symbols.remove(P)
            if verbose: print(f"\tUCH CASE: Unit Symbol: {P} = {value} -- Depth {depth}\n\n")
            return DPLL(clauses, symbols, model, UCH, depth+1, verbose)
    
    if len(symbols) == 0:
        if verbose: print(f"Ran out of Symbols -- Depth {depth}")
        return None
    
    # Choose the first unassigned symbol
    P = symbols.pop()
    rest = symbols
    
    # Try assigning true to P
    model[P] = True
    if verbose: print(f"\tTOP CASE 1: Attempting {P} = True -- Depth {depth}")
    if DPLL(clauses, rest, model, UCH, depth+1, verbose):
        return True
    
    # Try assigning false to P
    model[P] = False
    if verbose: print(f"\tTOP CASE 2: Attempting {P} = False -- Depth {depth}")
    if DPLL(clauses, rest, model, UCH, depth+1, verbose):
        return True
    
    return False

if __name__ == "__main__":
    # CONVERSION COMMAND:
    # python3 convCNF.py KBs/<FILENAME>.kb -DIMACS > CNFs/<FILENAME>.cnf
    
    filename, literals, UCH = parse_args(sys.argv)
   
    clauses, model = extract_CNF(filename, literals)
    symbols = set()
    for symbol, Bool in model.items():
        if Bool == None: 
            symbols.add(symbol)

    satisfied = DPLL(clauses, symbols, model, UCH, verbose=False)
    print('---------------')
    print(f"SATISFIED: {satisfied}")
    key_list = list(model.keys())
    key_list.sort()
    for symbol in key_list:
        print(symbol, model[symbol])


