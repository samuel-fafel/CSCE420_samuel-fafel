import sys
import os
def write_NQueens_KB(N, verbose=False):
    filename = f"KBs/{N}Queens.kb"
    with open(filename, 'w') as file:
        # Must be Queen in Every Column
        file.write(f"# Must be Queen in Every Column\n")
        for col in range(1, N+1):
            file.write("(or")
            for row in range(1, N+1):
                file.write(f" Q{col}{row}")
            file.write(")\n")
        file.write("\n")
        
        # Must be Queen in Every Row
        file.write(f"# Must be Queen in Every Row\n")
        for row in range(1, N+1):
            file.write("(or")
            for col in range(1, N+1):
                file.write(f" Q{col}{row}")
            file.write(")\n")
        file.write("\n")
        
        # Not Multiple Queens in Same Column
        for col in range(1, N+1):
            file.write(f"# Not Multiple Queens in Column {col}\n")
            for row in range(1, N):
                file.write(f"(not (and Q{col}{row} (or")
                for r in range(row, N):
                    file.write(f" Q{col}{r+1}")
                file.write(f")))\n")
            file.write("\n")
            
         # Not Multiple Queens in Same Row
        for row in range(1, N+1):
            file.write(f"# Not Multiple Queens in Row {row}\n")
            for col in range(1, N):
                file.write(f"(not (and Q{col}{row} (or")
                for c in range(col, N):
                    file.write(f" Q{c+1}{row}")
                file.write(f")))\n")
            file.write("\n")
            
        # Not Multiple Queens in Same Right Diagonal
        right_diags = {}
        for col in range(1, N+1):
            for row in range(1, N+1):
                key = 10*col + row
                right_diags[key] = []
                for c in range(col+1, N+1):
                    for r in range(row+1, N+1):
                        for k in range(1, N):
                            if c == col+k and r == row+k:
                                value = 10*c + r
                                right_diags[key].append(value)
                if right_diags[key] == []:
                    del right_diags[key]
            
        file.write(f"# Not Multiple Queens in Same Right Diagonal\n")
        for key, value in right_diags.items():
            file.write(f"(not (and Q{key} (or")
            for coord in value:
                file.write(f" Q{coord}")
            file.write(f")))\n")
        file.write("\n")
        
        
        # Not Multiple Queens in Same Left Diagonal
        left_diags = {}
        for row in range(1, N+1):
            for col in range(1, N+1):
                key = 10*col + row
                left_diags[key] = []
                for r in range(N, 0, -1):
                    for c in range(N, 0, -1):
                        value = 10*c + r
                        for k in range(1, N):
                            if c == col+k and r == row-k:
                                left_diags[key].append(value)
                if left_diags[key] == []:
                    del left_diags[key]
            
        file.write(f"# Not Multiple Queens in Same Left Diagonal\n")
        for key, value in left_diags.items():
            file.write(f"(not (and Q{key} (or")
            for coord in value:
                file.write(f" Q{coord}")
            file.write(f")))\n")
        file.write("\n")
        
        if verbose:
            for key, value in right_diags.items():
                print(f"{key}:", end='')
                for coord in value:
                    print(f" {coord}", end='')
                print("\n")
                
            for key, value in left_diags.items():
                print(f"{key}:", end='')
                for coord in value:
                    print(f" {coord}", end='')
                print()
        
""" 8x8 Board Coords:
11 21 31 41 51 61 71 81
12 22 32 42 52 62 72 82
13 23 33 43 53 63 73 83
14 24 34 44 54 64 74 84
15 25 35 45 55 65 75 85
16 26 36 46 56 66 76 86
17 27 37 47 57 67 77 87
18 28 38 48 58 68 78 88
"""
                
if __name__ == '__main__':
    NQ = int(sys.argv[1]) # Get number of queens
    write_NQueens_KB(NQ, verbose=False) # Write file for that many queens
    
    command = f"python3 convCNF.py KBs/{NQ}Queens.kb -DIMACS > CNFs/{NQ}Queens.cnf"
    os.system(command)
    