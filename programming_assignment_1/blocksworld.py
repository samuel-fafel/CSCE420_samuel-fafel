import sys
import queue

class State:
    # Defines the current state of the blocksworld
    def __init__(self, stacks):
        self.stacks = stacks
    
    def __str__(self):
        return "\n".join(["".join(stack) for stack in self.stacks])

    def successors(self):
        # Generate all possible successor states from the current state.
        successors = []

        # Iterate over all stacks to find possible blocks to move
        for i, src_stack in enumerate(self.stacks):
            if src_stack:  # if the stack is not empty
                # Get the top block from the source stack
                block_to_move = src_stack[-1]
                
                # Try to move this block to every other stack
                for j, tgt_stack in enumerate(self.stacks):
                    if i != j:  # Don't move the block to the same stack
                        new_stacks = [list(s) for s in self.stacks]  # Create a deep copy of current stacks
                        new_stacks[i].pop()  # Remove the block from the source stack
                        new_stacks[j].append(block_to_move)  # Add the block to the target stack
                        
                        # Create a new state from the modified stacks and add it to successors
                        successors.append(State(new_stacks))
        
        return successors

class Node:
    # Wrapper around State
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state          # The current state
        self.parent = parent        # Parent node
        self.g = g                  # Cost to reach this node from the start
        self.h = h                  # Heuristic estimate from this state to goal
        self.f = self.g + self.h    # f(n) = g(n) + h(n)

    def path(self):
        # Generate the path from the root to this node.
        node, path_backwards = self, []
        while node:
            path_backwards.append(node)
            node = node.parent
        return path_backwards[::-1]  # Return reversed path

    def __str__(self):
        return str(self.state)

    def __lt__(self, other):
        # Compare nodes in a priority queue by their f values.
        return self.f < other.f

class Problem:
    # Stores the input data of the problem
    def __init__(self, S, B, M, initial_stacks, goal_stacks):
        self.S = S  # Number of stacks
        self.B = B  # Number of blocks
        self.M = M  # Number of moves
        self.initial = initial_stacks  # Initial configuration of stacks
        self.goal = goal_stacks  # Goal configuration of stacks

    def __str__(self):
        return (f"S: {self.S}, B: {self.B}, M: {self.M}\n"
                f"Initial Stacks: {self.initial}\n"
                f"Goal Stacks: {self.goal}")
        
    def is_goal(self, state):
        return state.stacks == self.goal

class Result:
    # Stores the output data of the problem
    def __init__(self, node, iters, maxq):
        self.node = node
        self.iters = iters
        self.maxq = maxq

def load_problem(filename):
    with open(filename, 'r') as f:
        S, B, M = map(int, f.readline().split())
        f.readline()  # skip separator
        
        initial_stacks = [list(f.readline().strip()) for _ in range(S)]
        f.readline()  # skip separator
        
        goal_stacks = [list(f.readline().strip()) for _ in range(S)]
    
    return Problem(S, B, M, initial_stacks, goal_stacks)

def heuristic_h0(node, goal):
    # No heuristic, imitate BFS
    return 0

def heuristic_h1(node, goal,):
    # Sum of mismatched blocks
    state = node.state
    mismatches = 0
    for i in range(len(state.stacks)):
        for j in range(min(len(state.stacks[i]), len(goal.stacks[i]))):
            if state.stacks[i][j] != goal.stacks[i][j]:
                mismatches += 1
    return mismatches

def heuristic_h2(node, goal, maxdepth=20):
    # Number of Mismatched blocks are greater than steps left
    mismatches = heuristic_h1(node, goal)
    remaining_steps = maxdepth - node.g

    if mismatches > remaining_steps:
        return mismatches + (mismatches - remaining_steps)
    else:
        return mismatches

def heuristic_h3(node, goal):
    # Depth Balancing Heuristic (Explore states with fewer mismatches)
    return heuristic_h1(node, goal) - node.g//2

