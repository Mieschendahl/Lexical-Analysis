from dataclasses import dataclass
from typing import Callable
from utils import *
from regex import *
from automata import *


def Regex_to_DFA(al: str, rs: list[Re], index: int, re: Re) -> DFA:
    new = None
    match re:
        case Null():
            delta = [[[True] for _ in al]]
            epsilon = [[False]]
            start = [True]
            finish = [[False for _ in rs]]
            new = NFA(delta, epsilon, start, finish)
        case Eps():
            delta = [[[False] for _ in al]]
            epsilon = [[False]]
            start = [True]
            finish = [[False for _ in rs]]
            finish[0][index] = True
            new = NFA(delta, epsilon, start, finish)
        case Symbol(sym):
            delta = [[[False, sym == a] for a in al], [[False, False] for _ in al]]
            epsilon = [[False, False], [False, False]]
            start = [True, False]
            finish = [[False for _ in rs], [False for _ in rs]]
            finish[1][index] = True
            new = NFA(delta, epsilon, start, finish)
        case Con(r1, r2):
            nfa1 = DFA_to_NFA(al, rs, Regex_to_DFA(al, rs, index, r1))
            nfa2 = DFA_to_NFA(al, rs, Regex_to_DFA(al, rs, index, r2))
            finish = nfa1.finish
            start = nfa2.start
            nfa1.finish = [[False for _ in finish] for finish in nfa1.finish]
            nfa2.start = [False for start in nfa2.start]
            new = merge_NFAs(al, rs, [nfa1, nfa2])
            for i, f in enumerate(finish):
                if f[index]:
                    for j, s in enumerate(start):
                        if s:
                            new.epsilon[i][len(nfa1.delta) + j] = True
        case Alt(r1, r2):
            nfa1 = DFA_to_NFA(al, rs, Regex_to_DFA(al, rs, index, r1))
            nfa2 = DFA_to_NFA(al, rs, Regex_to_DFA(al, rs, index, r2))
            new = merge_NFAs(al, rs, [nfa1, nfa2])
        case Rep(r):
            new = DFA_to_NFA(al, rs, Regex_to_DFA(al, rs, index, r))
            for i, f in enumerate(new.finish):
                if f[index]:
                    for j, s in enumerate(new.start):
                        if s:
                            new.epsilon[i][j] = True
            for i, s in enumerate(new.start):
                if s:
                    new.finish[i][index] = True
        case Neg(r):
            new = DFA_to_NFA(al, rs, Regex_to_DFA(al, rs, index, r))
            for i, f in enumerate(new.finish):
                for j, t in enumerate(f):
                    f[j] = not t
    if new is None:
        raise Exception(f"Unexpected value '{new}'")
    return minimize_DFA(al, rs, NFA_to_DFA(al, rs, new)[0])


def generate_DFA(al: str, rs: list[Re]) -> list[DFA]:
    dfa = [Regex_to_DFA(al, [re], 0, re) for re in rs]
    return dfa


def generate_MDFA(al: str, rs: list[Re]) -> DFA:
    nfas = [DFA_to_NFA(al, rs, Regex_to_DFA(al, rs, i, re)) for i, re in enumerate(rs)]
    dfa = minimize_DFA(al, rs, NFA_to_DFA(al, rs, merge_NFAs(al, rs, nfas))[0])
    return dfa


def reverse_delta(al: str, delta: list[list[int]]) -> list[list[list[bool]]]:
    num = len(delta)
    rdelta = [[[False for _ in range(num)] for _ in al] for _ in range(num)]
    for i, edges in enumerate(delta):
        for j, edge in enumerate(edges):
            rdelta[edge][j][i] = True
    return rdelta


