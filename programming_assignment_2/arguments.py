import argparse
import subprocess
import sys

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="DPLL Algorithm Implementation")
    
    # Add arguments
    parser.add_argument("filename", type=str, help="Filename of the knowledge base")
    parser.add_argument("literals", nargs='*', type=str, help="Additional literals (optional)")
    parser.add_argument("--UCH", action="store_true", help="Enable Unit Clause Heuristic")

    # Parse arguments
    args = parser.parse_args()

    # Echo arguments
    print(f"Filename: {args.filename}")
    print(f"Literals: {args.literals}")
    print(f"Unit Clause Heuristic Enabled: {args.UCH}")

    # Read the knowledge base file
    try:
        with open(args.filename, 'r') as file:
            knowledge_base = file.read()
            print("\nKnowledge base content:")
            print(knowledge_base)
    except FileNotFoundError:
        print(f"The file {args.filename} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    # Convert to CNF
    print("\nConverting to CNF:")
    subprocess.run(["python", "convCNF.py", args.filename, "-DIMACS", ">>", "animals.cnf"])

    # Further DPLL processing will go here
    # ...

if __name__ == "__main__":
    main()