def heuristic_h4(node, goal):
    # Reward immediate closeness to solution
    current_stacks = node.state.stacks
    goal_stacks = goal.stacks
    
    heuristic_value = 0
    for current_stack, goal_stack in zip(current_stacks, goal_stacks):
        for i in range(min(len(current_stack), len(goal_stack))):
            # If block is in correct position and order, decrease heuristic_value
            if current_stack[i] == goal_stack[i]:
                heuristic_value -= 1
            else:
                heuristic_value += 2
    return heuristic_value

def a_star(problem, heuristic, maxiters):
    # Best First Search
    initial_state = State(problem.initial)
    goal_state = State(problem.goal)
    initial_node = Node(initial_state)
    
    frontier = queue.PriorityQueue()
    frontier.put(initial_node)
    maxq = frontier.qsize()
    
    reached = {str(initial_state): initial_node}

    iters = 0
    while not frontier.empty():
        solution = Result(None, iters, maxq)
        
        if iters > maxiters: # Surpassed cutoff
            return solution
        
        node = frontier.get()
        
        if problem.is_goal(node.state):
            solution.node = node
            return solution # Return the solution node

        for child_state in node.state.successors():
            g_new = node.g + 1  # Assuming cost for each move is 1
            
            child_node = Node(child_state, parent=node, g=g_new)
            h_new = heuristic(child_node, goal_state)
            child_node.h = h_new
            child_node.f = g_new + h_new
            
            state_str = str(child_state)
            if state_str not in reached or child_node.g < reached[state_str].g:
                reached[state_str] = child_node
                frontier.put(child_node)
        
        if frontier.qsize() > maxq: maxq = frontier.qsize()
        iters += 1

    return solution  # Return failure if no solution found

def print_path(result, filename, silent=False):
    # Writes & Prints the moves from initial to goal
    writefile = filename.replace("probs/", "transcripts/").replace(".bwp", "_transcript.txt")
    with open(writefile, "w") as file:
        if result.node:
            path_to_solution = result.node.path()
            move_count = 0
            for n in path_to_solution:
                message = (f"move {move_count}, pathcost={n.g}, heuristic={n.h}, f(n)=g(n)+h(n)={n.f}\n{n}\n>>>>>>>>>>\n")
                file.write(message)
                move_count += 1
                if not silent: print(message)
        else:
            file.write("")
            
def print_statistics(result, filename, heuristic_name, silent=False):
    # Writes, Prints, and Returns the statistics for each Result
    writefile = filename.replace("probs/", "transcripts/").replace(".bwp", "_transcript.txt")
    newname = filename.replace("probs/", "")
    if result.node:
        move_count = len(result.node.path()) - 1
    else:
        move_count = "FAILED"
    message = (f"statistics: {newname} heuristic {heuristic_name} planlen {move_count} iter {result.iters} maxq {result.maxq}\n")
    with open(writefile, "a") as file:
        file.write(message)
    if not silent: print(message)
    return message

if __name__ == "__main__": # Load & Solve Problem
    filename = sys.argv[1]
    problem = load_problem(filename)
    
    heuristic = heuristic_h4
    heuristic_name = "H4"
    if "-H" in sys.argv:
        heuristic_flag_index = sys.argv.index("-H")
        heuristic_name = sys.argv[heuristic_flag_index + 1]
        match heuristic_name:
            case "H0":
                heuristic = heuristic_h0
            case "H1":
                heuristic = heuristic_h1
            case "H2":
                heuristic = heuristic_h2
            case "H3":
                heuristic = heuristic_h3
            case "H4":
                heuristic = heuristic_h4
            case _:
                heuristic = heuristic_h4
    
    maxiters = 100000
    if "-M" in sys.argv:
        maxiters_flag_index = sys.argv.index("-M")
        maxiters = int(sys.argv[maxiters_flag_index + 1])

    solution = a_star(problem, heuristic, maxiters)
    print_path(solution, filename)
    print_statistics(solution, filename, heuristic_name)
