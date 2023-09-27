import sys
import queue

class State:
    def __init__(self, stacks):
        self.stacks = stacks
    
    def __str__(self):
        return "\n".join(["".join(stack) for stack in self.stacks])

    def successors(self):
        """Generate all possible successor states from the current state."""
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
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state         # The current state
        self.parent = parent       # Parent node
        self.g = g                 # Cost to reach this node from the start
        self.h = h                 # Heuristic estimate from this state to goal
        self.f = self.g + self.h   # f(n) = g(n) + h(n)

    def path(self):
        """Generate the path from the root to this node."""
        node, path_backwards = self, []
        while node:
            path_backwards.append(node)
            node = node.parent
        return path_backwards[::-1]  # Return reversed path

    def print_path(self):
        path_to_solution = self.path()
        move_count = 0
        for node in path_to_solution:
            print(f"move {move_count}, pathcost={node.g}, heuristic={node.h}, f(n)=g(n)+h(n)={node.f}")
            print(node)
            print(">>>>>>>>>>")
            move_count += 1
        # For statistics (this is a basic example, you might want to add more details later)
        print(f"statistics: method Astar planlen {move_count-1}")

    def __str__(self):
        return str(self.state)

    def __lt__(self, other):
        """This function is used to compare nodes in a priority queue by their f values."""
        return self.f < other.f

class Problem:
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

def load_problem(filename):
    with open(filename, 'r') as f:
        S, B, M = map(int, f.readline().split())
        f.readline()  # skip separator
        
        initial_stacks = [list(f.readline().strip()) for _ in range(S)]
        f.readline()  # skip separator
        
        goal_stacks = [list(f.readline().strip()) for _ in range(S)]
    
    return Problem(S, B, M, initial_stacks, goal_stacks)

def heuristic_h0(state, goal):
    # No heuristic, imitate BFS
    return 0

def heuristic_h1(state, goal):
    # Sum of mismatched blocks
    mismatches = 0
    for i in range(len(state.stacks)):
        for j in range(min(len(state.stacks[i]), len(goal.stacks[i]))):  # Use min to prevent IndexError
            if state.stacks[i][j] != goal.stacks[i][j]:
                mismatches += 1
    return mismatches

def a_star(problem, heuristic):
    initial_state = State(problem.initial)
    goal_state = State(problem.goal)
    initial_node = Node(initial_state, g=0, h=heuristic(initial_state, goal_state))
    
    frontier = queue.PriorityQueue()
    frontier.put(initial_node)
    
    reached = {str(initial_state): initial_node}

    while not frontier.empty():
        node = frontier.get()

        if problem.is_goal(node.state):
            return node  # Return the solution node

        for child_state in node.state.successors():
            g_new = node.g + 1  # Assuming cost for each move is 1
            h_new = heuristic(child_state, goal_state)
            child_node = Node(child_state, parent=node, g=g_new, h=h_new)
            
            state_str = str(child_state)
            if state_str not in reached or child_node.g < reached[state_str].g:
                reached[state_str] = child_node
                frontier.put(child_node)

    return None  # Return failure if no solution found

if __name__ == "__main__": # Load & Solve Problem
    problem = load_problem(sys.argv[1])
    initial_state = State(problem.initial)
    goal_state = State(problem.goal)
    
    heuristic = heuristic_h0
    if "-H" in sys.argv:
        heuristic_flag_index = sys.argv.index("-H")
        heuristic_name = sys.argv[heuristic_flag_index + 1]
        match heuristic_name:
            case "H1":
                heuristic = heuristic_h1
            case _:
                heuristic = heuristic_h0

    solution = a_star(problem, heuristic)
    if solution:
        solution.print_path()
    else:
        print("No solution found.")
