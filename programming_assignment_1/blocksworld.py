import heapq
import sys

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

if __name__ == "__main__":
    file = "probs/probB12.bwp"
    S,B,M, initial, goal = load_problem(file)
    
    print(S, B, M)
    print(">>>>>>>>>>")
    for i in initial:
        for j in i:
            print(j, end="")
        print()
    print(">>>>>>>>>>")
    for i in goal:
        for j in i:
            print(j, end="")
        print()

