import matplotlib.pyplot as plt
from evaluator import *


# directory = "realistic"
directory = "artificial"
algos = [Algo.DFA, Algo.MDFA, Algo.viable, Algo.lookahead, Algo.longest]
colors = ["brown", "green", "orange", "red", "blue"]

shapes = [".", ".", ".", ".", "."]
stats = {algo: load_statistics(directory, algo.value) for algo in algos}

values = "generation_size generation_time lexing_steps lexing_time".split()
ylabel = ["Size of the Automata", "Time in Seconds", "Number of Transitions", "Time in Seconds"]
xlabel = ["Size of the Regexes", "Size of the Regexes", "Length of the Word", "Length of the Word"]
for k, value in enumerate(values):
    for i, algo in enumerate(algos):
        data = stats[algo][value]

        dct = {}
        x = []
        y = []
        for j, (a, b) in enumerate(data):
            x.append(a)
            y.append(b)
            if a in dct:
                dct[a].append(b)
            else:
                dct[a] = [b]

        c = [colors[i]] * len(x)
        s = shapes[i]
        plt.scatter(x, y, c=c, marker=".", label=algo.value)

        x = []
        y = []
        for j, key in enumerate(sorted(dct)):
            x.append(key)
            y.append(sum(dct[key]) / len(dct[key]))
        plt.plot(x, y, c=colors[i])

    plt.xlabel(xlabel[k])
    plt.ylabel(ylabel[k])
    plt.legend()
    print("statistic:", value)
    plt.show()
