from dataclasses import dataclass
from typing import Callable, Optional
from utils import *
from regex import *
from automata import *


@dataclass(frozen=True)
class Token:
    value: str
    index: int


lexing_statistics = {
    "transitions": 0
}


def clear_lexing_statistics():
    lexing_statistics["transitions"] = 0


def run_DFA(lookup: Callable[[str], int], dfa: list[DFA], w: str, start: int) -> tuple[Token, int]:
    index = end = start
    r = -1
    states = [d.start for d in dfa]
    while True:
        for i, state in enumerate(states):
            if len(dfa[i].finish[state]) > 0:
                end = index
                r = i
                break
        stuck = True
        for i, state in enumerate(states):
            if state != dfa[i].stuck:
                stuck = False
                break
        if stuck or index == len(w):
            return (Token(w[start:end], r), end)
        for i, state in enumerate(states):
            states[i] = dfa[i].delta[state][lookup(w[index])]
            lexing_statistics["transitions"] += 1
        index += 1


def lex_DFA(lookup: Callable[[str], int], dfa: list[DFA], w: str) -> list[Token]:
    tokenization = []
    index = 0
    while True:
        t, index = run_DFA(lookup, dfa, w, index)
        if t.index == -1 or (t.value == "" and w != ""):
            return []
        tokenization.append(t)
        if index == len(w):
            return tokenization


def run_MDFA(lookup: Callable[[str], int], mdfa: DFA, w: str, start: int) -> tuple[Token, int]:
    index = end = start
    r = -1
    state = mdfa.start
    while True:
        if len(mdfa.finish[state]) > 0:
            end = index
            r = mdfa.finish[state][0]
        if state == mdfa.stuck or index == len(w):
            return (Token(w[start:end], r), end)
        state = mdfa.delta[state][lookup(w[index])]
        lexing_statistics["transitions"] += 1
        index += 1


def lex_MDFA(lookup: Callable[[str], int], mdfa: DFA, w: str) -> list[Token]:
    tokenization = []
    index = 0
    while True:
        t, index = run_MDFA(lookup, mdfa, w, index)
        if t.index == -1 or (t.value == "" and w != ""):
            return []
        tokenization.append(t)
        if index == len(w):
            return tokenization


# Match Predictor to Oracle
def MP_to_MO(lookup: Callable[[str], int], mp: DFA, states: list[list[bool]], w: str) -> Callable[[int, int], bool]:
    index = len(w)
    ms = [-1] * (len(w) + 1)
    state = mp.start
    while True:
        ms[index] = state
        if index == 0:
            return lambda q, i: states[ms[i]][q]
        index -= 1
        state = mp.delta[state][lookup(w[index])]
        lexing_statistics["transitions"] += 1


def run_longest(lookup: Callable[[str], int], mo: Callable[[int, int], bool], mdfa: DFA, w: str, start: int) -> tuple[Token, int]:
    index = end = start
    r = -1
    state = mdfa.start
    while True:
        if len(mdfa.finish[state]) > 0:
            end = index
            r = mdfa.finish[state][0]
        if index == len(w) or not mo(state, index):
            return (Token(w[start:end], r), end)
        state = mdfa.delta[state][lookup(w[index])]
        lexing_statistics["transitions"] += 1
        index += 1


def lex_longest(lookup: Callable[[str], int], lex: tuple[DFA, list[list[bool]], DFA], w: str) -> list[Token]:
    mp, states, mdfa = lex
    mo = MP_to_MO(lookup, mp, states, w)

    tokenization = []
    index = 0
    while True:
        t, index = run_longest(lookup, mo, mdfa, w, index)
        if t.index == -1 or (t.value == "" and w != ""):
            return []
        tokenization.append(t)
        if index == len(w):
            return tokenization


def run_lookahead(lookup: Callable[[str], int], mo: list[Callable[[int, int], bool]],
    starts: list[int], mdfa: DFA, w: str, start: int) -> tuple[Token, int]:
    index = end = start
    r = -1
    state = mdfa.start
    while True:
        if len(mdfa.finish[state]) > 0:
            for i in mdfa.finish[state]:
                if mo[i](starts[i], index):
                    end = index
                    r = i
                    break
        if index == len(w) or r != -1:
            return (Token(w[start:end], r), end)
        state = mdfa.delta[state][lookup(w[index])]
        lexing_statistics["transitions"] += 1
        index += 1


def lex_lookahead(lookup: Callable[[str], int], lex: tuple[list[DFA], list[list[list[bool]]], list[int], DFA], w: str) -> list[Token]:
    mp, states, starts, mdfa = lex
    mo = []
    for i, _ in enumerate(mp):
        mo.append(MP_to_MO(lookup, mp[i], states[i], w))

    tokenization = []
    index = 0
    while True:
        t, index = run_lookahead(lookup, mo, starts, mdfa, w, index)
        if t.index == -1 or (t.value == "" and w != ""):
            return []
        tokenization.append(t)
        if index == len(w):
            return tokenization