def generate_longest(al: str, rs: list[Re]) -> tuple[DFA, list[list[bool]], DFA]:
    mdfa = generate_MDFA(al, rs)
    rdelta = reverse_delta(al, mdfa.delta)
    delta = []
    finish: list[list[int]] = []
    init = [False] * len(mdfa.delta)
    states = [init]

    index = 0
    tree = Tree()
    Tree.index_state(tree, init, index)
    while index < len(states):
        state = states[index]
        delta.append([-1 for _ in al])

        for i, _ in enumerate(al):
            next_state = [False] * len(mdfa.delta)
            for j, b in enumerate(state):
                if b or len(mdfa.finish[j]) > 0:
                    next_state = [a or b for a, b in zip(next_state, rdelta[j][i])]
            stored = Tree.index_state(tree, next_state, len(states))
            delta[index][i] = stored
            if stored == len(states):
                states.append(next_state)

        finish.append([])
        index += 1

    return DFA(delta, 0, finish, -1), states, mdfa


def generate_lookahead_(al: str, lo: Re) -> tuple[DFA, list[list[bool]], DFA]:
    ldfa = Regex_to_DFA(al, [lo], 0, lo) 
    rdelta = reverse_delta(al, ldfa.delta)
    delta = []
    finish: list[list[int]] = []
    init = [len(f) > 0 for f in ldfa.finish]
    states = [init]

    index = 0
    tree = Tree()
    Tree.index_state(tree, init, index)
    while index < len(states):
        state = states[index]
        delta.append([-1 for _ in al])

        for i, _ in enumerate(al):
            # next_state = [len(f) > 0 for f in ldfa.finish]  # for matching lookahead to prefixes of the rest of the word
            next_state = [False] * len(ldfa.delta)  # for matching lookahead to the whole rest of the word
            for j, b in enumerate(state): 
                if b:
                    next_state = [a or b for a, b in zip(next_state, rdelta[j][i])]
            stored = Tree.index_state(tree, next_state, len(states))
            delta[index][i] = stored
            if stored == len(states):
                states.append(next_state)

        finish.append([])
        index += 1

    return DFA(delta, 0, finish, -1), states, ldfa


def generate_lookahead(al: str, rs: list[Re], lo: list[Re]) -> tuple[list[DFA], list[list[list[bool]]], list[int], DFA]:
    mdfa = generate_MDFA(al, rs)

    mp = []
    states = []
    starts = []
    for i, _ in enumerate(lo):
        m, s, l = generate_lookahead_(al, lo[i])
        mp.append(m)
        states.append(s)
        starts.append(l.start)
    return mp, states, starts, mdfa


def generate_viable(al: str, rs: list[Re]) -> tuple[DFA, list[list[bool]], DFA]:
    mdfa = generate_MDFA(al, rs)
    rep_rs = rep(altls(rs))
    rdfa = Regex_to_DFA(al, [rep_rs], 0, rep_rs) 
    rdelta_mdfa = reverse_delta(al, mdfa.delta)
    rdelta_rdfa = reverse_delta(al, rdfa.delta)
    delta = []
    finish: list[list[int]] = []
    init = [[False] * len(mdfa.delta), [len(f) > 0 for f in rdfa.finish]]
    states = [init]

    index = 0
    tree = Tree()
    Tree.index_state(tree, init[0] + init[1], index)
    while index < len(states):
        state = states[index]
        delta.append([-1 for _ in al])

        for i, _ in enumerate(al):
            state_mdfa, state_rdfa = state
            next_state_mdfa = [False] * len(mdfa.delta)
            next_state_rdfa = [False] * len(rdfa.delta)
            for j, b in enumerate(state_mdfa):
                if b or (state_rdfa[rdfa.start] and len(mdfa.finish[j]) > 0):
                    next_state_mdfa = [a or b for a, b in zip(next_state_mdfa, rdelta_mdfa[j][i])]
            for j, b in enumerate(state_rdfa):
                if b:
                    next_state_rdfa = [a or b for a, b in zip(next_state_rdfa, rdelta_rdfa[j][i])]
            next_state = [next_state_mdfa, next_state_rdfa]
            stored = Tree.index_state(tree, next_state[0] + next_state[1], len(states))
            delta[index][i] = stored
            if stored == len(states):
                states.append(next_state)

        finish.append([])
        index += 1

    return DFA(delta, 0, finish, -1), [s[0] for s in states], mdfa
