import matplotlib.pyplot as plt
from evaluator import *


# algos = [Algo.DFA, Algo.MDFA, Algo.longest, Algo.lookahead, Algo.viable]
algos = [Algo.DFA, Algo.MDFA, Algo.longest]
colors = ["brown", "green", "blue", "red", "purple"]
shapes = ["x", "+", "2", "3", "4"]
stats = {}

for algo in algos:
    stats[algo] = load_statistics(algo.value)

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
    plt.scatter(x, y, c=c, marker=s, label=algo.value)

    x = []
    y = []
    for j, key in enumerate(sorted(dct)):
        x.append(key)
        y.append(sum(dct[key]) / len(dct[key]))
    plt.plot(x, y, c=colors[i])
    

plt.legend()
plt.show()
