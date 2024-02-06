import matplotlib.pyplot as plt
from evaluator import *


# algos = [Algo.DFA, Algo.MDFA, Algo.longest, Algo.lookahead, Algo.viable]
algos = [Algo.DFA, Algo.MDFA, Algo.longest]
# algos = [Algo.MDFA, Algo.longest, Algo.lookahead]
colors = ["brown", "green", "blue", "red", "orange"]
shapes = [".", ".", ".", ".", "."]

stats = {algo: load_statistics(algo.value) for algo in algos}

for i, algo in enumerate(algos):
    data = stats[algo]["lexing_steps"]

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
    plt.scatter(x, y, c=c, marker="x", label=algo.value)

    x = []
    y = []
    for j, key in enumerate(sorted(dct)):
        x.append(key)
        y.append(sum(dct[key]) / len(dct[key]))
    plt.plot(x, y, c=colors[i], marker=".")

plt.xlabel("Number of Subexpressions")
plt.ylabel("Number of States")
plt.legend()
plt.show()
