import blocksworld as bw

heuristic = bw.heuristic_h4
heuristic_name = "H4"
maxiters = 100000

with open("statistics.txt", "w") as file:
    file.write("")

for a in range(3,12):
    if a < 10:
        filename = f"probs/probA0{a}.bwp"
    else:
        filename = f"probs/probA{a}.bwp"
    problem = bw.load_problem(filename)
    solution = bw.a_star(problem, heuristic, maxiters)
    bw.print_path(solution, filename, silent=True)
    statistic = bw.print_statistics(solution, filename, heuristic_name, silent=True)
    with open("statistics.txt", "a") as file:
        file.write(statistic)
    
for b in range(3,21):
    if b < 10:
        filename = f"probs/probB0{b}.bwp"
    else:
        filename = f"probs/probB{b}.bwp"
    problem = bw.load_problem(filename)
    solution = bw.a_star(problem, heuristic, maxiters)
    bw.print_path(solution, filename, silent=True)
    statistic = bw.print_statistics(solution, filename, heuristic_name, silent=True)
    with open("statistics.txt", "a") as file:
        file.write(statistic)
