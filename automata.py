from dataclasses import dataclass
from utils import *
from regex import *


# Theoretically an MDFA
@dataclass
class DFA:
    delta: list[list[int]]
    start: int
    finish: list[list[int]]
    stuck: int  # optional information (only computed in minimize_DFA)


# Theoretically an MNFA
@dataclass
class NFA:
    delta: list[list[list[bool]]]
    epsilon: list[list[bool]]
    start: list[bool]
    finish: list[list[bool]]


def merge_NFAs(al: str, rs: list[Re], nfas: list[NFA]) -> NFA:
    num = sum(len(nfa.delta) for nfa in nfas)
    delta = [[[False for _ in range(num)] for _ in al] for _ in range(num)]
    epsilon = [[False for _ in range(num)] for _ in range(num)]
    start = [False for _ in range(num)]
    finish = [[False for _ in rs] for _ in range(num)]
    offset = 0
    for nfa in nfas:
        for i, edges in enumerate(nfa.delta):
            for j, edge in enumerate(edges):
                for k, state in enumerate(edge):
                    delta[offset + i][j][offset + k] = state
            for j, state in enumerate(nfa.epsilon[i]):
                epsilon[offset + i][offset + j] = state
            start[offset + i] = nfa.start[i]
            finish[offset + i] = nfa.finish[i][:]
        offset += len(nfa.delta)
    return NFA(delta, epsilon, start, finish)


def epsilon_reachable(nfa: NFA, states: list[bool], state: int) -> None:
    states[state] = True
    for i, s in enumerate(nfa.epsilon[state]):
        if s and not states[i]:
            epsilon_reachable(nfa, states, i)


def infer_epsilon_closure(al: str, rs: list[Re], nfa: NFA) -> None:
    for i, edges in enumerate(nfa.delta):
        reached = [False] * len(nfa.delta)
        epsilon_reachable(nfa, reached, i)
        for j, state in enumerate(reached):
            if state and i != j:
                nfa.finish[i] = [a or b for a, b in zip(nfa.finish[i], nfa.finish[j])]
                for edge1, edge2 in zip(nfa.delta[i], nfa.delta[j]):
                    for k, s in enumerate(edge2):
                        edge1[k] = edge1[k] or s
        nfa.epsilon[i] = reached


def epsilon_closure(nfa: NFA, state: list[bool]) -> list[bool]:
    next_state = [False] * len(nfa.delta)
    for i, b in enumerate(state):
        if b:
            next_state = [a or b for a, b in zip(next_state, nfa.epsilon[i])]
    return next_state


def NFA_to_DFA(al: str, rs: list[Re], nfa: NFA) -> tuple[DFA, list[list[bool]]]:
    infer_epsilon_closure(al, rs, nfa)

    delta = []
    finish: list[list[int]] = []
    init = epsilon_closure(nfa, nfa.start)
    states = [init]

    index = 0
    tree = Tree()
    Tree.index_state(tree, init, index)
    while index < len(states):
        state = states[index]
        delta.append([-1 for _ in al])

        for i, _ in enumerate(al):
            next_state = [False] * len(nfa.delta)
            for j, b in enumerate(state):
                if b:
                    next_state = [a or b for a, b in zip(next_state, nfa.delta[j][i])]
            next_state = epsilon_closure(nfa, next_state)
            stored = Tree.index_state(tree, next_state, len(states))
            delta[index][i] = stored
            if stored == len(states):
                states.append(next_state)

        finish.append([])
        for i, _ in enumerate(rs):
            for j, s in enumerate(state):
                if s and nfa.finish[j][i]:
                    finish[index].append(i)
                    break
        index += 1

    return DFA(delta, 0, finish, -1), states


def DFA_to_NFA(al: str, rs: list[Re], dfa: DFA) -> NFA:
    num = len(dfa.delta)
    delta = [[[False for _ in range(num)] for _ in al] for _ in range(num)]
    epsilon = [[False for _ in range(num)] for _ in range(num)]
    start = [False for _ in range(num)]
    finish = [[False for _ in rs] for _ in range(num)]
    for i, edges in enumerate(dfa.delta):
        for j, edge in enumerate(edges):
            delta[i][j][edge] = True
        for state in dfa.finish[i]:
            finish[i][state] = True
    if dfa.start >= 0:
        start[dfa.start] = True
    return NFA(delta, epsilon, start, finish)


def remap_states(al: str, rs: list[Re], dfa: DFA, statemap: list[int]) -> DFA:
    num = max(statemap, default=-1) + 1
    delta = [[-1 for _ in al] for _ in range(num)]
    start = statemap[dfa.start]
    finish: list[list[int]] = [[] for _ in range(num)]
    stuck = -1 if dfa.stuck == -1 else statemap[dfa.stuck]
    for i, edges in enumerate(dfa.delta):
        if statemap[i] == -1:
            continue
        for j, edge in enumerate(edges):
            delta[statemap[i]][j] = statemap[edge]
        finish[statemap[i]] = dfa.finish[i][:]
    return DFA(delta, start, finish, stuck)


def minimize_DFA(al: str, rs: list[Re], dfa: DFA) -> DFA:
    order = lambda x, y: (y, x) if x < y else (x, y)
    equal = [
        [dfa.finish[i] == dfa.finish[j] for j in range(i)]
        for i, _ in enumerate(dfa.delta)
    ]
    edges = [
        [
            [order(dfa.delta[i][k], dfa.delta[j][k]) for k, _ in enumerate(al)]
            for j in range(i)
        ]
        for i, _ in enumerate(dfa.delta)
    ]

    # analyze DFA
    change = True
    while change:
        change = False
        for i, edge in enumerate(edges):
            for j, symbols in enumerate(edge):
                if not equal[i][j]:
                    continue
                for k, (next1, next2) in enumerate(symbols):
                    if next1 != next2 and not equal[next1][next2]:
                        equal[i][j] = False
                        change = True

    # construct new DFA
    num = 0
    statemap = [-1 for _ in dfa.delta]
    for i in reversed(range(len(equal))):
        if statemap[i] == -1:
            statemap[i] = num
            num += 1
        for j, _ in enumerate(equal[i]):
            if equal[i][j]:
                statemap[j] = statemap[i]

    # compute stuck state if one exists
    dfa = remap_states(al, rs, dfa, statemap)
    for i, edges in enumerate(dfa.delta):
        loop = True
        for j, edge in enumerate(edges):
            if i != edge:
                loop = False
                break
        if loop and len(dfa.finish[i]) == 0:
            dfa.stuck = i
            break

    return dfa
