import sys
import queue

class State:
    def __init__(self, stacks):
        self.stacks = stacks

    def __str__(self):
        return '\n'.join([''.join(stack) for stack in self.stacks])

    def is_goal(self, goal):
        return self.stacks == goal.stacks

    def generate_successors(self):
        successors = []

        for i in range(len(self.stacks)):
            if not self.stacks[i]:  # Can't move from an empty stack
                continue
            for j in range(len(self.stacks)):
                if i == j:
                    continue
                
                new_stacks = [stack.copy() for stack in self.stacks]
                block_to_move = new_stacks[i].pop()
                new_stacks[j].append(block_to_move)

                successors.append(State(new_stacks))
        return successors

class Node:
    def __init__(self, state, parent=None, g=0):
        self.state = state
        self.parent = parent
        self.g = g # path cost
        self.h = 0 # heuristic estimate
        self.f = 0 # f = g + h
        self.depth = 0 if parent is None else parent.depth + 1

    def __lt__(self, other):
        return self.f < other.f

def load_problem(filename):
    with open(filename, 'r') as f:
        S, B, M = map(int, f.readline().split())
        f.readline()  # skip separator
        
        initial_stacks = [list(f.readline().strip()) for _ in range(S)]
        f.readline()  # skip separator
        
        goal_stacks = [list(f.readline().strip()) for _ in range(S)]
    return S, B, M, initial_stacks, goal_stacks

def backtrack_solution(node):
    path = []
    while node:
        path.insert(0, node.state)
        node = node.parent
    return path

def heuristic_h0(current, goal):
    # No heuristic, imitate BFS
    return 0

def a_star(initial_state, goal_state, heuristic):
    open_list = queue.PriorityQueue()
    closed_list = set()

    start_node = Node(initial_state, g=0)
    start_node.h = heuristic(start_node.state, goal_state)
    start_node.f = start_node.g + start_node.h
    open_list.put(start_node)

    while not open_list.empty():
        current_node = open_list.get()

        if current_node.state.is_goal(goal_state):
            return backtrack_solution(current_node)

        closed_list.add(str(current_node.state))

        for successor_state in current_node.state.generate_successors():
            successor_node = Node(successor_state, parent=current_node, g=current_node.g + 1)
            successor_node.h = heuristic(successor_node.state, goal_state)
            successor_node.f = successor_node.g + successor_node.h

            if str(successor_node.state) in closed_list:
                continue

            # Check if this node is already in the open_list with a lower cost
            open_list_temp = []
            skip_successor = False
            while not open_list.empty():
                existing_node = open_list.get()
                if existing_node.state == successor_node.state and existing_node.f <= successor_node.f:
                    skip_successor = True
                    open_list_temp.append(existing_node)
                    break
                open_list_temp.append(existing_node)

            for node_to_reinsert in open_list_temp:
                open_list.put(node_to_reinsert)

            if not skip_successor:
                open_list.put(successor_node)

    # Goal not found
    return None

if __name__ == "__main__": # Load & Solve Problem
    S, B, M, initial_stacks, goal_stacks = load_problem(sys.argv[1])
    initial_state = State(initial_stacks)
    goal_state = State(goal_stacks)
    
    heuristic = heuristic_h0
    if "-H" in sys.argv:
        heuristic_flag_index = sys.argv.index("-H")
        heuristic_name = sys.argv[heuristic_flag_index + 1]
        if heuristic_name == "H1":
            heuristic = heuristic_h1

    solution = a_star(initial_state, goal_state, heuristic)  # Using heuristic_h0 as an example
    if solution:
        for step, state in enumerate(solution):
            print(f"move {step}, pathcost={step}, heuristic={heuristic_h0(state, goal_state)}, f(n)=g(n)+h(n)={step + heuristic_h0(state, goal_state)}")
            print(state)
            print(">>>>>>>>>>")
    else:
        print("No solution found.")