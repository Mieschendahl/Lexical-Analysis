# type: ignore
# do not use pytest with this file, just run it with py to test it
from typing import Union, Callable, Any
from generation import *
from lexing import *
from evaluator import *


def test_null(algo) -> None:
    alpha = "ab"
    regexes = [Null()]
    problems = ["", [], "a", []]
    evaluate(Config(algo, alpha, regexes, problems))


def test_epsilon(algo) -> None:
    alpha = "a"
    regexes = [Eps()]
    problems = ["", ["", 0], "a", []]
    evaluate(Config(algo, alpha, regexes, problems))
    alpha = "ab"
    evaluate(Config(algo, alpha, regexes, problems))


def test_symbol(algo) -> None:
    alpha = "ab"
    regexes = [Sym("a")]
    problems = [
        "", [],
        "a", ["a", 0],
        "b", [],
        "ab", [],
        "ba", [],
        "aa", ["a", 0, "a", 0],
        "aab", [],
        "aaa", ["a", 0, "a", 0, "a", 0]
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    alpha = "abc"
    regexes = [Sym("a"), Sym("b")]
    problems = [
        "", [],
        "a", ["a", 0],
        "b", ["b", 1],
        "ab", ["a", 0, "b", 1],
        "ba", ["b", 1, "a", 0],
        "aa", ["a", 0, "a", 0],
        "bab", ["b", 1, "a", 0, "b", 1],
        "c", [],
        "cb", [],
        "bacb", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_concat(algo) -> None:
    alpha = "ab"
    regexes = [con(Sym("a"), Sym("a"))]
    problems = [
        "", [],
        "a", [],
        "b", [],
        "ab", [],
        "ba", [],
        "aa", ["aa", 0],
        "aaa", [],
        "aaaa", ["aa", 0, "aa", 0],
        "aaaaaa", ["aa", 0, "aa", 0, "aa", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_alternative(algo) -> None:
    alpha = "abc"
    regexes = [alt(Sym("a"), Sym("b"))]
    problems = [
        "", [],
        "a", ["a", 0],
        "b", ["b", 0],
        "ab", ["a", 0, "b", 0],
        "ba", ["b", 0, "a", 0],
        "aa", ["a", 0, "a", 0],
        "bab", ["b", 0, "a", 0, "b", 0],
        "c", [],
        "cb", [],
        "bacb", []
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_repeat(algo) -> None:
    alpha = "ab"
    regexes = [rep(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", ["a", 0],
        "aa", ["aa", 0],
        "aaa", ["aaa", 0],
        "b", [],
        "ba", [],
        "aaab", []
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    alpha = "abc"
    regexes = [rep(Sym("a")), rep(Sym("b"))]
    problems = [
        "", ["", 0],
        "a", ["a", 0],
        "b", ["b", 1],
        "ab", ["a", 0, "b", 1],
        "ba", ["b", 1, "a", 0],
        "aa", ["aa", 0],
        "aabb", ["aa", 0, "bb", 1],
        "bbaa", ["bb", 1, "aa", 0],
        "caabb", [],
        "aabbc", [],
        "bbaac", []
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_negate(algo) -> None:
    alpha = "ab"
    regexes = [neg(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", [],
        "aa", ["aa", 0],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "aaab", ["aaab", 0],
        "bb", ["bb", 0],
        "bbba", ["bbba", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [neg(rep(Sym("a")))]
    problems = [
        "", [],
        "a", [],
        "aa", [],
        "aaa", [],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "aaab", ["aaab", 0],
        "bb", ["bb", 0],
        "bbba", ["bbba", 0]
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [neg(Null())]
    problems = [
        "", ["", 0],
        "a", ["a", 0],
        "aa", ["aa", 0],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "aaab", ["aaab", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [neg(Eps())]
    problems = [
        "", [],
        "a", ["a", 0],
        "aa", ["aa", 0],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "aaab", ["aaab", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [negg(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", [],
        "aa", [],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "ab", [],
        "aaab", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_repeat_shortest(algo) -> None:
    alpha = "ab"
    regexes = [rep(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", [],
        "aa", [],
        "b", [],
        "ba", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    alpha = "abc"
    regexes = [rep(Sym("a")), rep(Sym("b"))]
    problems = [
        "", ["", 0],
        "a", [],
        "b", [],
        "ba", [],
        "bbaa", [],
        "bbaac", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_negate_shortest(algo) -> None:
    alpha = "ab"
    regexes = [neg(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", [],
        "aa", [],
        "b", [],
        "ba", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [neg(rep(Sym("a")))]
    problems = [
        "", [],
        "a", [],
        "aa", [],
        "aba", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


algos = [Algo.DFA, Algo.MDFA, Algo.longest, Algo.lookahead, Algo.viable]
for algo in algos:
    test_null(algo)
    test_epsilon(algo)
    test_symbol(algo)
    test_concat(algo)
    test_alternative(algo)
    if algo is not Algo.lookahead:
        test_repeat(algo)
        test_negate(algo)
    else:
        test_repeat_shortest(algo)
        test_negate_shortest(algo)
        


algo = Algo.longest
alpha = "abc"
regexes = [con(Sym("a"), Sym("a")), con(Sym("a"), con(Sym("a"), Sym("a")))]
problems = [
    "aa", ["aa", 0],
    "aaa", ["aaa", 1],
    "aaaaa", ["aaa", 1, "aa", 0],
]
evaluate(Config(algo, alpha, regexes, problems))
